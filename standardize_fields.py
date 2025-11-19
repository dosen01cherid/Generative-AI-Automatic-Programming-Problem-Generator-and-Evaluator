#!/usr/bin/env python3
"""
Standardize problem set files to use English structural field labels
"""

import re
import sys

def standardize_problem_set(content):
    """
    Standardize structural fields in problem set content
    """
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Remove step headers like "#Step 1 [Pilihan Ganda - Tunggal]:" → just "#"
        if re.match(r'^#Step \d+.*:', line):
            result.append('#')
            i += 1
            continue

        # Change "Question:" to "Step Description:"
        if line.startswith('Question:'):
            result.append(line.replace('Question:', 'Step Description:', 1))
            i += 1
            continue

        # Change "Answer:" to "Correct Answer:" (but not "Expected Answer:")
        if re.match(r'^Answer:\s', line) and not line.startswith('Expected Answer:'):
            result.append(line.replace('Answer:', 'Correct Answer:', 1))
            i += 1
            continue

        # Change "Expected Answer:" to "Step Expected:"
        if line.startswith('Expected Answer:'):
            result.append(line.replace('Expected Answer:', 'Step Expected:', 1))
            i += 1
            continue

        # Handle "Options:" block - convert to Option A:, Option B:, etc.
        if line.startswith('Options:'):
            i += 1  # Skip the "Options:" line
            # Collect option lines
            while i < len(lines) and lines[i].strip().startswith(('A)', 'B)', 'C)', 'D)', 'E)')):
                option_line = lines[i].strip()
                # Extract option letter and text
                match = re.match(r'^([A-E])\)\s*(.+)$', option_line)
                if match:
                    letter = match.group(1)
                    text = match.group(2)
                    result.append(f'Option {letter}: {text}')
                i += 1
            continue

        # Change "Benar" and "Salah" to "True" and "False" in Correct Answer lines
        if 'Correct Answer:' in line:
            line = re.sub(r'\bBenar\b', 'True', line)
            line = re.sub(r'\bSalah\b', 'False', line)
            result.append(line)
            i += 1
            continue

        # Change "Must Be Correct: True/False" to lowercase
        if line.startswith('Must Be Correct:'):
            line = re.sub(r'Must Be Correct:\s*True', 'Must Be Correct: true', line)
            line = re.sub(r'Must Be Correct:\s*False', 'Must Be Correct: false', line)
            result.append(line)
            i += 1
            continue

        # Skip "Explanation:" lines
        if line.startswith('Explanation:'):
            i += 1
            continue

        # Skip "Blanks:" blocks
        if line.startswith('Blanks:'):
            i += 1
            # Skip indented content under Blanks
            while i < len(lines) and (lines[i].startswith('  -') or lines[i].strip() == ''):
                i += 1
            continue

        # Default: keep the line as-is
        result.append(line)
        i += 1

    return '\n'.join(result)


def main():
    # List of problem set files
    files = [
        '01_vector_problems_id.txt',
        '02_matrix_problems_id.txt',
        '03_linear_transformation_problems_id.txt',
        '04_linear_systems_problems_id.txt',
        '05_gauss_jordan_problems_id.txt'
    ]

    for filename in files:
        print(f'Processing {filename}...')

        try:
            # Read the file
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            # Standardize the content
            standardized = standardize_problem_set(content)

            # Write back to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(standardized)

            print(f'  ✓ Successfully standardized {filename}')

        except Exception as e:
            print(f'  ✗ Error processing {filename}: {e}')
            sys.exit(1)

    print('\nAll files successfully standardized!')


if __name__ == '__main__':
    main()
