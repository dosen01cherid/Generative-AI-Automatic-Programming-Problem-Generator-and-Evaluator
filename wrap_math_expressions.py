#!/usr/bin/env python3
"""
Script to wrap mathematical expressions in double backticks for AsciiMath notation.
"""

import re
import sys

def wrap_math_expressions(text):
    """Wrap mathematical expressions in double backticks."""

    # Patterns to match and wrap
    patterns = [
        # Vector spaces: RR^n
        (r'\bRR\^(\d+|n)\b', r'``RR^\1``'),

        # Vectors in brackets: [a,b], [[a,b]], [a,b,c]
        (r'(\[\[?[-\d/,\s]+\]?\])', r'``\1``'),

        # Coordinates: (x,y), (a,b)
        (r'\(([a-z],[a-z](?:,[a-z])?)\)', r'``(\1)``'),

        # Single variables in math context (x, y, z, etc.) - be careful with context
        (r'\b([a-z])\s*=\s*([-\d/]+)', r'``\1 = \2``'),
        (r'komponen\s+([a-z])\s*=\s*([-\d/]+)', r'komponen ``\1 = \2``'),

        # Expressions: x + y, 2x + 3y, etc.
        (r'\b(\d*[a-z]\s*[+\-*/×÷]\s*\d*[a-z])', r'``\1``'),

        # Matrix notation: A, B, C (when capitalized and standalone)
        (r'\bmatriks\s+([A-Z])\b', r'matriks ``\1``'),

        # Row notation: R_1, R_2, R_3
        (r'\bR_(\d+)\b', r'``R_\1``'),

        # Functions: T(x,y), f(x)
        (r'\b([T-Z]|[f-h])\(([a-z,]+)\)', r'``\1(\2)``'),

        # Fractions: 1/2, 1/3, a/b
        (r'\b(\d+/\d+|[a-z]/[a-z])\b', r'``\1``'),

        # Mathematical operators when standalone
        (r'\b(×|÷|≠)\b', r'``\1``'),

        # Specific vector/matrix operations already wrapped
        (r'(\d+)\*(\[\[[-\d,\s]+\]\])', r'``\1*\2``'),

        # Special operators: cdot, xx, -:, !=
        (r'\s+cdot\s+', r' ``cdot`` '),
        (r'\s+xx\s+', r' ``xx`` '),
    ]

    result = text
    for pattern, replacement in patterns:
        result = re.sub(pattern, replacement, result)

    # Clean up double-wrapping
    result = re.sub(r'``+', '``', result)
    result = re.sub(r'``\s*``', '``', result)

    return result

def should_skip_line(line):
    """Check if line should skip wrapping (field labels, etc.)."""
    skip_prefixes = [
        'Problem Title:',
        'Problem Description:',
        'Step Type:',
        'Must Be Correct:',
        'Correct Answer:',
        'Explanation:',
        '#Step',
        '###',
        'Options:',
        'Blanks:',
        'SET SOAL',
        'MANFAAT',
        'AKHIR',
    ]

    for prefix in skip_prefixes:
        if line.strip().startswith(prefix):
            return True

    # Skip if line is already heavily wrapped
    if line.count('``') > 4:
        return True

    return False

def process_file(input_path, output_path):
    """Process a file and wrap mathematical expressions."""
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed_lines = []
    for line in lines:
        if should_skip_line(line):
            processed_lines.append(line)
        else:
            processed_lines.append(wrap_math_expressions(line))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

    print(f"Processed: {input_path} -> {output_path}")

if __name__ == '__main__':
    files = [
        '01_vector_problems_id.txt',
        '02_matrix_problems_id.txt',
        '03_linear_transformation_problems_id.txt',
        '04_linear_systems_problems_id.txt',
        '05_gauss_jordan_problems_id.txt',
    ]

    for filename in files:
        process_file(filename, filename)

    print("All files processed!")
