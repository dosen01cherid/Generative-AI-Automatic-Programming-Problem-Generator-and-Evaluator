# Panduan Pengguna - Problem Solver (solve_problem.html)

## Daftar Isi
1. [Pengenalan](#pengenalan)
2. [Memulai Aplikasi](#memulai-aplikasi)
3. [Memuat Problem Set](#memuat-problem-set)
4. [Menjawab Soal](#menjawab-soal)
5. [Jenis-Jenis Soal](#jenis-jenis-soal)
6. [Freestyle Practice Mode](#freestyle-practice-mode)
7. [Navigasi dan Kontrol](#navigasi-dan-kontrol)
8. [Export Progress](#export-progress)
9. [Reset Answers](#reset-answers)
10. [Tips dan Trik](#tips-dan-trik)

---

## Pengenalan

**Problem Solver** adalah aplikasi web untuk mengerjakan soal-soal ujian atau latihan yang sudah dibuat dengan Problem Creator. Aplikasi ini mendukung berbagai jenis soal dan dapat memberikan feedback langsung pada jawaban Anda.

### Fitur Utama:
- Mendukung 7 jenis soal berbeda
- Auto-grading untuk soal objektif
- Freestyle practice dengan sistem kredit
- MathQuill keyboard untuk input matematika
- Export progress untuk submit ke pengajar
- Penyimpanan otomatis jawaban
- Bekerja offline setelah dimuat pertama kali

---

## Memulai Aplikasi

### Langkah Pertama:
1. Buka file `solve_problem.html` di browser web modern (Chrome, Firefox, Edge, atau Safari)
2. Tunggu hingga loading selesai (pertama kali akan download library yang diperlukan)
3. Status loading akan menampilkan:
   - "Loading Pyodide..."
   - "Loading packages..."
   - "Python app ready!"
4. Setelah loading selesai, aplikasi siap digunakan

### Tampilan Utama:

**Sidebar Kiri**:
- **Menu Button** (☰): Buka/tutup sidebar
- **Problem Set Info**: Informasi problem set yang dimuat
- **Navigation**:
  - Problems (Soal-soal)
  - Freestyle Practice
  - Load Problem Set
  - Submit Progress
  - Reset Answers

**Area Konten**:
- Menampilkan soal yang sedang dikerjakan
- Input field untuk menjawab
- Tombol navigasi (Next, Previous)
- Feedback dan hasil grading

---

## Memuat Problem Set

### Cara Load Problem Set:

1. **Klik menu "Load Problem Set"** di sidebar
2. **Ada 2 cara untuk memuat soal**:

#### A. Upload File JSON:
1. Klik tab **"Upload JSON"**
2. Klik tombol **"Choose File"**
3. Pilih file JSON yang diekspor dari Problem Creator
4. Klik **"Load Problem Set"**
5. Problem set akan dimuat dan muncul di halaman Problems

#### B. Paste JSON:
1. Klik tab **"Paste JSON"**
2. Copy JSON dari Problem Creator
3. Paste ke text area
4. Klik **"Load Problem Set"**
5. Problem set akan dimuat dan muncul di halaman Problems

### Setelah Problem Set Dimuat:

- **Problem Set Info** di sidebar akan menampilkan:
  - Nama/deskripsi problem set
  - UUID problem set (untuk tracking)
- Daftar **problems** akan muncul di halaman Problems
- Klik pada problem untuk mulai mengerjakan

---

## Menjawab Soal

### Alur Mengerjakan Soal:

1. **Pilih Problem**
   - Klik pada problem card di halaman Problems
   - Problem akan expand menampilkan step-step

2. **Baca Soal**
   - Setiap problem terdiri dari 1 atau lebih **steps**
   - Baca pertanyaan/instruksi dengan teliti

3. **Masukkan Jawaban**
   - Gunakan input field yang tersedia
   - Untuk soal matematika, gunakan MathQuill keyboard

4. **Submit Jawaban**
   - Klik tombol **"Check Answer"** atau **"Submit"**
   - Sistem akan memberikan feedback:
     - ✅ **Correct**: Jawaban benar
     - ❌ **Incorrect**: Jawaban salah
     - ℹ️ **Info**: Informasi tambahan

5. **Lanjut ke Step Berikutnya**
   - Jika jawaban benar, otomatis bisa lanjut ke step berikutnya
   - Klik tombol **"Next Step"** untuk melanjutkan

6. **Selesaikan Problem**
   - Kerjakan semua steps dalam problem
   - Score akan dihitung otomatis

---

## Jenis-Jenis Soal

### 1. Multiple Choice - Single Answer (Pilihan Ganda Tunggal)

**Tampilan**:
- Pertanyaan di atas
- Beberapa pilihan jawaban dengan radio button (○)
- Hanya bisa pilih 1 jawaban

**Cara Menjawab**:
1. Baca pertanyaan
2. Klik pada pilihan yang menurut Anda benar (○)
3. Klik tombol **"Check Answer"**
4. Feedback akan muncul:
   - ✅ Hijau = Benar
   - ❌ Merah = Salah

**Contoh**:
```
Question: Berapakah hasil dari 2 + 2?
○ 3
○ 4  ← (Klik di sini)
○ 5
○ 6

[Check Answer]
```

---

### 2. Multiple Choice - Multiple Answers (Pilihan Ganda Banyak)

**Tampilan**:
- Pertanyaan di atas
- Beberapa pilihan dengan checkbox (☐)
- Bisa pilih lebih dari 1 jawaban

**Cara Menjawab**:
1. Baca pertanyaan (biasanya ada instruksi "Pilih semua yang benar")
2. Centang (☑) semua pilihan yang benar
3. Klik **"Check Answer"**
4. Sistem akan cek apakah semua jawaban benar sudah dipilih

**Mode Grading**:
- **Require All Correct ON**: Harus pilih SEMUA jawaban benar untuk dapat nilai
- **Require All Correct OFF**: Nilai dihitung per pilihan yang benar

**Contoh**:
```
Question: Manakah bilangan prima? (Pilih semua yang benar)
☑ 2  ← (Centang)
☐ 4
☑ 5  ← (Centang)
☐ 6
☑ 7  ← (Centang)

[Check Answer]
```

---

### 3. True/False (Benar/Salah)

**Tampilan**:
- Pernyataan
- 2 pilihan: True dan False

**Cara Menjawab**:
1. Baca pernyataan dengan teliti
2. Pilih **True** jika pernyataan benar, **False** jika salah
3. Klik **"Check Answer"**

**Contoh**:
```
Statement: Python adalah bahasa pemrograman yang dikembangkan oleh Guido van Rossum.

● True  ○ False

[Check Answer]
```

---

### 4. Short Answer (Jawaban Singkat)

**Tampilan**:
- Pertanyaan
- Text input box
- Kadang ada keterangan Case Sensitive atau tidak

**Cara Menjawab**:
1. Baca pertanyaan
2. Ketik jawaban di text box
3. Klik **"Check Answer"**
4. Sistem akan compare dengan jawaban yang benar

**Catatan**:
- Jika **Case Sensitive**: "Python" ≠ "python"
- Jika **Not Case Sensitive**: "Python" = "python" = "PYTHON"

**Contoh**:
```
Question: Siapa pencipta bahasa Python?

[Guido van Rossum] ← (Ketik di sini)

[Check Answer]
```

---

### 5. Essay (Esai)

**Tampilan**:
- Prompt/instruksi
- Text area besar untuk menulis jawaban
- Sample answer (contoh jawaban yang baik)

**Cara Menjawab**:
1. Baca prompt dengan teliti
2. Tulis jawaban Anda di text area
3. Klik **"Submit"** (tidak ada auto-grading)
4. Sample answer akan ditampilkan untuk referensi
5. Jawaban Anda akan disimpan untuk di-review pengajar

**Catatan**:
- Essay tidak di-grade otomatis
- Jawaban disimpan untuk di-review manual
- Bandingkan jawaban Anda dengan sample answer

**Contoh**:
```
Prompt: Jelaskan perbedaan antara list dan tuple dalam Python.

[Text area untuk menulis jawaban...]

[Submit]
```

---

### 6. Fill in the Blank (Isi Titik-Titik)

**Tampilan**:
- Template kalimat dengan blank (kotak input)
- Bisa single blank atau multi blank

**Cara Menjawab**:

#### Single Blank:
1. Baca kalimat
2. Isi blank dengan jawaban yang sesuai
3. Klik **"Check Answer"**

**Contoh Single Blank**:
```
Python dikembangkan oleh [________].

[Check Answer]
```

#### Multi Blank:
1. Baca kalimat dengan beberapa blank
2. Isi setiap blank dengan jawaban yang sesuai
3. Semua blank harus diisi
4. Klik **"Check Answer"**

**Contoh Multi Blank**:
```
[bahasa] dikembangkan oleh [pencipta] pada tahun [tahun].

Blank 1: [Python]
Blank 2: [Guido van Rossum]
Blank 3: [1991]

[Check Answer]
```

---

### 7. Multi-MC (Fill Blank dengan Dropdown)

**Tampilan**:
- Template kalimat dengan dropdown (▼)
- Setiap blank memiliki pilihan dropdown
- Pilih jawaban dari dropdown

**Cara Menjawab**:
1. Baca kalimat
2. Untuk setiap blank, klik dropdown (▼)
3. Pilih jawaban yang sesuai
4. Klik **"Check Answer"**

**Contoh**:
```
Bahasa [▼ Python/Java/C++] adalah bahasa [▼ compiled/interpreted/assembly].

Pilih: Python dan interpreted

[Check Answer]
```

---

### 8. Math Expression (Ekspresi Matematika)

**Tampilan**:
- Pertanyaan matematika
- MathQuill input field (dengan toolbar keyboard)
- Keyboard virtual untuk input matematika

**Cara Menjawab**:

1. **Menggunakan Keyboard Virtual**:
   - Klik tombol pada keyboard virtual untuk input simbol matematika
   - Tersedia: angka, operator (+, -, ×, ÷), power (^), subscript (_), dll.

2. **Menggunakan Keyboard Fisik**:
   - Ketik langsung (untuk angka dan operator dasar)
   - Gunakan shortcut:
     - `^` untuk power/pangkat
     - `_` untuk subscript
     - `/` untuk pecahan

3. **Navigasi dalam Expression**:
   - **Arrow keys**: Pindah cursor
   - **Backspace**: Hapus
   - **Tab**: Pindah ke field berikutnya

4. **Submit Jawaban**:
   - Klik **"Check Answer"**
   - Sistem akan evaluate ekspresi matematika

**Contoh Keyboard Virtual**:
```
Numbers:    [7] [8] [9] [^] [_]
            [4] [5] [6] [÷] [×]
            [1] [2] [3] [-] [+]
            [0] [.] [(] [)] [=]

Functions:  [sqrt] [sin] [cos] [tan]
Greek:      [α] [β] [π] [θ]
Navigation: [←] [→] [Backspace]
```

**Contoh Input**:
- Untuk x²: Ketik `x` lalu `^` lalu `2`
- Untuk √2: Klik tombol `sqrt` lalu ketik `2`
- Untuk ½: Ketik `1` lalu `/` lalu `2`

---

## Freestyle Practice Mode

Freestyle mode adalah mode latihan bebas di mana Anda bisa membuat soal matematika sendiri dan berlatih menyelesaikannya dengan sistem kredit.

### Cara Menggunakan Freestyle:

1. **Masuk ke Freestyle Mode**:
   - Klik **"Freestyle Practice"** di sidebar
   - Halaman freestyle akan terbuka

2. **Set Problem (Buat Soal)**:
   - Di field **"Problem"**, ketik soal matematika
   - Gunakan MathQuill keyboard untuk input matematika
   - Contoh: `2x + 5 = 11`, `x² - 4 = 0`
   - Klik **"Set Problem"**

3. **Solve Problem (Kerjakan Soal)**:
   - Soal akan ditampilkan di **"Problem Display"**
   - Masukkan jawaban Anda di field **"Answer"**
   - Klik **"Submit Attempt"**

4. **Feedback**:
   - ✅ **Correct**: Jawaban benar! (+kredit)
   - ❌ **Incorrect**: Jawaban salah, coba lagi
   - **Hints**: Sistem bisa memberikan hint

5. **Tombol Lainnya**:
   - **Get Structure String**: Untuk submit ke Moodle
   - **Give Up**: Menyerah, lihat jawaban (−kredit)
   - **Check Simplest Form**: Cek apakah jawaban sudah dalam bentuk paling sederhana
   - **Reset Problem**: Mulai ulang dengan soal baru

### Sistem Kredit:

**Credit Display** di bagian atas menampilkan:
- **Credit Balance**: Total kredit Anda saat ini
- **Earned**: Kredit yang diperoleh (dari jawaban benar)
- **Spent**: Kredit yang dipakai (dari give up atau hint)

**Cara Mendapat Kredit**:
- ✅ Jawab soal dengan benar: +10 kredit
- ✅ Jawab soal sulit: +20 kredit

**Cara Kehilangan Kredit**:
- ❌ Give up (menyerah): −5 kredit
- ℹ️ Minta hint: −2 kredit

**Credit History**:
- Klik **"Credit History"** untuk melihat riwayat
- Menampilkan semua transaksi kredit

### Keyboard Matematika di Freestyle:

**Accordion Sections**:
1. **Numbers & Basic**: Angka, operator dasar
2. **Functions**: sqrt, sin, cos, tan, log, ln
3. **Greek Letters**: α, β, γ, θ, π, dll.
4. **Advanced**: integral, summation, limit, matrix

**Cara Menggunakan**:
- Klik pada accordion untuk expand/collapse
- Klik tombol untuk insert simbol
- Gunakan navigation buttons untuk pindah cursor

---

## Navigasi dan Kontrol

### Sidebar Navigation:

**Menu Button (☰)**:
- Buka/tutup sidebar
- Otomatis tertutup di mobile

**Pages**:
1. **Problems**: Halaman utama dengan daftar soal
2. **Freestyle Practice**: Mode latihan bebas
3. **Load Problem Set**: Muat soal baru
4. **Submit Progress**: Export jawaban untuk submit
5. **Reset Answers**: Reset semua jawaban

### Problem Navigation:

**Di dalam Problem**:
- **Next Step**: Lanjut ke step berikutnya (setelah jawaban benar)
- **Previous Step**: Kembali ke step sebelumnya
- **Problem List**: Klik problem lain untuk pindah

**Step Transition**:
- Ada animasi transisi saat pindah step
- Banner menampilkan nomor step

### Keyboard Shortcuts:

- **Enter**: Submit jawaban (pada beberapa tipe soal)
- **Tab**: Pindah ke field berikutnya
- **Arrow Keys**: Navigasi dalam MathQuill input

---

## Export Progress

Export progress digunakan untuk mengirim jawaban Anda ke pengajar.

### Cara Export Progress:

1. **Klik "Submit Progress"** di sidebar
2. Halaman export akan terbuka
3. Ada 2 tab:

#### Tab 1: Progress Summary
- Menampilkan ringkasan progress Anda:
  - Problem Set UUID
  - Jumlah soal yang sudah dikerjakan
  - Score total
  - Timestamp

#### Tab 2: Export to File
1. Klik tombol **"📤 Export to File"**
2. File JSON akan di-download
3. File berisi:
   - Semua jawaban Anda
   - Score per problem
   - Timestamp pengerjaan
   - Problem Set UUID (untuk tracking)

### Format Export:

File JSON berisi:
```json
{
  "problem_set_uuid": "xxx-xxx-xxx",
  "student_name": "Your Name",
  "submission_time": "2025-11-25T12:00:00",
  "problems": [
    {
      "problem_id": "...",
      "steps": [
        {
          "answer": "...",
          "correct": true,
          "score": 10
        }
      ]
    }
  ],
  "total_score": 100
}
```

### Submit ke Pengajar:

1. Export file JSON
2. Kirim file ke pengajar via:
   - Email attachment
   - Learning Management System (LMS)
   - Cloud storage (Google Drive, OneDrive)
3. Pengajar akan import file untuk review dan grading

---

## Reset Answers

Reset digunakan untuk menghapus semua jawaban dan mulai dari awal.

### Cara Reset:

1. **Klik "Reset Answers"** di sidebar
2. Konfirmasi dialog akan muncul:
   ```
   ⚠️ Reset All Answers?

   This will clear all your answers and progress.
   Problem set will remain loaded.

   [Cancel] [Reset]
   ```
3. Klik **"Reset"** untuk confirm
4. Semua jawaban akan dihapus
5. Problem set tetap dimuat (tidak perlu load ulang)

### Yang Direset:

✅ **Direset**:
- Semua jawaban Anda
- Score/grade
- Progress per step

❌ **Tidak Direset**:
- Problem set yang dimuat
- Credit di freestyle mode (terpisah)

### Kapan Perlu Reset:

- Ingin mengerjakan ulang soal dari awal
- Testing sebelum ujian sebenarnya
- Latihan berulang dengan soal yang sama

---

## Tips dan Trik

### 1. Input Matematika dengan Cepat

**Menggunakan LaTeX Shortcut**:
- Ketik `\frac` untuk pecahan
- Ketik `\sqrt` untuk akar
- Ketik `\pi` untuk π
- Ketik `\alpha` untuk α

**Menggunakan Keyboard Fisik**:
- `^` untuk pangkat: `x^2` → x²
- `_` untuk subscript: `x_1` → x₁
- `/` untuk pecahan: `1/2` → ½
- `*` untuk perkalian: `2*x` → 2×x

### 2. Strategi Mengerjakan Soal

**Untuk Multiple Choice**:
- Baca semua pilihan sebelum menjawab
- Eliminasi pilihan yang jelas salah
- Jika ragu, tandai dan kembali lagi nanti

**Untuk Math Expression**:
- Cek ulang tanda (+ atau −)
- Pastikan kurung () berpasangan
- Simplify jawaban sebelum submit
- Gunakan "Check Simplest Form" di freestyle

**Untuk Fill in the Blank**:
- Perhatikan konteks kalimat
- Multi-blank: isi semua dulu baru submit
- Case sensitive: perhatikan huruf besar/kecil

### 3. Menggunakan Freestyle untuk Latihan

**Latihan Efektif**:
1. Mulai dengan soal mudah untuk dapat kredit
2. Secara bertahap tingkatkan kesulitan
3. Jangan terlalu sering give up (buang kredit)
4. Gunakan structure string untuk verifikasi

**Membuat Soal Sendiri**:
- Buat soal dari materi yang sulit
- Variasikan tipe soal (linear, quadratic, dll)
- Coba solve manual dulu sebelum set problem

### 4. Troubleshooting

**Jawaban Tidak Diterima**:
- Pastikan format benar (contoh: gunakan × bukan *, gunakan ÷ bukan /)
- Cek apakah sudah dalam bentuk paling sederhana
- Untuk pecahan: pastikan sudah disederhanakan
- Restart browser jika MathQuill error

**Problem Set Tidak Load**:
- Pastikan file JSON valid (dari export Problem Creator)
- Cek console browser (F12) untuk error
- Clear cache dan reload
- Pastikan koneksi internet aktif (untuk loading pertama)

**Keyboard Matematika Tidak Muncul**:
- Klik di dalam input field
- Refresh halaman
- Pastikan JavaScript enabled
- Coba browser lain (recommend Chrome/Firefox)

### 5. Mobile Usage

**Menggunakan di Mobile**:
- Sidebar otomatis tertutup untuk menghemat ruang
- Buka sidebar dengan tombol ☰ di kiri atas
- Keyboard virtual otomatis muncul
- Rotate ke landscape untuk layar lebih lebar

**Optimasi Mobile**:
- Gunakan zoom browser jika teks terlalu kecil
- Keyboard virtual lebih mudah dari keyboard fisik
- Collapse keyboard accordion yang tidak digunakan
- Export dari mobile: file akan ke Downloads folder

### 6. Best Practices

**Sebelum Mengerjakan**:
- Pastikan koneksi internet stabil (loading pertama)
- Download problem set dari pengajar
- Test dengan load problem set terlebih dahulu
- Backup file JSON problem set

**Saat Mengerjakan**:
- Jawaban otomatis tersimpan di localStorage
- Tidak perlu save manual
- Jangan clear browser data saat mengerjakan
- Kerjakan secara berurutan (problem 1, 2, 3, ...)

**Setelah Selesai**:
- Export progress segera
- Simpan file export sebagai backup
- Submit ke pengajar sebelum deadline
- Cek email konfirmasi dari pengajar (jika ada)

### 7. Performa dan Kecepatan

**Optimasi Loading**:
- Setelah loading pertama, app bekerja offline
- Library di-cache di browser
- Packages di-cache di IndexedDB
- Loading kedua jauh lebih cepat (< 5 detik)

**Menghemat Bandwidth**:
- Load Pyodide sekali, cache selamanya
- Problem set dalam bentuk JSON (kecil)
- Gambar dan aset di-cache otomatis

### 8. Keamanan dan Privacy

**Data Lokal**:
- Semua jawaban disimpan di localStorage browser
- Tidak ada data yang dikirim ke server (kecuali saat export)
- Clear browser data = hilang semua progress

**Export Safety**:
- File export hanya berisi jawaban dan score
- Tidak ada informasi pribadi (kecuali yang Anda isi)
- Enkripsi tidak diperlukan (data tidak sensitif)

---

## Informasi Tambahan

### Browser yang Didukung:
- ✅ **Google Chrome** (Recommended)
- ✅ **Mozilla Firefox**
- ✅ **Microsoft Edge**
- ✅ **Safari** (macOS/iOS)
- ⚠️ **Internet Explorer**: Tidak didukung

### Kapasitas dan Limits:
- **Problem Set**: Tidak ada limit jumlah soal
- **Answers**: Tersimpan di localStorage (~5-10 MB)
- **Offline Usage**: Setelah loading pertama, app 100% offline
- **Export File**: Ukuran tergantung jumlah soal (biasanya < 100 KB)

### Offline Capability:

**Setelah Loading Pertama**:
- ✅ Pyodide cached
- ✅ MathQuill cached
- ✅ All packages cached
- ✅ App dapat digunakan tanpa internet

**Yang Butuh Internet**:
- ❌ Loading pertama kali
- ❌ Update browser cache (jika clear cache)

### Compatibility:

**Desktop**:
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu, Fedora, dll.)

**Mobile**:
- Android 8.0+
- iOS 13+
- Responsive design

**Screen Size**:
- Minimum: 320px (mobile)
- Optimal: 768px+ (tablet/desktop)

---

## Dukungan dan Bantuan

### Jika Mengalami Masalah:

1. **Cek Console Browser**:
   - Tekan `F12` (Windows/Linux) atau `Cmd+Option+I` (Mac)
   - Lihat tab "Console" untuk error messages
   - Screenshot error dan kirim ke pengajar

2. **Troubleshooting Umum**:
   - Refresh halaman (`Ctrl+R` atau `Cmd+R`)
   - Clear cache (`Ctrl+Shift+Delete`)
   - Restart browser
   - Coba browser lain

3. **Export Backup**:
   - Selalu export progress secara berkala
   - Simpan file export sebagai backup
   - Jika browser crash, import progress dari file

4. **Kontak Pengajar**:
   - Kirim screenshot error
   - Sertakan file problem set JSON
   - Jelaskan langkah-langkah yang sudah dicoba

---

## FAQ (Frequently Asked Questions)

**Q: Apakah jawaban tersimpan otomatis?**
A: Ya, semua jawaban tersimpan otomatis di localStorage browser.

**Q: Bagaimana jika browser crash?**
A: Jawaban tetap tersimpan. Buka ulang browser dan load problem set kembali.

**Q: Bisa mengerjakan di 2 device berbeda?**
A: Tidak disarankan. Export dari device 1, import ke device 2 jika perlu.

**Q: Apakah bisa edit jawaban setelah submit?**
A: Ya, bisa. Jawaban bisa diubah kapan saja sebelum export final.

**Q: Bagaimana cara submit ke pengajar?**
A: Export progress → kirim file JSON ke pengajar via email/LMS.

**Q: Apakah ada time limit?**
A: Tidak ada time limit di aplikasi. Time limit (jika ada) ditentukan oleh pengajar.

**Q: Bisa mengerjakan offline?**
A: Ya, setelah loading pertama kali, app bisa digunakan 100% offline.

**Q: Bagaimana cara input √2?**
A: Klik tombol `sqrt` di keyboard, atau ketik `\sqrt{2}` di MathQuill.

**Q: Essay di-grade otomatis?**
A: Tidak. Essay disimpan untuk di-review manual oleh pengajar.

**Q: Credit di freestyle untuk apa?**
A: Gamification untuk motivasi latihan. Tidak mempengaruhi grade sebenarnya.

---

**Catatan**: Panduan ini dibuat untuk versi terbaru dari Problem Solver (NoNet-NoSet-NoChat). Beberapa fitur mungkin berbeda jika menggunakan versi yang berbeda.

---

*Panduan ini dibuat dengan Claude Code - Anthropic*
