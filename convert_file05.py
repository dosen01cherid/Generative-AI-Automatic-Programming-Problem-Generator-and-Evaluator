def convert_fill_blank_to_math_file05(filename):
    """Convert fill-blank questions to math-expression in file 05"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    conversions = [
        # Baris kedua matrix
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Dalam matriks [[a,b,c],[d,e,f]], baris kedua adalah [{blank},{blank},{blank}]\nCorrect Answer: d,e,f',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Dalam matriks [[a,b,c],[d,e,f]], baris kedua adalah?\nStep Expression: `[[d,e,f]]`\nStep Expected: `[[d,e,f]]`'
        },
        # R_2 notation
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Untuk mengalikan baris 2 dengan 3, kita tulis R_2 → {blank}R_2\nCorrect Answer: 3',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Untuk mengalikan baris 2 dengan 3, faktor perkalian adalah?\nStep Expression: `3*R_2`\nStep Expected: `3`'
        },
        # Row swap notation
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Untuk menukar baris 1 dan baris 3, kita tulis R_1 {blank} R_3\nCorrect Answer: \leftrightarrow',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Notasi untuk menukar baris 1 dan baris 3 adalah?\nStep Expression: `R_1 <-> R_3`\nStep Expected: `\leftrightarrow`'
        },
        # Subtraction notation
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Untuk mengganti baris 2 dengan "baris 2 dikurangi 2 kali baris 1", kita tulis R_2 → R_2 {blank} 2R_1\nCorrect Answer: -',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Operator dalam R_2 → R_2 ___ 2R_1 untuk mengurangi adalah?\nStep Expression: `R_2 - 2*R_1`\nStep Expected: `-`'
        },
        # Scalar multiplication factor
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Baris 1 dikalikan dengan berapa? Jawab dalam bentuk pecahan jika perlu: {blank}\nCorrect Answer: 1/2',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Baris 1 dikalikan dengan berapa? (bentuk pecahan)\nStep Expression: `k`\nStep Expected: `1/2`'
        },
        # Element calculations
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Elemen pertama baris 2 baru = 3 - 1 = {blank}\nCorrect Answer: 2',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Elemen pertama baris 2 baru = ?\nStep Expression: `3 - 1`\nStep Expected: `2`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Elemen kedua baris 2 baru = 4 - 1 = {blank}\nCorrect Answer: 3',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Elemen kedua baris 2 baru = ?\nStep Expression: `4 - 1`\nStep Expected: `3`'
        },
        # Scalar multiplication result
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: 3R_1 = 3[[1,2,3]] = [[3,{blank},9]]\nCorrect Answer: 6',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: 3R_1 = 3[[1,2,3]], elemen kedua adalah?\nStep Expression: `3*2`\nStep Expected: `6`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: 2R_1 = 2[[1,2,3]] = [[2,4,{blank}]]\nCorrect Answer: 6',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: 2R_1 = 2[[1,2,3]], elemen ketiga adalah?\nStep Expression: `2*3`\nStep Expected: `6`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: R_2 - 2R_1 = [[4,5,6]] - [[2,4,6]] = [[2,1,{blank}]]\nCorrect Answer: 0',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: R_2 - 2R_1 = [[4,5,6]] - [[2,4,6]], elemen ketiga adalah?\nStep Expression: `6 - 6`\nStep Expected: `0`'
        }
    ]
    
    # Apply conversions
    for conv in conversions:
        content = content.replace(conv['old'], conv['new'])
    
    # Write back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Converted {filename}")

convert_fill_blank_to_math_file05('05_gauss_jordan_problems_id.txt')
