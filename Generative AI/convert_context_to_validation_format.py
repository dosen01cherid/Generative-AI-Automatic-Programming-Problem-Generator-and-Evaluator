"""
Convert context.txt to context_with_validation.txt

Transforms fill-in-the-blank examples from the old format:
  Code -> Question -> Options -> Answer

To the new validation format:
  CODE -> TARGET -> DISTRACTORS

This new format teaches the model to output in the exact format
expected by genai_ollama_client_with_rag_validated.py
"""

import re
import sys
import io
from pathlib import Path

# Fix encoding for Windows console to support emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def extract_target_from_question(code, question):
    """
    Compare code and question to find what was replaced with _____.
    Returns the target string that should be replaced.
    """
    # Tokenize both code and question
    code_lines = code.strip().split('\n')
    question_lines = question.strip().split('\n')

    if len(code_lines) != len(question_lines):
        return None

    # Find the line with _____
    for code_line, q_line in zip(code_lines, question_lines):
        if '_____' in q_line:
            # Find what was replaced
            # Simple approach: find the difference

            # Split by common delimiters
            code_tokens = re.split(r'(\s+|[(){}<>;,.\[\]"])', code_line)
            q_tokens = re.split(r'(\s+|[(){}<>;,.\[\]"])', q_line)

            # Find the token that became _____
            for i, (ct, qt) in enumerate(zip(code_tokens, q_tokens)):
                if qt == '_____' and ct != '_____':
                    return ct

            # Fallback: try to find the word/token that differs
            # This handles cases where the replacement spans multiple tokens
            code_words = code_line.split()
            q_words = q_line.split()

            for cw in code_words:
                if cw not in q_line and '_____' in q_line:
                    # Check if this word appears in the code line at the blank position
                    return cw

    return None


def parse_example(text):
    """Parse a single fill-in-the-blank example."""
    # Extract example ID and description
    header_match = re.search(
        r'Fill-in-the-Blank Question Example ([^\(]+)\(([^\)]+)\)',
        text
    )
    if not header_match:
        return None

    example_id = header_match.group(1).strip()
    description = header_match.group(2).strip()

    # Extract Code section
    code_match = re.search(
        r'Code\s*--+\s*(.*?)\s*--+',
        text,
        re.DOTALL
    )
    if not code_match:
        return None
    code = code_match.group(1).strip()

    # Extract Question section
    question_match = re.search(
        r'Question\s*--+\s*(.*?)\s*--+',
        text,
        re.DOTALL
    )
    if not question_match:
        return None
    question = question_match.group(1).strip()

    # Extract Options section
    options_match = re.search(
        r'Options\s*--+\s*(.*?)\s*--+',
        text,
        re.DOTALL
    )
    if not options_match:
        return None
    options_text = options_match.group(1).strip()

    # Extract Answer
    answer_match = re.search(
        r'Answer\s*--+\s*(\d+)',
        text,
        re.DOTALL
    )
    if not answer_match:
        return None
    answer_num = int(answer_match.group(1).strip())

    # Parse options
    options = []
    for line in options_text.split('\n'):
        # Match pattern: 1. option1  2. option2  3. option3  4. option4
        parts = re.findall(r'\d+\.\s*([^\d]+?)(?=\s+\d+\.|$)', line)
        if parts:
            options.extend([p.strip() for p in parts])

    if len(options) < 4:
        # Try alternate format
        option_matches = re.findall(r'\d+\.\s*(.+)', options_text)
        if option_matches:
            options = [opt.strip() for opt in option_matches]

    if len(options) != 4:
        print(f"Warning: Example {example_id} has {len(options)} options instead of 4")
        return None

    # Extract target from code and question
    target = extract_target_from_question(code, question)
    if not target:
        print(f"Warning: Could not extract target from Example {example_id}")
        return None

    # Get correct answer and distractors
    correct_answer = options[answer_num - 1]  # Convert to 0-indexed

    # Verify target matches correct answer
    if target != correct_answer:
        print(f"Warning: Example {example_id} - target '{target}' != answer '{correct_answer}'")
        # Use correct answer as target (trust the answer)
        target = correct_answer

    # Get distractors (all options except correct answer)
    distractors = [opt for i, opt in enumerate(options) if i != answer_num - 1]

    return {
        'id': example_id,
        'description': description,
        'code': code,
        'target': target,
        'distractors': distractors
    }


