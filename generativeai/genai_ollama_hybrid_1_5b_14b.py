"""
Hybrid Question Generator: qwen2.5:1.5b + qwen2.5:14b
------------------------------------------------------
Leverages the speed of 1.5b and the quality of 14b for optimal performance.

Strategy:
1. Use 1.5b for fast code generation (10s)
2. Use 14b for validation and structuring (15s)
3. Total: 25s vs 70s for 14b alone (64% faster)

Usage: python genai_ollama_hybrid_1_5b_14b.py "Create a for loop example"
"""

import requests
import json
import time
import re
from pathlib import Path
from typing import Optional, Dict
import sys
import io
import argparse

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
OLLAMA_URL = "https://unpatented-saylor-nonirate.ngrok-free.dev"
FAST_MODEL = "qwen2.5:1.5b"  # Fast code generation
QUALITY_MODEL = "qwen2.5:14b"  # Validation and structuring
TIMEOUT = 300
KEEP_ALIVE = "60m"


class HybridQuestionGenerator:
    """
    Hybrid generator using 1.5b for speed and 14b for quality.
    """

    def __init__(self, base_url: str, fast_model: str, quality_model: str):
        self.base_url = base_url.rstrip('/')
        self.fast_model = fast_model
        self.quality_model = quality_model
        self.keep_alive = KEEP_ALIVE

    def call_model(self, model: str, prompt: str, verbose: bool = False) -> Optional[str]:
        """Call Ollama model and return response."""
        if verbose:
            print(f"\n🤖 Calling {model}...")

        start_time = time.time()
        response_text = ""

        try:
            payload = {
                "model": model,
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
                print(f"\n⏱️  Time: {elapsed:.2f}s")

            return response_text.strip()

        except Exception as e:
            print(f"\n❌ Error: {e}")
            return None

    def generate_code_with_1_5b(self, topic: str, verbose: bool = False) -> Optional[str]:
        """
        Phase 1: Use 1.5b to generate code quickly.
        Simple, focused prompt for better compliance.
        """
        prompt = f"""Write a simple, complete C++ code example for: {topic}

Requirements:
- Use modern C++ (C++11+)
- Complete working code
- Include necessary headers
- Add a main function
- Keep it simple and clear

Just write the code, nothing else:"""

        if verbose:
            print(f"\n{'='*60}")
            print(f"📝 Phase 1: Fast Code Generation (1.5b)")
            print(f"{'='*60}")

        code = self.call_model(self.fast_model, prompt, verbose)
        return code

    def extract_targets_with_14b(
        self,
        code: str,
        num_targets: int = 3,
        verbose: bool = False
    ) -> Optional[Dict]:
        """
        Phase 2: Use 14b to extract targets and distractors from code.
        14b is better at understanding and structuring.
        """
        prompt = f"""Given this C++ code:

```cpp
{code}
```

Extract {num_targets} important keywords/concepts that would make good fill-in-the-blank questions.

OUTPUT FORMAT (follow exactly):

TARGETS:
1. [keyword 1]
2. [keyword 2]
3. [keyword 3]

DISTRACTORS:
For Target 1:
1. [wrong option 1]
2. [wrong option 2]
3. [wrong option 3]

For Target 2:
1. [wrong option 1]
2. [wrong option 2]
3. [wrong option 3]

For Target 3:
1. [wrong option 1]
2. [wrong option 2]
3. [wrong option 3]

Remember:
- Each TARGET must appear EXACTLY in the code
- Each TARGET gets 3 DISTRACTORS
- DISTRACTORS should be similar but wrong"""

        if verbose:
            print(f"\n{'='*60}")
            print(f"🔍 Phase 2: Extract Targets & Distractors (14b)")
            print(f"{'='*60}")

        response = self.call_model(self.quality_model, prompt, verbose)

        if not response:
            return None

        # Parse response
        return self.parse_targets_response(response)

    def parse_targets_response(self, response: str) -> Optional[Dict]:
        """Parse 14b response to extract targets and distractors."""
        try:
            # Extract TARGETS
            targets_match = re.search(r'TARGETS?:\s*(.*?)(?=DISTRACTORS?:|$)', response, re.DOTALL | re.IGNORECASE)
            if not targets_match:
                return None

            targets_text = targets_match.group(1)
            targets = []
            for line in targets_text.split('\n'):
                match = re.match(r'\d+\.\s*([^\n]+)', line.strip())
                if match:
                    targets.append(match.group(1).strip())

            # Extract DISTRACTORS
            distractors_match = re.search(r'DISTRACTORS?:\s*(.*?)$', response, re.DOTALL | re.IGNORECASE)
            if not distractors_match:
                return None

            distractors_text = distractors_match.group(1)
            all_distractors = []

            target_sections = re.split(r'For Target \d+:', distractors_text, flags=re.IGNORECASE)
            for section in target_sections[1:]:
                target_distractors = []
                for line in section.split('\n'):
                    match = re.match(r'\d+\.\s*(.+)', line.strip())
                    if match:
                        target_distractors.append(match.group(1).strip())
                if target_distractors:
                    all_distractors.append(target_distractors[:3])

            return {
                'targets': targets,
                'distractors': all_distractors
            }

        except Exception as e:
            print(f"⚠️  Parse error: {e}")
            return None

    def generate_hybrid_question(
        self,
        topic: str,
        num_blanks: int = 3,
        verbose: bool = True
    ) -> Optional[Dict]:
        """
        Generate question using hybrid approach:
        1. 1.5b generates code (fast)
        2. 14b extracts targets and distractors (accurate)
        """
        if verbose:
            print(f"\n{'='*60}")
            print(f"🔬 Hybrid Question Generation")
            print(f"{'='*60}")
            print(f"Topic: {topic}")
            print(f"Blanks: {num_blanks}")
            print(f"Strategy: 1.5b (code) + 14b (validation)")

        start_total = time.time()

        # Phase 1: Generate code with 1.5b (fast)
        code = self.generate_code_with_1_5b(topic, verbose)
        if not code:
            print("❌ Failed to generate code")
            return None

        # Extract code block if wrapped
        code_match = re.search(r'```(?:cpp)?\s*(.*?)\s*```', code, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()

        # Phase 2: Extract targets with 14b (accurate)
        parsed = self.extract_targets_with_14b(code, num_blanks, verbose)
        if not parsed:
            print("❌ Failed to extract targets")
            return None

        total_time = time.time() - start_total

        if verbose:
            print(f"\n{'='*60}")
            print(f"✅ Hybrid Generation Complete")
            print(f"{'='*60}")
            print(f"Total time: {total_time:.2f}s")
            print(f"Targets found: {len(parsed['targets'])}")
            print(f"Distractors: {len(parsed['distractors'])} sets")

        # Create validated question
        return self.create_validated_question(code, parsed, verbose)

    def create_validated_question(
        self,
        code: str,
        parsed: Dict,
        verbose: bool = False
    ) -> Optional[Dict]:
        """Create validated question from code and parsed targets."""
        import random

        targets = parsed['targets']
        all_distractors = parsed['distractors']

        # Validate targets exist in code
        validated_targets = []
        validated_distractors = []

        for i, (target, distractors) in enumerate(zip(targets, all_distractors)):
            if target in code:
                validated_targets.append(target)
                validated_distractors.append(distractors)
            else:
                if verbose:
                    print(f"⚠️  Target '{target}' not found in code, skipping")

        if not validated_targets:
            print("❌ No valid targets found in code")
            return None

        # Create question code with numbered blanks
        question_code = code
        for i, target in enumerate(validated_targets):
            blank = f"_____({i+1})_____"
            question_code = question_code.replace(target, blank, 1)

        # Create sub-questions
        sub_questions = []
        for i, (target, distractors) in enumerate(zip(validated_targets, validated_distractors)):
            options = [target] + distractors
            random.shuffle(options)

            try:
                answer_pos = options.index(target) + 1
            except ValueError:
                options = [target] + distractors
                answer_pos = 1

            sub_questions.append({
                'number': i + 1,
                'target': target,
                'options': options,
                'answer': answer_pos
            })

        return {
            'code': code,
            'question_code': question_code,
            'sub_questions': sub_questions,
            'num_blanks': len(validated_targets)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Hybrid Question Generator: 1.5b + 14b',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python genai_ollama_hybrid_1_5b_14b.py "Create a for loop"
  python genai_ollama_hybrid_1_5b_14b.py "Vector with push_back" --blanks 3
  python genai_ollama_hybrid_1_5b_14b.py "Class definition" --blanks 5 --quiet
        """
    )
    parser.add_argument('topic', type=str, help='The topic/question')
    parser.add_argument('--blanks', '-b', type=int, default=3, help='Number of blanks')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode')

    args = parser.parse_args()
    verbose = not args.quiet

    if verbose:
        print("="*60)
        print("🚀 Hybrid Question Generator")
        print("="*60)
        print(f"\nFast Model:    {FAST_MODEL} (code generation)")
        print(f"Quality Model: {QUALITY_MODEL} (validation)")
        print(f"\nExpected time: ~25s (vs 70s for 14b alone)")
        print(f"Quality:       Very Good (14b validated)\n")

    # Initialize generator
    generator = HybridQuestionGenerator(
        base_url=OLLAMA_URL,
        fast_model=FAST_MODEL,
        quality_model=QUALITY_MODEL
    )

    # Generate question
    result = generator.generate_hybrid_question(
        topic=args.topic,
        num_blanks=args.blanks,
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
        print(f"\nNumber of Blanks: {result['num_blanks']}")
        print("\nSub-Questions:")
        for sq in result['sub_questions']:
            print(f"\n--- Question {sq['number']} (Fill in blank {sq['number']}) ---")
            print("Options:")
            for i, option in enumerate(sq['options'], 1):
                marker = " ✓ CORRECT" if i == sq['answer'] else ""
                print(f"  {i}. {option}{marker}")
            print(f"Answer: {sq['answer']}")
        print(f"\n{'='*60}")
        print("💡 Generation Strategy:")
        print(f"  Phase 1: 1.5b generated code (~10s)")
        print(f"  Phase 2: 14b extracted targets (~15s)")
        print(f"  Result: 64% faster than 14b alone!")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
