"""
Ollama RAG Client with Validated Question Generation
------------------------------------------------------
This client uses a two-stage approach to ensure consistency:
1. Model generates: complete code + target to replace + distractors
2. System deterministically creates question with guaranteed correct answer

Usage: python genai_ollama_client_with_rag_validated.py "Your question here"
"""

import requests
import json
import math
import time
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter
import sys
import io
import argparse

# Fix encoding for Windows console to support emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# =======================================================
# 🔧 CONFIGURATION
# =======================================================
OLLAMA_URL = "https://null-server-reliability-integration.trycloudflare.com"
GEN_MODEL = "qwen2.5:14b"
TIMEOUT = 600
CONTEXT_FILE = "context_with_validation.txt"  # New validation-formatted context
MODEL_CONTEXT_SIZE = 128_000  # in tokens
AVG_CHARS_PER_TOKEN = 4.0
KEEP_ALIVE = "60m"

# RAG Configuration
MAX_EXAMPLES_TO_RETRIEVE = 20  # Number of examples to retrieve
MAX_CONTEXT_TOKENS = 30_000    # Maximum tokens for context
# =======================================================


class ContextParser:
    """Parses context.txt file into structured examples."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.examples = []
        self.instructions = ""

    def parse(self):
        """Parse the context file into examples and instructions."""
        path = Path(self.filepath)
        if not path.exists():
            raise FileNotFoundError(f"Context file not found: {self.filepath}")

        content = path.read_text(encoding="utf-8")

        # Extract instructions section
        instructions_match = re.search(
            r'HOW TO CREATE ACCURATE FILL-IN-THE-BLANK QUESTIONS.*?(?=SIMPLE FILL-IN-THE-BLANK EXAMPLES)',
            content,
            re.DOTALL
        )
        if instructions_match:
            self.instructions = instructions_match.group(0).strip()

        # Parse individual examples
        example_pattern = r'------------------\s*Fill-in-the-Blank Question Example ([^(]+)\(([^)]+)\)\s*------------------\s*(.*?)(?=------------------\s*Fill-in-the-Blank Question Example|END OF EXAMPLES|$)'

        matches = re.finditer(example_pattern, content, re.DOTALL)

        for match in matches:
            example_id = match.group(1).strip()
            description = match.group(2).strip()
            full_text = match.group(3).strip()

            # Extract keywords from description and content
            keywords = self._extract_keywords(description + " " + full_text)

            example = {
                'id': example_id,
                'description': description,
                'text': match.group(0),  # Full example text
                'keywords': keywords
            }
            self.examples.append(example)

        print(f"📚 Parsed {len(self.examples)} examples from context file")
        return self

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        cpp_keywords = {
            'int', 'float', 'double', 'char', 'string', 'bool', 'void',
            'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue',
            'class', 'struct', 'public', 'private', 'protected',
            'new', 'delete', 'nullptr', 'NULL',
            'return', 'cout', 'cin', 'endl', 'namespace', 'using', 'std',
            'include', 'iostream', 'vector', 'map', 'set', 'list', 'queue', 'stack',
            'template', 'typename', 'virtual', 'override', 'final',
            'const', 'static', 'extern', 'inline', 'volatile', 'mutable',
            'try', 'catch', 'throw', 'exception',
            'array', 'pointer', 'reference', 'loop', 'function', 'method',
            'constructor', 'destructor', 'inheritance', 'polymorphism',
            'operator', 'assignment', 'comparison', 'arithmetic',
            'fstream', 'ofstream', 'ifstream', 'file',
            'algorithm', 'sort', 'find', 'reverse', 'swap',
            'push_back', 'pop_back', 'size', 'empty', 'clear', 'insert', 'erase',
            'semicolon', 'brace', 'bracket', 'parenthesis'
        }

        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w in cpp_keywords or len(w) > 3]
        return list(set(keywords))


class RAGRetriever:
    """Retrieves relevant examples using keyword-based similarity."""

    def __init__(self, examples: List[Dict]):
        self.examples = examples

    def retrieve(self, query: str, top_k: int = 20) -> List[Dict]:
        """Retrieve top-k most relevant examples for the query."""
        query_keywords = self._extract_query_keywords(query)

        scored_examples = []
        for example in self.examples:
            score = self._calculate_relevance(query_keywords, example['keywords'])
            scored_examples.append((score, example))

        scored_examples.sort(reverse=True, key=lambda x: x[0])
        top_examples = [ex for score, ex in scored_examples[:top_k] if score > 0]

        if not top_examples:
            top_examples = [ex for ex in self.examples if ex['id'].startswith('S')][:top_k]

        return top_examples

    def _extract_query_keywords(self, query: str) -> List[str]:
        """Extract keywords from query."""
        patterns = {
            'for loop': ['for', 'loop', 'iteration'],
            'while loop': ['while', 'loop'],
            'if statement': ['if', 'condition', 'conditional'],
            'function': ['function', 'void', 'return'],
            'class': ['class', 'object', 'oop'],
            'array': ['array', 'bracket'],
            'pointer': ['pointer', 'new', 'delete'],
            'vector': ['vector', 'push_back', 'size'],
            'string': ['string', 'text'],
            'file': ['file', 'fstream', 'ifstream', 'ofstream'],
            'output': ['cout', 'output', 'print'],
            'input': ['cin', 'input', 'read'],
        }

        query_lower = query.lower()
        keywords = []

        for pattern, kws in patterns.items():
            if pattern in query_lower:
                keywords.extend(kws)

        words = re.findall(r'\b\w+\b', query_lower)
        keywords.extend([w for w in words if len(w) > 3])

        return list(set(keywords))

    def _calculate_relevance(self, query_keywords: List[str], example_keywords: List[str]) -> float:
        """Calculate relevance score between query and example."""
        if not query_keywords or not example_keywords:
            return 0.0

        matches = len(set(query_keywords) & set(example_keywords))
        total = len(set(query_keywords) | set(example_keywords))
        jaccard = matches / total if total > 0 else 0
        score = jaccard * (1 + matches * 0.1)

        return score


class QuestionValidator:
    """Validates and creates consistent fill-in-the-blank questions."""

    @staticmethod
    def parse_model_output(output: str) -> Optional[Dict]:
        """
        Parse model output to extract structured data.
        Expected format:
        CODE:
        [complete working code]

        TARGET:
        [exact token/phrase to replace]

        DISTRACTORS:
        1. option1
        2. option2
        3. option3
        """
        try:
            # Extract CODE section
            code_match = re.search(r'CODE:\s*```(?:cpp)?\s*(.*?)\s*```', output, re.DOTALL | re.IGNORECASE)
            if not code_match:
                code_match = re.search(r'CODE:\s*(.*?)(?=TARGET:|DISTRACTORS:|$)', output, re.DOTALL | re.IGNORECASE)

            if not code_match:
                return None

            code = code_match.group(1).strip()

            # Extract TARGET section
            target_match = re.search(r'TARGET:\s*([^\n]+)', output, re.IGNORECASE)
            if not target_match:
                return None

            target = target_match.group(1).strip()

            # Extract DISTRACTORS section
            distractors = []
            distractor_section = re.search(r'DISTRACTORS:\s*(.*?)(?=\n\n|$)', output, re.DOTALL | re.IGNORECASE)
            if distractor_section:
                distractor_text = distractor_section.group(1)
                # Parse numbered list
                for line in distractor_text.split('\n'):
                    match = re.match(r'\d+\.\s*(.+)', line.strip())
                    if match:
                        distractors.append(match.group(1).strip())

            if len(distractors) < 3:
                return None

            return {
                'code': code,
                'target': target,
                'distractors': distractors
            }

        except Exception as e:
            print(f"⚠️  Error parsing model output: {e}")
            return None

    @staticmethod
    def create_validated_question(parsed_data: Dict) -> Optional[Dict]:
        """
        Create a validated fill-in-the-blank question with guaranteed consistency.
        """
        code = parsed_data['code']
        target = parsed_data['target']
        distractors = parsed_data['distractors']

        # Find the target in the code
        if target not in code:
            print(f"⚠️  Target '{target}' not found in code. Trying case-insensitive match...")
            # Try case-insensitive match
            pattern = re.compile(re.escape(target), re.IGNORECASE)
            match = pattern.search(code)
            if match:
                target = match.group(0)  # Use the actual case from code
            else:
                print(f"❌ Target '{target}' not found in code at all!")
                return None

        # Count occurrences
        occurrences = code.count(target)
        if occurrences == 0:
            print(f"❌ No occurrences of '{target}' found")
            return None
        elif occurrences > 1:
            print(f"⚠️  Warning: '{target}' appears {occurrences} times - replacing first occurrence")

        # Create question code by replacing target with _____
        question_code = code.replace(target, "_____", 1)

        # Create options: correct answer + distractors
        # Shuffle to randomize correct answer position
        import random
        options = [target] + distractors[:3]  # Take only first 3 distractors

        # Randomly determine correct answer position
        correct_position = random.randint(0, min(3, len(options) - 1))

        # Create shuffled options with correct answer at correct_position
        shuffled_options = distractors[:correct_position] + [target] + distractors[correct_position:3]
        shuffled_options = shuffled_options[:4]  # Ensure exactly 4 options

        # Find the actual position of correct answer
        try:
            answer_position = shuffled_options.index(target) + 1  # 1-indexed
        except ValueError:
            # Fallback: put correct answer first
            shuffled_options = [target] + distractors[:3]
            answer_position = 1

        return {
            'code': code,
            'question_code': question_code,
            'options': shuffled_options,
            'answer': answer_position,
            'target': target
        }


class OllamaRAGClient:
    """Ollama client with RAG and validation capabilities."""

    def __init__(self, base_url: str, model: str, context_file: str, keep_alive: str = "60m"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.keep_alive = keep_alive

        print("🔍 Parsing context file...")
        parser = ContextParser(context_file)
        parser.parse()

        self.instructions = parser.instructions
        self.retriever = RAGRetriever(parser.examples)

        print(f"✅ RAG system initialized with {len(parser.examples)} examples")

    def estimate_tokens(self, text: str) -> int:
        """Rough estimate of token count."""
        return math.ceil(len(text) / AVG_CHARS_PER_TOKEN)

    def generate_validated_question(self, question: str, top_k: int = 20, verbose: bool = True) -> Optional[Dict]:
        """Generate a validated fill-in-the-blank question using two-stage approach."""

        if verbose:
            print(f"\n{'='*60}")
            print(f"🔎 Question: {question}")
            print(f"{'='*60}")

        # Retrieve relevant examples
        start_retrieval = time.time()
        relevant_examples = self.retriever.retrieve(question, top_k=top_k)
        retrieval_time = time.time() - start_retrieval

        if verbose:
            print(f"\n📚 Retrieved {len(relevant_examples)} relevant examples in {retrieval_time:.2f}s:")
            for i, ex in enumerate(relevant_examples[:5], 1):
                print(f"   {i}. {ex['id']} - {ex['description']}")
            if len(relevant_examples) > 5:
                print(f"   ... and {len(relevant_examples) - 5} more")

        # Build context
        context_parts = []

        if self.instructions:
            context_parts.append(self.instructions)
            if verbose:
                print(f"\n✅ Instructions included in context (~{self.estimate_tokens(self.instructions):,} tokens)")

        current_tokens = self.estimate_tokens(self.instructions if self.instructions else "")
        examples_added = []
        for example in relevant_examples:
            example_tokens = self.estimate_tokens(example['text'])
            if current_tokens + example_tokens > MAX_CONTEXT_TOKENS:
                break
            context_parts.append(example['text'])
            examples_added.append(example)
            current_tokens += example_tokens

        full_context = "\n\n".join(context_parts)

        if verbose:
            print(f"\n📊 Context composition:")
            print(f"   - Instructions: ~{self.estimate_tokens(self.instructions):,} tokens")
            print(f"   - Examples: {len(examples_added)} examples (~{current_tokens - self.estimate_tokens(self.instructions):,} tokens)")
            print(f"   - Total: ~{self.estimate_tokens(full_context):,} tokens")

        # Create STRUCTURED prompt that forces model to output in parseable format
        prompt = f"""You are an AI assistant that creates C++ programming questions.

