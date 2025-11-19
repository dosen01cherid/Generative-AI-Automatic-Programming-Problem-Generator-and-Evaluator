import re

def wrap_math(content):
    # Don't wrap if already wrapped
    patterns = [
        # RR^n spaces
        (r'(?<!`)RR\^(\d+)(?!`)', r'``RR^\1``'),
        # Vectors [[...]]
        (r'(?<!`)\[\[([^\]]+)\]\](?!`)', r'``[[\1]]``'),
        # Single vectors [1,2,3]
        (r'(?<![\[`])\[([0-9,\-\s/]+)\](?![\]`])', r'``[\1]``'),
        # Row notation R_1
        (r'(?<!`)R_(\d+)(?!`)', r'``R_1``'.replace('1', r'\1')),
        # Fractions 1/2
        (r'(?<![0-9`])(\d+)/(\d+)(?![0-9`])', r'``\1/\2``'),
        # Variables in expressions
        (r'([0-9]*[a-z])(\s*[\+\-\*]\s*[0-9]*[a-z])+', r'``\g<0>``'),
    ]
    
    for pattern, repl in patterns:
        content = re.sub(pattern, repl, content)
    
    return content

files = [
    "01_vector_problems_id.txt",
    "02_matrix_problems_id.txt",
    "03_linear_transformation_problems_id.txt",
    "04_linear_systems_problems_id.txt",
    "05_gauss_jordan_problems_id.txt"
]

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    wrapped = wrap_math(content)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(wrapped)
    
    print(f"Updated {fname}")

print("Done!")