def format_example_for_validation(example):
    """Format an example in the new validation format."""
    output = []
    output.append("------------------")
    output.append(f"Fill-in-the-Blank Question Example {example['id']} ({example['description']})")
    output.append("------------------")
    output.append("CODE:")
    output.append("```cpp")
    output.append(example['code'])
    output.append("```")
    output.append("")
    output.append("TARGET:")
    output.append(example['target'])
    output.append("")
    output.append("DISTRACTORS:")
    for i, distractor in enumerate(example['distractors'], 1):
        output.append(f"{i}. {distractor}")
    output.append("")

    return '\n'.join(output)


def main():
    # Read context.txt
    context_path = Path("context.txt")
    if not context_path.exists():
        print("❌ context.txt not found!")
        return

    content = context_path.read_text(encoding='utf-8')

    print("📖 Reading context.txt...")

    # Extract the instructions section
    instructions_match = re.search(
        r'(.*?SIMPLE FILL-IN-THE-BLANK EXAMPLES)',
        content,
        re.DOTALL
    )

    instructions = ""
    if instructions_match:
        instructions = instructions_match.group(1).strip()

    # Split into individual examples
    example_pattern = r'------------------\s*Fill-in-the-Blank Question Example.*?(?=------------------\s*Fill-in-the-Blank Question Example|END OF EXAMPLES|$)'

    matches = re.finditer(example_pattern, content, re.DOTALL)

    examples = []
    for match in matches:
        example_text = match.group(0)
        parsed = parse_example(example_text)
        if parsed:
            examples.append(parsed)

    print(f"✅ Parsed {len(examples)} examples")

    # Create new context with validation format
    print("🔄 Converting to validation format...")

    output_lines = []

    # Add modified instructions
    output_lines.append("HOW TO CREATE ACCURATE FILL-IN-THE-BLANK QUESTIONS")
    output_lines.append("=" * 60)
    output_lines.append("")
    output_lines.append("IMPORTANT: Use this EXACT format for all fill-in-the-blank questions:")
    output_lines.append("")
    output_lines.append("CODE:")
    output_lines.append("```cpp")
    output_lines.append("[Write complete, working C++ code here - no blanks, full working code]")
    output_lines.append("```")
    output_lines.append("")
    output_lines.append("TARGET:")
    output_lines.append("[Write the EXACT token/word/phrase from the code above that should be replaced with _____]")
    output_lines.append("")
    output_lines.append("DISTRACTORS:")
    output_lines.append("1. [Wrong option 1 - similar but incorrect]")
    output_lines.append("2. [Wrong option 2 - similar but incorrect]")
    output_lines.append("3. [Wrong option 3 - similar but incorrect]")
    output_lines.append("")
    output_lines.append("CRITICAL RULES:")
    output_lines.append("1. CODE must be complete and working C++ code")
    output_lines.append("2. TARGET must appear EXACTLY as written in CODE")
    output_lines.append("3. DISTRACTORS must be plausible but incorrect alternatives")
    output_lines.append("4. Use ONLY modern C++ syntax (C++11 and later)")
    output_lines.append("5. NEVER use old C-style code (malloc, printf, char*, NULL)")
    output_lines.append("")
    output_lines.append("=" * 60)
    output_lines.append("FILL-IN-THE-BLANK EXAMPLES WITH VALIDATION FORMAT")
    output_lines.append("=" * 60)
    output_lines.append("")
    output_lines.append("These examples demonstrate the correct format for creating")
    output_lines.append("fill-in-the-blank questions. Each example shows:")
    output_lines.append("- CODE: Complete working code")
    output_lines.append("- TARGET: Exact token to replace")
    output_lines.append("- DISTRACTORS: 3 wrong but plausible options")
    output_lines.append("")

    # Add converted examples
    for example in examples:
        output_lines.append(format_example_for_validation(example))

    output_lines.append("------------------")
    output_lines.append("END OF EXAMPLES")
    output_lines.append("------------------")

    # Write to context_with_validation.txt
    output_path = Path("context_with_validation.txt")
    output_content = '\n'.join(output_lines)
    output_path.write_text(output_content, encoding='utf-8')

    print(f"✅ Created context_with_validation.txt")
    print(f"   - {len(examples)} examples converted")
    print(f"   - File size: {len(output_content):,} characters")
    print(f"   - Format: CODE -> TARGET -> DISTRACTORS")
    print("")
    print("📊 Summary:")
    print(f"   Original format: Code -> Question -> Options -> Answer")
    print(f"   New format:      CODE -> TARGET -> DISTRACTORS")
    print("")
    print("✅ Ready for use with genai_ollama_client_with_rag_validated.py")


if __name__ == "__main__":
    main()
