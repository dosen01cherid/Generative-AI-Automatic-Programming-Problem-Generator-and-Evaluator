"""
Ollama RAG Client - Retrieval-Augmented Generation
----------------------------------------------------
This client uses RAG to dynamically retrieve relevant examples from context.txt
instead of loading the entire context file. This keeps the context fresh and
focused on the most relevant examples for each question.

Usage: python genai_ollama_client_with_rag.py "Your question here"
"""

import requests
import json
import math
import time
import re
from pathlib import Path
from typing import List, Dict, Tuple
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
CONTEXT_FILE = "context.txt"
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
        # Pattern: Fill-in-the-Blank Question Example [ID] ([Description])
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
        # Common C++ keywords and concepts
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

        # Convert to lowercase and split
        words = re.findall(r'\b\w+\b', text.lower())

        # Filter for C++ keywords and important terms
        keywords = [w for w in words if w in cpp_keywords or len(w) > 3]

        # Return unique keywords
        return list(set(keywords))


class RAGRetriever:
    """Retrieves relevant examples using keyword-based similarity."""

    def __init__(self, examples: List[Dict]):
        self.examples = examples

    def retrieve(self, query: str, top_k: int = 20) -> List[Dict]:
        """Retrieve top-k most relevant examples for the query."""
        # Extract keywords from query
        query_keywords = self._extract_query_keywords(query)

        # Calculate relevance scores
        scored_examples = []
        for example in self.examples:
            score = self._calculate_relevance(query_keywords, example['keywords'])
            scored_examples.append((score, example))

        # Sort by score (descending) and return top-k
        scored_examples.sort(reverse=True, key=lambda x: x[0])

        # Get top-k examples
        top_examples = [ex for score, ex in scored_examples[:top_k] if score > 0]

        # If no matches, return some simple examples (S series)
        if not top_examples:
            top_examples = [ex for ex in self.examples if ex['id'].startswith('S')][:top_k]

        return top_examples

    def _extract_query_keywords(self, query: str) -> List[str]:
        """Extract keywords from query."""
        # Common question patterns
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

        # Check for pattern matches
        for pattern, kws in patterns.items():
            if pattern in query_lower:
                keywords.extend(kws)

        # Extract words from query
        words = re.findall(r'\b\w+\b', query_lower)
        keywords.extend([w for w in words if len(w) > 3])

        return list(set(keywords))

    def _calculate_relevance(self, query_keywords: List[str], example_keywords: List[str]) -> float:
        """Calculate relevance score between query and example."""
        if not query_keywords or not example_keywords:
            return 0.0

        # Count matching keywords
        matches = len(set(query_keywords) & set(example_keywords))

        # Calculate score (Jaccard similarity with boost for matches)
        total = len(set(query_keywords) | set(example_keywords))
        jaccard = matches / total if total > 0 else 0

        # Boost score by number of matches
        score = jaccard * (1 + matches * 0.1)

        return score


