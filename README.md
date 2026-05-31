# Tubes Besar — Optimasi Pemilihan Mata Kuliah
## Algoritma Dynamic Programming (0/1 Knapsack)

---

## Cara Menjalankan

### 1. Install dependency
```bash
pip install -r requirements.txt
```

### 2. Jalankan aplikasi
```bash
streamlit run app.py
```

### 3. Buka browser
Browser akan otomatis terbuka di `http://localhost:8501`

---

## Struktur File

```
tubes-dp/
├── app.py              ← Antarmuka Streamlit (Anggota 3)
├── dp_solver.py        ← Algoritma DP inti (Anggota 1)
├── requirements.txt    ← Library yang dibutuhkan
├── README.md           ← Panduan ini
└── data/
    └── matkul.json     ← Dataset mata kuliah (Anggota 2)
```

---

## Pembagian Tugas

| Anggota | File Utama | Tanggung Jawab |
|---|---|---|
| Anggota 1 | `dp_solver.py` | Algoritma DP, traceback, analisis kompleksitas |
| Anggota 2 | `data/matkul.json` | Dataset, skenario pengujian, validasi output |
| Anggota 3 | `app.py` | Antarmuka Streamlit, grafik, visualisasi tabel DP |
| Anggota 4 | Laporan | Dokumentasi, penjelasan algoritma, daftar pustaka |

---

## Test Cepat Algoritma (tanpa Streamlit)

```bash
python dp_solver.py
```

---

## Skenario Pengujian

| Skenario | Batas SKS | Jumlah Matkul |
|---|---|---|
| Kecil | 6 SKS | 10 matkul |
| Sedang | 12 SKS | 10 matkul |
| Besar | 20 SKS | 10 matkul |
# tubes-paa-knapsack-dp
