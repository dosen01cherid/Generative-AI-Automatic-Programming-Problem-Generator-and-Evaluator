def convert_file_02():
    with open('02_matrix_problems_id.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    conversions = [
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Perkalian skalar k dengan matriks A dilakukan dengan mengalikan setiap __ matriks dengan k',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Perkalian skalar k dengan matriks A dilakukan dengan mengalikan setiap ___ matriks dengan k?\nStep Expression: `k*A`\nStep Expected: `elemen`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Jika A berukuran 2x3 dan B berukuran 3x2, maka AB berukuran __ x __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Jika A berukuran 2x3 dan B berukuran 3x2, maka ukuran AB adalah?\nStep Expression: `[[2,2]]`\nStep Expected: `2x2`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Jumlah kolom C adalah __ dan jumlah baris D adalah __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Jumlah kolom C (2x3) dan jumlah baris D (2x4) berbeda, berapa selisihnya?\nStep Expression: `3 - 2`\nStep Expected: `1`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Jika A berukuran 2x2, maka A^T berukuran __ x __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Jika A berukuran 2x2, maka A^T berukuran?\nStep Expression: `[[2,2]]`\nStep Expected: `2x2`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Jika A berukuran 3x2, maka A^T berukuran __ x __',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Jika A berukuran 3x2, maka A^T berukuran?\nStep Expression: `[[2,3]]`\nStep Expected: `2x3`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Matriks identitas 2x2 adalah I = [[__,0],[0,__]]',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Matriks identitas 2x2 adalah I = ?\nStep Expression: `[[1,0],[0,1]]`\nStep Expected: `[[1,0],[0,1]]`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: A^2 = A __ A',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: A^2 = A ___ A, operator yang digunakan adalah?\nStep Expression: `A*A`\nStep Expected: `*`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Trace matriks adalah jumlah dari elemen-elemen pada __ utama',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Trace matriks adalah jumlah dari elemen-elemen pada posisi apa?\nStep Expression: `diagonal`\nStep Expected: `diagonal`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Dari elemen (1,1): k times __ = 6',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Dari elemen (1,1): k times ___ = 6, nilai elemen (1,1) adalah?\nStep Expression: `6/k`\nStep Expected: `2`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Mengalikan matriks diagonal D dari kiri ke matriks A akan mengalikan setiap __ A dengan elemen diagonal D yang bersesuaian',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Mengalikan matriks diagonal D dari kiri ke matriks A akan mengalikan setiap ___ dengan elemen diagonal D?\nStep Expression: `D*A`\nStep Expected: `baris`'
        }
    ]
    
    for conv in conversions:
        content = content.replace(conv['old'], conv['new'])
    
    with open('02_matrix_problems_id.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Converted file 02")

def convert_file_03():
    with open('03_linear_transformation_problems_id.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    conversions = [
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Sifat T(u+v) = T(u) + T(v) disebut sifat {blank}\nCorrect Answer: aditivitas',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Sifat T(u+v) = T(u) + T(v) disebut sifat apa?\nStep Expression: `T(u+v) == T(u) + T(v)`\nStep Expected: `aditivitas`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Sifat T(cv) = cT(v) disebut sifat {blank}\nCorrect Answer: homogenitas',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Sifat T(cv) = cT(v) disebut sifat apa?\nStep Expression: `T(c*v) == c*T(v)`\nStep Expected: `homogenitas`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Vektor basis standar di RR^2 adalah e_1 = (1,{blank}) dan e_2 = ({blank},1)\nCorrect Answer: 0, 0',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Vektor basis standar di RR^2 adalah e_1 = (1,?) dan e_2 = (?,1)\nStep Expression: `[[1,0],[0,1]]`\nStep Expected: `0, 0`'
        }
    ]
    
    for conv in conversions:
        content = content.replace(conv['old'], conv['new'])
    
    with open('03_linear_transformation_problems_id.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Converted file 03")

def convert_file_04():
    with open('04_linear_systems_problems_id.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    conversions = [
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Misalkan x = harga satu {blank} dan y = harga satu pensil\nCorrect Answer: buku',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Misalkan x = harga satu ___ dan y = harga satu pensil (isi nama barang)\nStep Expression: `x`\nStep Expected: `buku`'
        },
        {
            'old': 'Step Type: fill-blank\nMust Be Correct: true\nStep Description: Misalkan x = jumlah produk {blank}\nCorrect Answer: A',
            'new': 'Step Type: math-expression\nMust Be Correct: true\nStep Description: Misalkan x = jumlah produk ___ (nama produk)\nStep Expression: `x`\nStep Expected: `A`'
        }
    ]
    
    for conv in conversions:
        content = content.replace(conv['old'], conv['new'])
    
    with open('04_linear_systems_problems_id.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Converted file 04")

convert_file_02()
convert_file_03()
convert_file_04()
print("\nAll conversions complete!")