class OllamaRAGClient:
    """Ollama client with RAG capabilities."""

    def __init__(self, base_url: str, model: str, context_file: str, keep_alive: str = "60m"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.keep_alive = keep_alive

        # Parse context file
        print("🔍 Parsing context file...")
        parser = ContextParser(context_file)
        parser.parse()

        self.instructions = parser.instructions
        self.retriever = RAGRetriever(parser.examples)

        print(f"✅ RAG system initialized with {len(parser.examples)} examples")

    def estimate_tokens(self, text: str) -> int:
        """Rough estimate of token count."""
        return math.ceil(len(text) / AVG_CHARS_PER_TOKEN)

    def generate_with_rag(self, question: str, top_k: int = 20, verbose: bool = True) -> Tuple[str, float, List[str]]:
        """Generate response using RAG to retrieve relevant context."""

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

        # Build context from retrieved examples
        context_parts = []

        # ALWAYS include detailed instructions (MANDATORY)
        if self.instructions:
            context_parts.append(self.instructions)
            if verbose:
                print(f"\n✅ Instructions included in context (~{self.estimate_tokens(self.instructions):,} tokens)")
        else:
            print("⚠️  WARNING: No instructions found!")

        # Add retrieved examples
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

        # Save retrieved context to file
        context_filename = f"retrieved_context_{int(time.time())}.txt"
        try:
            with open(context_filename, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("RETRIEVED CONTEXT FOR QUESTION\n")
                f.write("="*60 + "\n\n")
                f.write(f"Question: {question}\n\n")
                f.write("="*60 + "\n")
                f.write("CONTEXT SENT TO LLM\n")
                f.write("="*60 + "\n\n")
                f.write(full_context)
                f.write("\n\n" + "="*60 + "\n")
                f.write(f"Retrieved {len(examples_added)} examples:\n")
                for i, ex in enumerate(examples_added, 1):
                    f.write(f"{i}. {ex['id']} - {ex['description']}\n")
            if verbose:
                print(f"💾 Context saved to: {context_filename}")
        except Exception as e:
            if verbose:
                print(f"⚠️  Could not save context: {e}")

        # Create prompt with context
        prompt = f"""You are an AI assistant that creates C++ programming questions.

IMPORTANT: Use ONLY modern C++ syntax (C++11 and later). DO NOT use old C-style code:
- Use new/delete or smart pointers (std::unique_ptr, std::shared_ptr) - NEVER malloc/free
- Use std::string - NEVER char* or char arrays for strings
- Use std::cout/std::cin - NEVER printf/scanf
- Use std::vector, std::array - prefer over raw arrays
- Use nullptr - NEVER NULL or 0 for pointers
- Use modern C++ features: auto, range-based for loops, etc.

Based on the following context and examples, please answer the question.

Context:
{full_context}

Question: {question}

Please provide a detailed and accurate response following the format shown in the examples.
Remember: Generate ONLY modern C++ code, NO old C-style constructs."""

        # Generate response
        if verbose:
            print(f"\n🚀 Generating response...\n")

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
            return "", 0, []

        elapsed_time = time.time() - start_time

        if verbose:
            print(f"\n\n⏱️  Response time: {elapsed_time:.2f}s")
            print(f"📈 Retrieval time: {retrieval_time:.2f}s")
            print(f"🔢 Total examples in context: {len([ex for ex in relevant_examples if self.estimate_tokens(ex['text']) <= current_tokens])}")

        # Get example IDs that were used
        used_example_ids = [ex['id'] for ex in relevant_examples[:len(context_parts)-1]]

        return response_text.strip(), elapsed_time, used_example_ids


def main():
    parser = argparse.ArgumentParser(
        description='Ollama RAG Client - Retrieval-Augmented Generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python genai_ollama_client_with_rag.py "Create a for loop example"
  python genai_ollama_client_with_rag.py "How to use vectors in C++" --examples 30
  python genai_ollama_client_with_rag.py "Create class example" --quiet
        """
    )
    parser.add_argument('question', type=str, help='The question to ask')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - only show the answer')
    parser.add_argument('--context', '-c', type=str, default=CONTEXT_FILE, help='Path to context file')
    parser.add_argument('--examples', '-e', type=int, default=MAX_EXAMPLES_TO_RETRIEVE,
                       help='Number of examples to retrieve (default: 20)')

    args = parser.parse_args()

    verbose = not args.quiet

    if verbose:
        print("="*60)
        print("🧠 Ollama RAG Client")
        print("="*60)
        print("\nThis client uses RAG to retrieve only relevant examples")
        print("from context.txt, keeping the context fresh and focused.\n")

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

    # Generate response with RAG
    answer, response_time, used_examples = client.generate_with_rag(
        args.question,
        top_k=args.examples,
        verbose=verbose
    )

    if args.quiet and answer:
        print(answer)

    if verbose and answer:
        print(f"\n{'='*60}")
        print("✅ Response generated successfully")
        print(f"{'='*60}")
        if used_examples:
            print(f"\n📝 Examples used: {', '.join(used_examples[:10])}")
            if len(used_examples) > 10:
                print(f"   ... and {len(used_examples) - 10} more")


if __name__ == "__main__":
    main()
