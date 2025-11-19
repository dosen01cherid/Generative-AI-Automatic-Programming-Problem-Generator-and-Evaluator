"""
Ollama RAG Client with Validated Multi-Blank Question Generation
-----------------------------------------------------------------
Generates questions with multiple blanks, each with its own numbered question
and multiple choice options. Uses deterministic replacement for guaranteed consistency.

Usage: python genai_ollama_client_with_rag_validated_multi_blank.py "Your question here"
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
import random

# Fix encoding for Windows console to support emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# =======================================================
# 🔧 CONFIGURATION
# =======================================================
OLLAMA_URL = "https://soundtrack-birds-walk-likelihood.trycloudflare.com"
GEN_MODEL = "qwen2.5:14b"
TIMEOUT = 600
CONTEXT_FILE = "context_with_validation.txt"
MODEL_CONTEXT_SIZE = 128_000  # in tokens
AVG_CHARS_PER_TOKEN = 4.0
KEEP_ALIVE = "60m"

# RAG Configuration
MAX_EXAMPLES_TO_RETRIEVE = 20
MAX_CONTEXT_TOKENS = 30_000
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
            r'HOW TO CREATE ACCURATE FILL-IN-THE-BLANK QUESTIONS.*?(?=FILL-IN-THE-BLANK EXAMPLES)',
            content,
            re.DOTALL
        )
        if instructions_match:
            self.instructions = instructions_match.group(0).strip()

        # Parse individual examples
        example_pattern = r'------------------\s*Fill-in-the-Blank Question Example ([^\(]+)\(([^\)]+)\)\s*------------------\s*(.*?)(?=------------------\s*Fill-in-the-Blank Question Example|END OF EXAMPLES|$)'

        matches = re.finditer(example_pattern, content, re.DOTALL)

        for match in matches:
            example_id = match.group(1).strip()
            description = match.group(2).strip()
            full_text = match.group(3).strip()

            keywords = self._extract_keywords(description + " " + full_text)

            example = {
                'id': example_id,
                'description': description,
                'text': match.group(0),
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


class MultiBlankValidator:
    """Validates and creates consistent multi-blank fill-in-the-blank questions."""

    @staticmethod
    def parse_model_output(output: str) -> Optional[Dict]:
        """
        Parse model output to extract structured data for multi-blank questions.
        Expected format:
        CODE:
        [complete working code]

        TARGETS:
        1. target1 - description
        2. target2 - description
        3. target3 - description

        DISTRACTORS:
        For Target 1:
        1. distractor1
        2. distractor2
        3. distractor3

        For Target 2:
        1. distractor1
        2. distractor2
        3. distractor3
        """
        try:
            # Extract CODE section
            code_match = re.search(r'CODE:\s*```(?:cpp)?\s*(.*?)\s*```', output, re.DOTALL | re.IGNORECASE)
            if not code_match:
                code_match = re.search(r'CODE:\s*(.*?)(?=TARGETS?:|DISTRACTORS?:|$)', output, re.DOTALL | re.IGNORECASE)

            if not code_match:
                return None

            code = code_match.group(1).strip()

            # Extract TARGETS section
            targets_match = re.search(r'TARGETS?:\s*(.*?)(?=DISTRACTORS?:|$)', output, re.DOTALL | re.IGNORECASE)
            if not targets_match:
                return None

            targets_text = targets_match.group(1)
            targets = []

            # Parse numbered targets
            for line in targets_text.split('\n'):
                match = re.match(r'\d+\.\s*([^\-\n]+)', line.strip())
                if match:
                    target = match.group(1).strip()
                    targets.append(target)

            if not targets:
                return None

            # Extract DISTRACTORS section
            distractors_match = re.search(r'DISTRACTORS?:\s*(.*?)$', output, re.DOTALL | re.IGNORECASE)
            if not distractors_match:
                return None

            distractors_text = distractors_match.group(1)
            all_distractors = []

            # Parse distractors for each target
            # Pattern: "For Target N:" followed by numbered list
            target_sections = re.split(r'For Target \d+:', distractors_text, flags=re.IGNORECASE)

            for section in target_sections[1:]:  # Skip first empty split
                target_distractors = []
                for line in section.split('\n'):
                    match = re.match(r'\d+\.\s*(.+)', line.strip())
                    if match:
                        target_distractors.append(match.group(1).strip())

                if target_distractors:
                    all_distractors.append(target_distractors[:3])  # Take first 3

            # Ensure we have distractors for all targets
            while len(all_distractors) < len(targets):
                all_distractors.append([])

            return {
                'code': code,
                'targets': targets,
                'distractors': all_distractors
            }

        except Exception as e:
            print(f"⚠️  Error parsing model output: {e}")
            return None

    @staticmethod
    def create_validated_multi_blank_question(parsed_data: Dict) -> Optional[Dict]:
        """
        Create validated multi-blank question with guaranteed consistency.
        """
        code = parsed_data['code']
        targets = parsed_data['targets']
        all_distractors = parsed_data['distractors']

        # Validate all targets exist in code
        validated_targets = []
        validated_distractors = []

        for i, (target, distractors) in enumerate(zip(targets, all_distractors)):
            # Check if target exists in code
            if target not in code:
                print(f"⚠️  Target {i+1} '{target}' not found in code. Trying case-insensitive...")
                pattern = re.compile(re.escape(target), re.IGNORECASE)
                match = pattern.search(code)
                if match:
                    target = match.group(0)
                else:
                    print(f"❌ Target {i+1} '{target}' not found in code!")
                    continue

            validated_targets.append(target)

            # Ensure we have at least 3 distractors
            if len(distractors) < 3:
                print(f"⚠️  Target {i+1} has only {len(distractors)} distractors, need 3")
                # Pad with generic options
                while len(distractors) < 3:
                    distractors.append(f"option{len(distractors)+1}")

            validated_distractors.append(distractors[:3])

        if not validated_targets:
            print("❌ No valid targets found!")
            return None

        # Create question code with numbered blanks
        question_code = code
        blank_positions = []

        # Replace each target with numbered blank
        for i, target in enumerate(validated_targets):
            blank_marker = f"_____({i+1})_____"

            # Find position of target in question_code
            if target in question_code:
                pos = question_code.find(target)
                blank_positions.append(pos)
                question_code = question_code.replace(target, blank_marker, 1)
            else:
                print(f"⚠️  Warning: Target '{target}' not found during replacement")

        # Create sub-questions with options
        sub_questions = []

        for i, (target, distractors) in enumerate(zip(validated_targets, validated_distractors)):
            # Create options: correct answer + distractors
            options = [target] + distractors

            # Shuffle options
            shuffled_options = options.copy()
            random.shuffle(shuffled_options)

            # Find correct answer position
            try:
                answer_position = shuffled_options.index(target) + 1  # 1-indexed
            except ValueError:
                shuffled_options = [target] + distractors
                answer_position = 1

            sub_questions.append({
                'number': i + 1,
                'target': target,
                'options': shuffled_options,
                'answer': answer_position
            })

        return {
            'code': code,
            'question_code': question_code,
            'sub_questions': sub_questions,
            'num_blanks': len(validated_targets)
        }


class OllamaRAGClient:
    """Ollama client with RAG and multi-blank validation capabilities."""

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

    def generate_validated_multi_blank_question(
        self,
        question: str,
        num_blanks: int = 3,
        top_k: int = 20,
        verbose: bool = True
    ) -> Optional[Dict]:
        """Generate a validated multi-blank question."""

        if verbose:
            print(f"\n{'='*60}")
            print(f"🔎 Question: {question}")
            print(f"📝 Requested blanks: {num_blanks}")
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
            print(f"   - Examples: {len(examples_added)} (~{current_tokens - self.estimate_tokens(self.instructions):,} tokens)")
            print(f"   - Total: ~{self.estimate_tokens(full_context):,} tokens")

        # Create STRUCTURED prompt for multi-blank questions
        prompt = f"""You are an AI assistant that creates C++ programming questions.

