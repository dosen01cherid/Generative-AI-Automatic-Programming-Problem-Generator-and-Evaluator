import re

def convert_fill_blank_to_math(filename):
    """Convert fill-blank questions to math-expression where appropriate"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    conversions = [
        # Pattern 1: Simple numeric answers
        {
            'pattern': r'(#\nStep Type: fill-blank\nMust Be Correct: true\nStep Description: [^\n]*\{blank\}[^\n]*\nCorrect Answer: )(\d+)',
            'replace': lambda m: f"#\nStep Type: math-expression\nMust Be Correct: true\nStep Description: {m.group(0).split('Step Description: ')[1].split('Correct Answer:')[0].strip().replace('{blank}', '___')}\nStep Expression: `x`\nStep Expected: `{m.group(2)}`"
        },
        # Pattern 2: Convert "komponen kedua adalah {blank}" type questions
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Dalam vektor [5,8,1], komponen kedua adalah {blank}\nCorrect Answer: 8',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Dalam vektor [5,8,1], komponen kedua adalah ___\nStep Expression: `[5,8,1][1]`\nStep Expected: `8`'
        },
        # Pattern 3: Result of cross product component
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Untuk a = (a_1, a_2, a_3) dan b = (b_1, b_2, b_3), komponen i dari a xx b = __ kali __ - __ kali __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Untuk a = (a_1, a_2, a_3) dan b = (b_1, b_2, b_3), komponen i dari a xx b adalah:\nStep Expression: `a_2*b_3 - a_3*b_2`\nStep Expected: `a_2*b_3 - a_3*b_2`'
        },
        # Pattern 4: Vector subtraction formula
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Untuk vektor a = (a_1, a_2) dan b = (b_1, b_2), pengurangan a - b = (__, __)',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Untuk vektor a = (a_1, a_2) dan b = (b_1, b_2), pengurangan a - b = ?\nStep Expression: `[[a_1 - b_1, a_2 - b_2]]`\nStep Expected: `[[a_1 - b_1, a_2 - b_2]]`'
        },
        # Pattern 5: Dot product formula
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Untuk vektor u = (u_1, u_2) dan v = (v_1, v_2), hasil kali titik u cdot v = __ kali __ + __ kali __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Untuk vektor u = (u_1, u_2) dan v = (v_1, v_2), hasil kali titik u cdot v = ?\nStep Expression: `u_1*v_1 + u_2*v_2`\nStep Expected: `u_1*v_1 + u_2*v_2`'
        },
        # Pattern 6: Orthogonality condition
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Dua vektor u dan v ortogonal jika dan hanya jika hasil kali titik u cdot v = __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Dua vektor u dan v ortogonal jika dan hanya jika hasil kali titik u cdot v = ?\nStep Expression: `u*v`\nStep Expected: `0`'
        },
        # Pattern 7: Magnitude formula
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Untuk vektor v = (x, y), besar ||v|| = sqrt(__^2 + __^2)',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Untuk vektor v = (x, y), besar ||v|| = ?\nStep Expression: `sqrt(x^2 + y^2)`\nStep Expected: `sqrt(x^2 + y^2)`'
        },
        # Pattern 8: Unit vector formula
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Untuk mencari vektor satuan u-topi dalam arah v, kita hitung u-topi = v / __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Untuk mencari vektor satuan u-topi dalam arah v, kita hitung u-topi = v / ?\nStep Expression: `v/||v||`\nStep Expected: `||v||`'
        },
        # Pattern 9: Scalar projection formula
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Proyeksi skalar dari u pada v = (u cdot v) / __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Proyeksi skalar dari u pada v = (u cdot v) / ?\nStep Expression: `(u*v)/||v||`\nStep Expected: `||v||`'
        }
    ]
    
    # Apply conversions
    for conv in conversions:
        if 'pattern' in conv:
            # Regex-based conversion
            content = re.sub(conv['pattern'], conv['replace'], content)
        else:
            # Direct string replacement
            content = content.replace(conv['old'], conv['new'])
    
    # Write back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Converted {filename}")

# Process file 01
convert_fill_blank_to_math('01_vector_problems_id.txt')