IMPORTANT: Use ONLY modern C++ syntax (C++11 and later). DO NOT use old C-style code:
- Use new/delete or smart pointers (std::unique_ptr, std::shared_ptr) - NEVER malloc/free
- Use std::string - NEVER char* or char arrays for strings
- Use std::cout/std::cin - NEVER printf/scanf
- Use std::vector, std::array - prefer over raw arrays
- Use nullptr - NEVER NULL or 0 for pointers
- Use modern C++ features: auto, range-based for loops, etc.

Based on the following context and examples, create a fill-in-the-blank question.

Context:
{full_context}

Question: {question}

OUTPUT FORMAT (you MUST follow this exact format):

CODE:
```cpp
[Write complete, working C++ code here - no blanks, full working code]
```

TARGET:
[Write the EXACT token/word/phrase from the code above that should be replaced with _____]

DISTRACTORS:
1. [Wrong option 1 - similar but incorrect]
2. [Wrong option 2 - similar but incorrect]
3. [Wrong option 3 - similar but incorrect]

Remember:
- CODE must be complete and working
- TARGET must appear EXACTLY as written in CODE
- Generate ONLY modern C++ code, NO old C-style constructs"""

        # Generate response
        if verbose:
            print(f"\n🚀 Generating structured output...\n")

        start_time = time.time()
        response_text = ""

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "keep_alive": self.keep_alive
            }

            with requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=TIMEOUT,
            ) as r:
                r.raise_for_status()

                for line in r.iter_lines(decode_unicode=True):
                    if not line or not line.strip():
                        continue

                    try:
                        data = json.loads(line)

                        if "response" in data:
                            chunk = data["response"]
                            if verbose:
                                print(chunk, end='', flush=True)
                            response_text += chunk

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            print(f"\n❌ Error during generation: {e}")
            return None

        elapsed_time = time.time() - start_time

        if verbose:
            print(f"\n\n⏱️  Response time: {elapsed_time:.2f}s")

        # Parse and validate the model output
        if verbose:
            print(f"\n{'='*60}")
            print("🔍 Parsing and validating model output...")
            print(f"{'='*60}")

        parsed = QuestionValidator.parse_model_output(response_text)
        if not parsed:
            print("❌ Failed to parse model output")
            return None

        if verbose:
            print(f"✅ Parsed: code ({len(parsed['code'])} chars), target: '{parsed['target']}', {len(parsed['distractors'])} distractors")

        # Create validated question
        validated_question = QuestionValidator.create_validated_question(parsed)
        if not validated_question:
            print("❌ Failed to create validated question")
            return None

        if verbose:
            print(f"✅ Validated question created successfully!")
            print(f"   Answer position: {validated_question['answer']}")

        return validated_question


def main():
    parser = argparse.ArgumentParser(
        description='Ollama RAG Client with Validated Question Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python genai_ollama_client_with_rag_validated.py "Create a for loop example"
  python genai_ollama_client_with_rag_validated.py "How to use vectors in C++" --examples 30
        """
    )
    parser.add_argument('question', type=str, help='The question to ask')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - only show the final question')
    parser.add_argument('--context', '-c', type=str, default=CONTEXT_FILE, help='Path to context file')
    parser.add_argument('--examples', '-e', type=int, default=MAX_EXAMPLES_TO_RETRIEVE,
                       help='Number of examples to retrieve (default: 20)')

    args = parser.parse_args()

    verbose = not args.quiet

    if verbose:
        print("="*60)
        print("🧠 Ollama RAG Client with Validation")
        print("="*60)
        print("\nTwo-stage approach for guaranteed consistency:")
        print("1. Model generates: CODE + TARGET + DISTRACTORS")
        print("2. System validates and creates question\n")

    # Initialize RAG client
    try:
        client = OllamaRAGClient(
            base_url=OLLAMA_URL,
            model=GEN_MODEL,
            context_file=args.context,
            keep_alive=KEEP_ALIVE
        )
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print(f"❗ Please ensure '{args.context}' exists in the current directory.")
        sys.exit(1)

    # Generate validated question
    result = client.generate_validated_question(
        args.question,
        top_k=args.examples,
        verbose=verbose
    )

    if result:
        print(f"\n{'='*60}")
        print("✅ FINAL VALIDATED QUESTION")
        print(f"{'='*60}")
        print("\nComplete Code:")
        print("```cpp")
        print(result['code'])
        print("```")
        print("\nQuestion Code:")
        print("```cpp")
        print(result['question_code'])
        print("```")
        print("\nOptions:")
        for i, option in enumerate(result['options'], 1):
            marker = " ✓ CORRECT" if i == result['answer'] else ""
            print(f"{i}. {option}{marker}")
        print(f"\nAnswer: {result['answer']}")
        print(f"\nTarget replaced: '{result['target']}'")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
