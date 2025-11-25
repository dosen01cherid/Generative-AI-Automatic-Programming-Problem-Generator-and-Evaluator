# Panduan Pengguna - Problem Creator (create_problem.html)

## Daftar Isi
1. [Pengenalan](#pengenalan)
2. [Memulai Aplikasi](#memulai-aplikasi)
3. [Membuat Problem Baru](#membuat-problem-baru)
4. [Jenis-Jenis Soal](#jenis-jenis-soal)
5. [Mengelola Problem Set](#mengelola-problem-set)
6. [Import dan Export](#import-dan-export)
7. [Fitur Pencarian](#fitur-pencarian)
8. [Tips dan Trik](#tips-dan-trik)

---

## Pengenalan

**Problem Creator** adalah aplikasi web untuk membuat dan mengelola set soal ujian atau latihan. Aplikasi ini mendukung berbagai jenis soal dan dapat digunakan secara offline setelah dimuat pertama kali.

### Fitur Utama:
- Mendukung 7 jenis soal berbeda
- Editor teks kaya (rich text) dengan dukungan matematika
- Import/Export dalam format JSON
- Penyimpanan otomatis (autosave)
- Validasi jawaban otomatis
- Pencarian cepat
- Bekerja offline

---

## Memulai Aplikasi

### Langkah Pertama:
1. Buka file `create_problem.html` di browser web modern (Chrome, Firefox, Edge, atau Safari)
2. Tunggu hingga loading selesai (pertama kali akan download library yang diperlukan)
3. Status loading akan menampilkan:
   - "Loading Pyodide..."
   - "Loading packages..."
   - "Python app ready!"
4. Setelah loading selesai, aplikasi siap digunakan

### Tampilan Utama:
- **Header**: Judul aplikasi "NoNet-NoSet-NoChat - Problem Creator"
- **Tombol "+ Create Problem"**: Untuk membuat soal baru
- **Area Konten**: Menampilkan daftar soal yang sudah dibuat
- **Panel Export**: Menampilkan Problem Set UUID dan JSON hasil export
- **Toolbar Melayang**: Tombol biru di pojok kanan bawah untuk akses cepat fitur-fitur

---

## Membuat Problem Baru

### Cara Membuat Soal:

1. **Klik tombol "+ Create Problem"**
   - Sebuah card soal baru akan muncul

2. **Isi Deskripsi Problem (Opsional)**
   - Field teks di bagian atas untuk deskripsi atau judul soal
   - Contoh: "Soal Aljabar Linear - Vektor"

3. **Klik "+ Add Step"**
   - Step adalah bagian/langkah dari soal
   - Satu problem bisa memiliki multiple steps

4. **Pilih Jenis Soal**
   - Dialog akan muncul dengan 7 pilihan jenis soal
   - Klik salah satu jenis yang diinginkan

5. **Isi Konten Soal**
   - Setiap jenis soal memiliki field yang berbeda
   - Gunakan toolbar editor untuk formatting teks
   - Klik tombol "Math" untuk memasukkan formula matematika

---

## Jenis-Jenis Soal

### 1. Multiple Choice - Single Answer (Pilihan Ganda - Satu Jawaban)

**Kapan digunakan**: Soal dengan beberapa pilihan, hanya satu jawaban benar.

**Cara penggunaan**:
1. Isi **Question** (pertanyaan)
2. Tambahkan **Options** (pilihan jawaban)
   - Klik "+ Add Option" untuk menambah pilihan
   - Minimal 2 pilihan
3. Centang **Correct Answer** pada pilihan yang benar
4. **Require All Correct**: Tidak berlaku untuk single answer

**Contoh**:
```
Question: Berapakah hasil dari 2 + 2?
Options:
○ 3
● 4  ← (Correct Answer)
○ 5
○ 6
```

---

### 2. Multiple Choice - Multiple Answers (Pilihan Ganda - Banyak Jawaban)

**Kapan digunakan**: Soal dengan beberapa pilihan, lebih dari satu jawaban benar.

**Cara penggunaan**:
1. Isi **Question**
2. Tambahkan **Options**
3. Centang **Correct Answer** pada semua pilihan yang benar
4. **Require All Correct**:
   - ✓ (ON): Siswa harus pilih SEMUA jawaban benar untuk dapat nilai
   - ✗ (OFF): Nilai dihitung per pilihan yang benar

**Contoh**:
```
Question: Manakah bilangan prima di bawah ini? (Pilih semua yang benar)
Options:
☑ 2  ← (Correct)
☐ 4
☑ 5  ← (Correct)
☐ 6
☑ 7  ← (Correct)

Require All Correct: ✓ (siswa harus pilih 2, 5, dan 7 untuk dapat nilai)
```

---

### 3. True/False (Benar/Salah)

**Kapan digunakan**: Pernyataan yang hanya bisa dijawab benar atau salah.

**Cara penggunaan**:
1. Isi **Statement** (pernyataan)
2. Pilih **Correct Answer**: True atau False

**Contoh**:
```
Statement: Python adalah bahasa pemrograman yang dikembangkan oleh Guido van Rossum.
Correct Answer: ● True ○ False
```

---

### 4. Short Answer (Jawaban Singkat)

**Kapan digunakan**: Soal yang memerlukan jawaban singkat dalam bentuk teks.

**Cara penggunaan**:
1. Isi **Question**
2. Isi **Correct Answer** (jawaban yang benar)
3. **Case Sensitive**:
   - ✓ (ON): "Python" ≠ "python"
   - ✗ (OFF): "Python" = "python"

**Contoh**:
```
Question: Siapa pencipta bahasa Python?
Correct Answer: Guido van Rossum
Case Sensitive: ✗ (menerima "guido van rossum" atau "GUIDO VAN ROSSUM")
```

---

### 5. Essay (Esai)

**Kapan digunakan**: Soal yang memerlukan jawaban panjang/penjelasan.

**Cara penggunaan**:
1. Isi **Prompt** (pertanyaan atau instruksi)
2. Isi **Sample Answer** (contoh jawaban yang baik)
   - Ini sebagai referensi, tidak untuk auto-grading

**Contoh**:
```
Prompt: Jelaskan perbedaan antara list dan tuple dalam Python. Berikan contoh penggunaan masing-masing.

Sample Answer: List adalah struktur data yang mutable (dapat diubah), ditulis dengan [...]. Tuple adalah immutable (tidak dapat diubah), ditulis dengan (...). Contoh list: [1, 2, 3], dapat diubah dengan append(). Contoh tuple: (1, 2, 3), tidak dapat diubah setelah dibuat.
```

---

### 6. Fill in the Blank (Isi Titik-Titik)

**Kapan digunakan**: Soal dengan satu atau lebih blank yang harus diisi.

**Cara penggunaan**:

#### Mode Single Blank (Satu Titik-Titik):
1. Isi **Template** dengan teks yang mengandung `____` (4 underscore)
2. Isi **Correct Answer**
3. **Case Sensitive**: pilih sesuai kebutuhan

**Contoh Single Blank**:
```
Template: Python dikembangkan oleh ____.
Correct Answer: Guido van Rossum
Case Sensitive: ✗
```

#### Mode Multi Blank (Banyak Titik-Titik):
1. Isi **Template** dengan teks yang mengandung `[blank1]`, `[blank2]`, dst.
2. Untuk setiap blank, klik "+ Add Correct Answer"
3. Isi **Label** (misalnya: "blank1") dan **Answer** (jawaban yang benar)

**Contoh Multi Blank**:
```
Template: [bahasa] dikembangkan oleh [pencipta] pada tahun [tahun].

Correct Answers:
- Label: bahasa    → Answer: Python
- Label: pencipta  → Answer: Guido van Rossum
- Label: tahun     → Answer: 1991
```

---

### 7. Multi-MC (Fill Blank dengan Dropdown)

**Kapan digunakan**: Soal isi titik-titik di mana siswa memilih dari dropdown options.

**Cara penggunaan**:
1. Isi **Template** dengan `[blank1]`, `[blank2]`, dst.
2. Untuk setiap blank:
   - Isi **Label** (contoh: "blank1")
   - Tambahkan **Options** dengan tombol "+ Add Option"
   - Centang **Correct Answer** pada option yang benar

**Contoh**:
```
Template: Bahasa [blank1] adalah bahasa [blank2].

Blank 1 (blank1):
  Options: Python ● | Java ○ | C++ ○  (Python correct)

Blank 2 (blank2):
  Options: compiled ○ | interpreted ● | assembly ○  (interpreted correct)
```

---

## Mengelola Problem Set

### Problem Set UUID
- Setiap problem set memiliki UUID unik
- UUID digunakan untuk tracking dan referensi
- Klik tombol "Copy UUID" untuk menyalin

### Problem Set Description
- Isi deskripsi untuk memberi konteks pada set soal
- Contoh: "UTS Aljabar Linear 2025", "Latihan Python Dasar"

### Mengelola Multiple Problems:
- **Duplicate**: Klik tombol duplikat untuk menyalin problem
- **Delete**: Klik tombol hapus untuk menghapus problem
- **Collapse/Expand**: Klik header untuk minimize/maximize problem card

### Mengelola Steps dalam Problem:
- **Add Step**: Tambah langkah/bagian baru dalam problem
- **Delete Step**: Hapus step yang tidak diperlukan
- **Reorder**: Drag and drop untuk mengubah urutan (jika tersedia)

---

## Import dan Export

### Export JSON

**Cara Export**:
1. Klik tombol **melayang biru** di pojok kanan bawah
2. Pilih accordion **"Data Management"**
3. Klik **"Export All"**
4. JSON akan muncul di panel "Exported JSON Preview"
5. Klik **"Download JSON"** untuk download file

**Catatan**:
- Aplikasi melakukan validasi sebelum export
- Problem yang tidak valid akan ditandai dengan warna:
  - 🟡 Kuning (Warning): Ada yang kurang lengkap
  - 🔴 Merah (Error): Error kritis, tidak bisa di-export
  - 🟢 Hijau (Valid): Problem siap di-export
- Lihat komentar validasi untuk detail error

### Import JSON

**Cara Import**:
1. Buka toolbar (tombol biru di kanan bawah)
2. Pilih **"Data Management"** → **"Import Problem Set"**
3. Ada 2 cara import:

   **A. Upload File JSON**:
   - Klik tab "Upload JSON"
   - Klik "Choose File" dan pilih file .json
   - Pilih mode import:
     - **Replace**: Hapus semua problem lama, ganti dengan yang baru
     - **Merge**: Gabungkan dengan problem yang sudah ada

   **B. Paste JSON Text**:
   - Klik tab "Paste JSON"
   - Copy-paste JSON text ke text area
   - Pilih mode import (Replace/Merge)

4. Klik tombol import
5. Tunggu proses selesai

---

## Fitur Pencarian

### Cara Menggunakan Search:
1. Klik **tombol toolbar** (biru, pojok kanan bawah)
2. Accordion **"Search & Navigate"** akan terbuka otomatis
3. Ketik kata kunci di search box
4. Hasil pencarian akan di-highlight dengan warna kuning
5. Gunakan tombol **Prev** / **Next** untuk navigasi antar hasil
6. Toggle **".*"** untuk mengaktifkan Regex mode

### Fitur Search:
- **Real-time search**: Hasil muncul saat mengetik
- **Regex support**: Pencarian dengan regular expression
- **Match counter**: Menampilkan jumlah hasil (contoh: "3/15")
- **Highlight**: Hasil ditandai dengan outline kuning
- **Current match**: Hasil aktif ditandai dengan warna oranye
- **Clear button**: Tombol "×" untuk menghapus pencarian

**Contoh Pencarian**:
- Cari kata: `Python`
- Cari dengan regex: `Python|Java` (cari Python atau Java)
- Cari angka: `\d+` (regex untuk angka)

---

## Tips dan Trik

### 1. Menggunakan Formula Matematika

**Inline Math** (dalam teks):
- Klik tombol **"Math"** di toolbar editor
- Pilih **"MathQuill"** untuk input visual atau **"LaTeX Text"** untuk menulis langsung
- Contoh LaTeX: `$x^2 + y^2 = r^2$`

**Display Math** (terpisah/tengah):
- Gunakan `$$` untuk display math
- Contoh: `$$\int_0^1 x^2 dx = \frac{1}{3}$$`

### 2. Autosave
- Aplikasi otomatis menyimpan progress setiap beberapa detik
- Indikator autosave muncul di pojok kanan bawah
- Data disimpan di localStorage browser

### 3. Validasi Sebelum Export
- Selalu cek komentar validasi (warna kuning/merah)
- Perbaiki error sebelum export
- Problem dengan error tidak akan ter-export

### 4. Keyboard Shortcuts
- **Ctrl/Cmd + B**: Bold teks (di editor)
- **Ctrl/Cmd + I**: Italic teks (di editor)
- **Ctrl/Cmd + U**: Underline teks (di editor)

### 5. Best Practices

**Untuk Pilihan Ganda**:
- Gunakan minimal 4 options untuk mengurangi tebakan
- Buat distractor (jawaban salah) yang masuk akal
- Hindari options "Semua benar" atau "Tidak ada yang benar"

**Untuk Short Answer**:
- Jika jawaban bisa bervariasi, non-aktifkan Case Sensitive
- Pertimbangkan gunakan Essay jika jawaban perlu penjelasan

**Untuk Fill in the Blank**:
- Gunakan single blank untuk konsep sederhana
- Gunakan multi blank untuk konsep yang saling terkait
- Label blank dengan nama yang jelas (misalnya: [subjek], [predikat])

**Untuk Essay**:
- Buat sample answer yang komprehensif
- Sample answer membantu grading manual
- Jelaskan kriteria penilaian di prompt

### 6. Menangani Error

**"Pyodide loading failed"**:
- Pastikan koneksi internet aktif untuk loading pertama
- Refresh halaman dan coba lagi
- Clear cache browser jika masih error

**"Validation failed"**:
- Baca pesan error di komentar validasi
- Pastikan semua field wajib terisi
- Untuk MC: minimal 2 options dan 1 correct answer
- Untuk True/False: correct answer harus dipilih

**"Import failed"**:
- Pastikan format JSON valid
- Cek apakah file JSON dari export yang compatible
- Gunakan mode Merge jika Replace error

### 7. Workflow Efisien

**Untuk Membuat Set Soal Besar**:
1. Buat 1 problem dengan beberapa steps sebagai template
2. Duplicate problem tersebut
3. Edit konten sesuai kebutuhan
4. Export secara berkala untuk backup

**Untuk Kolaborasi**:
1. Export JSON dari satu komputer
2. Share file JSON via email/cloud storage
3. Import JSON di komputer lain
4. Edit dan export lagi

---

## Informasi Tambahan

### Browser yang Didukung:
- Google Chrome (Recommended)
- Mozilla Firefox
- Microsoft Edge
- Safari

### Kapasitas:
- Tidak ada batasan jumlah problem/steps
- Batasan hanya dari localStorage browser (~5-10 MB)
- Untuk set soal besar, export JSON secara berkala

### Offline Usage:
- Setelah loading pertama kali, aplikasi dapat digunakan offline
- Library (Pyodide, MathJax) sudah di-cache di browser
- Data disimpan di localStorage, tidak hilang meskipun offline

---

## Dukungan dan Bantuan

Jika mengalami masalah:
1. Cek console browser (F12) untuk error message
2. Refresh halaman
3. Clear cache jika perlu
4. Export JSON sebagai backup sebelum troubleshooting

---

**Catatan**: Panduan ini dibuat untuk versi terbaru dari Problem Creator (NoNet-NoSet-NoChat). Beberapa fitur mungkin berbeda jika menggunakan versi yang berbeda.

---

*Panduan ini dibuat dengan Claude Code - Antropic*
