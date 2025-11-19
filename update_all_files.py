#!/usr/bin/env python3
"""
Comprehensive script to wrap ALL mathematical expressions in double backticks.
"""

import re
import os

def wrap_expressions(text):
    """Apply ALL wrapping rules in the correct order."""

    # Skip lines that are labels or already processed
    if any(text.strip().startswith(x) for x in ['#Step', '###', 'SET SOAL', 'AKHIR', 'MANFAAT']):
        return text

    # If line already has many backticks, skip it
    if text.count('``') > 6:
        return text

    result = text

    # 1. Vector spaces like RR^2, RR^3, RR^n
    result = re.sub(r'\bRR\^([0-9n])\b', r'``RR^\1``', result)

    # 2. Vectors in double brackets [[a,b,c]]
    result = re.sub(r'(\[\[[-\d/,\s]+\]\])', r'``\1``', result)

    # 3. Vectors in single brackets [a,b,c]
    result = re.sub(r'(\[[-\d/,\s]+\])', r'``\1``', result)

    # 4. Coordinate pairs and triples (x,y), (x,y,z)
    result = re.sub(r'\(([a-z]),([a-z])\)', r'``(\1,\2)``', result)
    result = re.sub(r'\(([a-z]),([a-z]),([a-z])\)', r'``(\1,\2,\3)``', result)
    result = re.sub(r'\(([0-9]+),([0-9]+)\)', r'``(\1,\2)``', result)
    result = re.sub(r'\(([0-9]+),([0-9]+),([0-9]+)\)', r'``(\1,\2,\3)``', result)

    # 5. Single variable assignments: x = 2, y = 3
    result = re.sub(r'\b([a-z])\s*=\s*([-\d/]+)\b', r'``\1 = \2``', result)

    # 6. Row notation R_1, R_2, etc.
    result = re.sub(r'\bR_(\d+)\b', r'``R_\1``', result)

    # 7. Fractions like 1/2, 3/4, a/b
    result = re.sub(r'\b(\d+/\d+)\b', r'``\1``', result)
    result = re.sub(r'\b([a-z])/([a-z])\b', r'``\1/\2``', result)

    # 8. Functions T(x,y), f(x)
    result = re.sub(r'\b([A-Z])\(([a-z,]+)\)', r'``\1(\2)``', result)

    # 9. Math operations: cdot, xx (cross product)
    result = re.sub(r'\scdot\s', r' ``cdot`` ', result)
    result = re.sub(r'\sxx\s', r' ``xx`` ', result)

    # 10. sqrt function
    result = re.sub(r'\bsqrt\(', r'``sqrt(', result)
    # Close the sqrt parenthesis
    result = re.sub(r'(\d+)\)(\s|$)', r'\1)``\2', result)

    # 11. Matrix dimensions like 2x2, 3x3
    result = re.sub(r'\b(\d+)x(\d+)\b', r'``\1xx\2``', result)

    # 12. Single variables when meaningful (in specific contexts)
    result = re.sub(r'variabel\s+([a-z])\b', r'variabel ``\1``', result)
    result = re.sub(r'komponen\s+([a-z])\b', r'komponen ``\1``', result)

    # 13. Matrix transpose notation A^T, B^T
    result = re.sub(r'\b([A-Z])\^T\b', r'``\1^T``', result)

    # 14. Expressions like 3*2, 4+5, etc.
    result = re.sub(r'\b(\d+)\s*\*\s*(\d+)\b', r'``\1*\2``', result)
    result = re.sub(r'\b(\d+)\s*\+\s*(\d+)\b', r'``\1+\2``', result)
    result = re.sub(r'\b(\d+)\s*-\s*(\d+)\b', r'``\1-\2``', result)

    # 15. Variables like x, y, z when standalone and clearly mathematical
    result = re.sub(r'\b([uvwxyz])\s+dan\s+([uvwxyz])\b', r'``\1`` dan ``\2``', result)

    # 16. Matrix names in specific contexts
    result = re.sub(r'matriks\s+([A-Z])\b', r'matriks ``\1``', result)

    # Clean up: remove double wrapping
    result = re.sub(r'``+', '``', result)
    result = re.sub(r'``\s*``', '``', result)

    # Clean up: unwrap field labels if accidentally wrapped
    result = re.sub(r'``(Question|Options|Answer|Expression|Blanks):``', r'\1:', result)

    return result

def process_file(filepath):
    """Process a single file."""
    print(f"Processing {filepath}...")

    # Read file
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process each line
    processed = [wrap_expressions(line) for line in lines]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(processed)

    print(f"✓ Completed {filepath}")

def main():
    """Main function."""
    files = [
        '01_vector_problems_id.txt',
        '02_matrix_problems_id.txt',
        '03_linear_transformation_problems_id.txt',
        '04_linear_systems_problems_id.txt',
        '05_gauss_jordan_problems_id.txt',
    ]

    for filename in files:
        if os.path.exists(filename):
            # Create backup
            backup = filename + '.backup'
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created backup: {backup}")

            # Process file
            process_file(filename)
        else:
            print(f"File not found: {filename}")

    print("\n✓ All files processed successfully!")
    print("Backups created with .backup extension")

if __name__ == '__main__':
    main()
