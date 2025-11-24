import re

def add_backticks_to_line(line):
    """Add backticks to Step Expression and Step Expected lines if not already present"""
    # Pattern for Step Expression: content (without backticks)
    if line.startswith('Step Expression: ') and '`' not in line:
        content = line.replace('Step Expression: ', '').strip()
        return f'Step Expression: `{content}`\n'
    # Pattern for Step Expected: content (without backticks)
    elif line.startswith('Step Expected: ') and '`' not in line:
        content = line.replace('Step Expected: ', '').strip()
        return f'Step Expected: `{content}`\n'
    return line

def process_file(filename):
    """Process a file to add backticks where needed"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified_lines = [add_backticks_to_line(line) for line in lines]
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)
        
        print(f"✓ Processed {filename}")
    except Exception as e:
        print(f"✗ Error processing {filename}: {e}")

# Process all 5 files
files = [
    '01_vector_problems_id.txt',
    '02_matrix_problems_id.txt',
    '03_linear_transformation_problems_id.txt',
    '04_linear_systems_problems_id.txt',
    '05_gauss_jordan_problems_id.txt'
]

for filename in files:
    process_file(filename)

print("\nAll files processed!")
