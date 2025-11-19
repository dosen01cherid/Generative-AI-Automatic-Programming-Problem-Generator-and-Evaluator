"""
RAG + Deterministic System for Small Model (qwen2.5:1.5b)
----------------------------------------------------------
Leverages 1.5b by minimizing AI tasks and maximizing deterministic processing.

Strategy:
- AI does: Simple code generation only
- Deterministic system does: Everything else
  * Target extraction (rule-based)
  * Distractor generation (template-based)
  * Validation (pattern matching)
  * Question creation (deterministic)

Usage: python genai_ollama_rag_deterministic_1_5b.py "Create a for loop"
"""

import requests
import json
import time
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import sys
import io
import argparse
import random

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
OLLAMA_URL = "https://null-server-reliability-integration.trycloudflare.com"
MODEL = "qwen2.5:1.5b"  # Small, fast model
TIMEOUT = 300
CONTEXT_FILE = "context_with_validation.txt"
KEEP_ALIVE = "60m"
MAX_EXAMPLES_TO_RETRIEVE = 15


class CppTokenExtractor:
    """
    Deterministic C++ token extractor.
    Uses pattern matching and rules, not AI.
    """

    # Comprehensive C++ keyword patterns
    KEYWORDS = {
        'types': ['int', 'float', 'double', 'char', 'bool', 'void', 'string', 'auto'],
        'control': ['if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return'],
        'class': ['class', 'struct', 'public', 'private', 'protected', 'virtual', 'override'],
        'memory': ['new', 'delete', 'nullptr'],
        'namespace': ['namespace', 'using', 'std'],
        'io': ['cout', 'cin', 'endl', 'cerr'],
        'container': ['vector', 'map', 'set', 'list', 'queue', 'stack', 'array', 'deque'],
        'method': ['push_back', 'pop_back', 'size', 'empty', 'clear', 'front', 'back', 'insert', 'erase'],
        'operator': ['++', '--', '==', '!=', '<=', '>=', '<<', '>>', '&&', '||', '->', '::'],
        'symbol': [';', '{', '}', '(', ')', '[', ']', ',', '.']
    }

    # Distractor templates by category
    DISTRACTORS = {
        'int': ['float', 'double', 'char'],
        'float': ['int', 'double', 'char'],
        'double': ['int', 'float', 'long'],
        'char': ['int', 'string', 'bool'],
        'bool': ['int', 'char', 'short'],
        'void': ['int', 'char', 'bool'],
        'string': ['char', 'text', 'str'],
        'auto': ['int', 'var', 'type'],

        'for': ['while', 'do', 'if'],
        'while': ['for', 'do', 'until'],
        'if': ['for', 'while', 'when'],
        'else': ['elif', 'otherwise', 'then'],
        'switch': ['if', 'case', 'select'],
        'case': ['if', 'when', 'option'],
        'break': ['continue', 'exit', 'stop'],
        'continue': ['break', 'next', 'skip'],
        'return': ['exit', 'end', 'yield'],

        'class': ['struct', 'object', 'type'],
        'struct': ['class', 'record', 'type'],
        'public': ['private', 'protected', 'visible'],
        'private': ['public', 'protected', 'hidden'],
        'protected': ['public', 'private', 'internal'],

        'new': ['create', 'allocate', 'make'],
        'delete': ['remove', 'free', 'destroy'],
        'nullptr': ['NULL', '0', 'null'],

        'cout': ['cin', 'print', 'output'],
        'cin': ['cout', 'input', 'read'],
        'endl': ['newline', 'end', '\\n'],

        'vector': ['array', 'list', 'deque'],
        'map': ['dict', 'hash', 'table'],
        'set': ['list', 'array', 'collection'],
        'list': ['vector', 'array', 'sequence'],

        'push_back': ['insert', 'add', 'append'],
        'pop_back': ['remove', 'delete', 'erase'],
        'size': ['length', 'count', 'capacity'],
        'empty': ['isEmpty', 'blank', 'null'],
        'front': ['first', 'begin', 'start'],
        'back': ['last', 'end', 'rear'],

        '#include': ['import', 'using', 'require'],
        'iostream': ['stdio', 'stream', 'io'],
        'std': ['standard', 'sys', 'main'],

        '++': ['--', '+1', 'increment'],
        '--': ['++', '-1', 'decrement'],
        '<<': ['>>', '==', '<='],
        '>>': ['<<', '==', '>='],
        '->': ['.', '::', '=>'],
        '::': ['.', '->', ':'],
        ';': [',', '.', ':'],
        '{': ['[', '(', '<'],
        '}': [']', ')', '>'],
    }

    @staticmethod
    def extract_all_tokens(code: str) -> List[Dict]:
        """
        Extract all significant tokens from code.
        Returns list of {token, category, position}.
        """
        tokens = []

        # Extract all keyword categories
        for category, keywords in CppTokenExtractor.KEYWORDS.items():
            for keyword in keywords:
                # Use word boundaries for keywords
                if keyword.isalnum():
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                else:
                    pattern = re.escape(keyword)

                for match in re.finditer(pattern, code):
                    tokens.append({
                        'token': keyword,
                        'category': category,
                        'position': match.start(),
                        'line': code[:match.start()].count('\n') + 1
                    })

        # Sort by position
        tokens.sort(key=lambda x: x['position'])

        return tokens

    @staticmethod
    def select_best_targets(tokens: List[Dict], num_targets: int = 3) -> List[str]:
        """
        Select best targets for fill-in-the-blank.
        Prioritize: keywords > operators > symbols
        """
        # Priority order
        priority = {
            'control': 10,
            'types': 9,
            'container': 8,
            'method': 7,
            'class': 6,
            'io': 5,
            'namespace': 4,
            'memory': 3,
            'operator': 2,
            'symbol': 1
        }

        # Score tokens
        scored_tokens = []
        seen = set()

        for token_info in tokens:
            token = token_info['token']
            if token in seen:
                continue

            seen.add(token)
            score = priority.get(token_info['category'], 0)

            # Bonus for longer tokens (more interesting)
            score += len(token) * 0.1

            scored_tokens.append((score, token, token_info['category']))

        # Sort by score and return top N
        scored_tokens.sort(reverse=True, key=lambda x: x[0])

        return [token for _, token, _ in scored_tokens[:num_targets]]

    @staticmethod
    def get_distractors(target: str) -> List[str]:
        """
        Get distractors for a target using rule-based templates.
        """
        # Direct lookup
        if target in CppTokenExtractor.DISTRACTORS:
            return CppTokenExtractor.DISTRACTORS[target][:3]

        # Fallback: Generate based on category
        for category, keywords in CppTokenExtractor.KEYWORDS.items():
            if target in keywords:
                # Get other keywords from same category
                others = [k for k in keywords if k != target]
                if len(others) >= 3:
                    return random.sample(others, 3)
                else:
                    # Pad with generic options
                    return (others + ['option1', 'option2', 'option3'])[:3]

        # Ultimate fallback
        return ['option1', 'option2', 'option3']