IMPORTANT: Use ONLY modern C++ syntax (C++11 and later). DO NOT use old C-style code.

Based on the context and examples, create a fill-in-the-blank question with {num_blanks} blanks.

Context:
{full_context}

Question: {question}

OUTPUT FORMAT (you MUST follow this exact format):

CODE:
```cpp
[Write complete, working C++ code here - no blanks]
```

TARGETS:
1. [First token/phrase to replace]
2. [Second token/phrase to replace]
3. [Third token/phrase to replace]
{f'... up to {num_blanks} targets' if num_blanks > 3 else ''}

DISTRACTORS:
For Target 1:
1. [Wrong option 1]
2. [Wrong option 2]
3. [Wrong option 3]

For Target 2:
1. [Wrong option 1]
2. [Wrong option 2]
3. [Wrong option 3]

For Target 3:
1. [Wrong option 1]
2. [Wrong option 2]
3. [Wrong option 3]

{f'... provide distractors for all {num_blanks} targets' if num_blanks > 3 else ''}

Remember:
- CODE must be complete and working
- Each TARGET must appear EXACTLY in CODE
- Each TARGET gets 3 DISTRACTORS
- Generate ONLY modern C++ code"""

        # Generate response
        if verbose:
            print(f"\n🚀 Generating multi-blank question...\n")

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

        # Parse and validate
        if verbose:
            print(f"\n{'='*60}")
            print("🔍 Parsing and validating model output...")
            print(f"{'='*60}")

        parsed = MultiBlankValidator.parse_model_output(response_text)
        if not parsed:
            print("❌ Failed to parse model output")
            return None

        if verbose:
            print(f"✅ Parsed: {len(parsed['targets'])} targets, {len(parsed['distractors'])} distractor sets")

        # Create validated question
        validated_question = MultiBlankValidator.create_validated_multi_blank_question(parsed)
        if not validated_question:
            print("❌ Failed to create validated question")
            return None

        if verbose:
            print(f"✅ Multi-blank question created successfully!")
            print(f"   Number of blanks: {validated_question['num_blanks']}")

        return validated_question


def main():
    parser = argparse.ArgumentParser(
        description='Ollama RAG Client with Validated Multi-Blank Question Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python genai_ollama_client_with_rag_validated_multi_blank.py "Create a for loop"
  python genai_ollama_client_with_rag_validated_multi_blank.py "Vector operations" --blanks 5
        """
    )
    parser.add_argument('question', type=str, help='The question to ask')
    parser.add_argument('--blanks', '-b', type=int, default=3, help='Number of blanks (default: 3)')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode')
    parser.add_argument('--context', '-c', type=str, default=CONTEXT_FILE, help='Path to context file')
    parser.add_argument('--examples', '-e', type=int, default=MAX_EXAMPLES_TO_RETRIEVE,
                       help='Number of examples to retrieve')

    args = parser.parse_args()

    verbose = not args.quiet

    if verbose:
        print("="*60)
        print("🧠 Ollama RAG Client - Multi-Blank Questions")
        print("="*60)
        print("\nGenerates questions with multiple blanks,")
        print("each with numbered sub-questions and options.\n")

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
        sys.exit(1)

    # Generate validated multi-blank question
    result = client.generate_validated_multi_blank_question(
        args.question,
        num_blanks=args.blanks,
        top_k=args.examples,
        verbose=verbose
    )

    if result:
        print(f"\n{'='*60}")
        print("✅ FINAL VALIDATED MULTI-BLANK QUESTION")
        print(f"{'='*60}")
        print("\nComplete Code:")
        print("```cpp")
        print(result['code'])
        print("```")
        print("\nQuestion Code:")
        print("```cpp")
        print(result['question_code'])
        print("```")
        print(f"\nNumber of Blanks: {result['num_blanks']}")
        print("\nSub-Questions:")
        for sq in result['sub_questions']:
            print(f"\n--- Question {sq['number']} (Fill in blank {sq['number']}) ---")
            print("Options:")
            for i, option in enumerate(sq['options'], 1):
                marker = " ✓ CORRECT" if i == sq['answer'] else ""
                print(f"  {i}. {option}{marker}")
            print(f"Answer: {sq['answer']}")
            print(f"Target: '{sq['target']}'")
        print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