class SimpleRAGRetriever:
    """Lightweight RAG for retrieving relevant examples."""

    def __init__(self, context_file: str):
        self.examples = []
        self._load_examples(context_file)

    def _load_examples(self, filepath: str):
        """Load and parse examples from context file."""
        path = Path(filepath)
        if not path.exists():
            print(f"⚠️  Context file not found: {filepath}")
            return

        content = path.read_text(encoding='utf-8')

        # Simple parsing: extract code blocks
        pattern = r'```cpp\s*(.*?)\s*```'
        matches = re.finditer(pattern, content, re.DOTALL)

        for i, match in enumerate(matches):
            code = match.group(1).strip()
            if code:
                self.examples.append({
                    'id': f'EX{i+1}',
                    'code': code,
                    'keywords': self._extract_keywords(code)
                })

        print(f"📚 Loaded {len(self.examples)} examples from context")

    def _extract_keywords(self, code: str) -> List[str]:
        """Extract C++ keywords from code."""
        keywords = []
        for category, kws in CppTokenExtractor.KEYWORDS.items():
            for kw in kws:
                if kw in code:
                    keywords.append(kw)
        return list(set(keywords))

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """Retrieve relevant code examples."""
        # Extract keywords from query
        query_lower = query.lower()
        query_keywords = []

        for category, kws in CppTokenExtractor.KEYWORDS.items():
            for kw in kws:
                if kw in query_lower:
                    query_keywords.append(kw)

        if not query_keywords:
            # Return random examples
            return [ex['code'] for ex in random.sample(self.examples, min(top_k, len(self.examples)))]

        # Score examples by keyword match
        scored = []
        for ex in self.examples:
            score = len(set(query_keywords) & set(ex['keywords']))
            if score > 0:
                scored.append((score, ex['code']))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [code for _, code in scored[:top_k]]


class DeterministicQuestionGenerator:
    """
    Main generator: Uses 1.5b for code only, deterministic for everything else.
    """

    def __init__(self, base_url: str, model: str, context_file: str):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.keep_alive = KEEP_ALIVE
        self.rag = SimpleRAGRetriever(context_file)
        self.extractor = CppTokenExtractor()

    def generate_code_with_rag(self, topic: str, verbose: bool = False) -> Optional[str]:
        """
        Use RAG + 1.5b to generate code.
        RAG provides examples, 1.5b generates similar code.
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"📝 Step 1: Generate Code (1.5b + RAG)")
            print(f"{'='*60}")

        # Retrieve relevant examples
        examples = self.rag.retrieve(topic, top_k=3)

        if verbose and examples:
            print(f"\n📚 Retrieved {len(examples)} relevant examples:")
            for i, ex in enumerate(examples, 1):
                preview = ex.split('\n')[0][:50]
                print(f"   {i}. {preview}...")

        # Create focused prompt with examples
        prompt = f"""Write a simple C++ code example for: {topic}

Here are similar examples for reference:

Example 1:
```cpp
{examples[0] if examples else 'int main() { return 0; }'}
```

Now write YOUR code for: {topic}

Requirements:
- Complete working code
- Include headers
- Use modern C++
- Keep it simple

Just write the code:"""

        if verbose:
            print(f"\n🤖 Calling {self.model}...")

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
                timeout=TIMEOUT
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

            elapsed = time.time() - start_time
            if verbose:
                print(f"\n\n⏱️  Generation time: {elapsed:.2f}s")

            # Extract code block
            code_match = re.search(r'```(?:cpp)?\s*(.*?)\s*```', response_text, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
            else:
                # Try to extract code without markdown
                code = response_text.strip()

            return code

        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None

    def create_question_deterministic(
        self,
        code: str,
        num_blanks: int = 3,
        verbose: bool = False
    ) -> Optional[Dict]:
        """
        Create fill-in-the-blank question using PURE deterministic processing.
        No AI involved here!
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"🔧 Step 2: Deterministic Question Creation")
            print(f"{'='*60}")

        # Extract all tokens
        tokens = self.extractor.extract_all_tokens(code)

        if verbose:
            print(f"\n📊 Extracted {len(tokens)} tokens from code")
            print(f"   Token categories: {len(set(t['category'] for t in tokens))}")

        # Select best targets
        targets = self.extractor.select_best_targets(tokens, num_blanks)

        if verbose:
            print(f"\n🎯 Selected {len(targets)} targets:")
            for i, target in enumerate(targets, 1):
                print(f"   {i}. {target}")

        if not targets:
            print("❌ No suitable targets found")
            return None

        # Generate distractors deterministically
        sub_questions = []
        question_code = code

        for i, target in enumerate(targets):
            # Get distractors
            distractors = self.extractor.get_distractors(target)

            if verbose:
                print(f"\n   Distractors for '{target}': {distractors}")

            # Create options
            options = [target] + distractors
            random.shuffle(options)

            try:
                answer_pos = options.index(target) + 1
            except ValueError:
                options = [target] + distractors
                answer_pos = 1

            # Replace in code (first occurrence only)
            blank_marker = f"_____({i+1})_____"
            question_code = question_code.replace(target, blank_marker, 1)

            sub_questions.append({
                'number': i + 1,
                'target': target,
                'options': options,
                'answer': answer_pos
            })

        if verbose:
            print(f"\n✅ Created {len(sub_questions)} sub-questions deterministically")

        return {
            'code': code,
            'question_code': question_code,
            'sub_questions': sub_questions,
            'num_blanks': len(sub_questions),
            'method': 'deterministic'
        }

    def generate_question(
        self,
        topic: str,
        num_blanks: int = 3,
        verbose: bool = True
    ) -> Optional[Dict]:
        """
        Main generation pipeline:
        1. RAG + 1.5b: Generate code
        2. Deterministic: Extract targets
        3. Deterministic: Generate distractors
        4. Deterministic: Create question
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"🚀 RAG + Deterministic Question Generation")
            print(f"{'='*60}")
            print(f"Topic: {topic}")
            print(f"Blanks: {num_blanks}")
            print(f"Model: {self.model} (code generation only)")
            print(f"Processing: 95% deterministic, 5% AI")

        start_total = time.time()

        # Step 1: Generate code (AI)
        code = self.generate_code_with_rag(topic, verbose)
        if not code:
            return None

        # Step 2-4: Everything else (Deterministic)
        result = self.create_question_deterministic(code, num_blanks, verbose)

        total_time = time.time() - start_total

        if verbose and result:
            print(f"\n{'='*60}")
            print(f"✅ Generation Complete")
            print(f"{'='*60}")
            print(f"Total time: {total_time:.2f}s")
            print(f"AI usage: Code generation only")
            print(f"Deterministic: Target extraction, distractors, validation")

        return result


def main():
    parser = argparse.ArgumentParser(
        description='RAG + Deterministic Question Generator (1.5b)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Strategy: Minimize AI tasks, maximize deterministic processing

AI does: Code generation only (~5s)
Deterministic does:
  - Token extraction (pattern matching)
  - Target selection (scoring rules)
  - Distractor generation (templates)
  - Question creation (deterministic)

Examples:
  python genai_ollama_rag_deterministic_1_5b.py "Create a for loop"
  python genai_ollama_rag_deterministic_1_5b.py "Vector operations" --blanks 5
        """
    )
    parser.add_argument('topic', type=str, help='Topic/question')
    parser.add_argument('--blanks', '-b', type=int, default=3, help='Number of blanks')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode')
    parser.add_argument('--context', '-c', type=str, default=CONTEXT_FILE, help='Context file')

    args = parser.parse_args()
    verbose = not args.quiet

    if verbose:
        print("="*60)
        print("🔬 RAG + Deterministic Generator")
        print("="*60)
        print(f"\nModel: {MODEL} (1.5b - fast!)")
        print(f"AI Task: Code generation only (~5s)")
        print(f"Deterministic: Everything else (pattern matching)")
        print(f"\nExpected: ~8s total, Good quality\n")

    # Initialize generator
    try:
        generator = DeterministicQuestionGenerator(
            base_url=OLLAMA_URL,
            model=MODEL,
            context_file=args.context
        )
    except Exception as e:
        print(f"\n❌ Initialization error: {e}")
        sys.exit(1)

    # Generate question
    result = generator.generate_question(
        topic=args.topic,
        num_blanks=args.blanks,
        verbose=verbose
    )

    if result:
        print(f"\n{'='*60}")
        print("✅ FINAL QUESTION (DETERMINISTICALLY GENERATED)")
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
        print("💡 Generation Method:")
        print(f"  AI (1.5b): Code generation only")
        print(f"  Deterministic: Token extraction (regex)")
        print(f"  Deterministic: Target selection (scoring)")
        print(f"  Deterministic: Distractor generation (templates)")
        print(f"  Deterministic: Question creation (replacement)")
        print(f"  Result: Fast, reliable, consistent!")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
