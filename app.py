"""
app.py  —  Tubes Besar: Optimasi Pemilihan Mata Kuliah
=======================================================
Algoritma Dynamic Programming (0/1 Knapsack)
Antarmuka  : Streamlit (web)
Jalankan   : streamlit run app.py

Kelompok   : [Nama Kelompok]
Anggota    :
    1. [Nama A1] — Algoritma DP
    2. [Nama A2] — Data & Pengujian
    3. [Nama A3] — Visualisasi & UI
    4. [Nama A4] — Laporan & Dokumentasi
"""

import json
import os
import time

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dp_solver import solve, hitung_skenario_kompleksitas

# ─────────────────────────────────────────────
#  KONFIGURASI HALAMAN
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Optimasi Matkul — DP",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────

@st.cache_data
def load_matkul():
    path = os.path.join(os.path.dirname(__file__), "data", "matkul.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

MATKUL_DEFAULT = load_matkul()

# ─────────────────────────────────────────────
#  SIDEBAR — INPUT & NAVIGASI
# ─────────────────────────────────────────────

with st.sidebar:
    st.title("⚙️ Pengaturan")
    st.markdown("---")

    st.subheader("📚 Batas SKS")
    batas_sks = st.slider(
        "Maksimal SKS yang bisa diambil",
        min_value=4,
        max_value=24,
        value=10,
        step=1,
        help="Sesuaikan dengan aturan fakultas / kondisi kamu."
    )

    st.markdown("---")
    st.subheader("📋 Daftar Mata Kuliah")
    st.caption("Edit ekspektasi nilai sesuai kemampuanmu.")

    # Tabel editable matkul
    df_edit = pd.DataFrame(MATKUL_DEFAULT)
    df_edit = df_edit[["nama", "sks", "ekspektasi_nilai"]]
    df_edit.columns = ["Mata Kuliah", "SKS", "Ekspektasi Nilai"]

    edited_df = st.data_editor(
        df_edit,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "SKS"              : st.column_config.NumberColumn(min_value=1, max_value=6, step=1),
            "Ekspektasi Nilai" : st.column_config.NumberColumn(min_value=0.0, max_value=4.0, step=0.1, format="%.1f"),
        },
        hide_index=True,
    )

    matkul_list = [
        {
            "nama"             : row["Mata Kuliah"],
            "sks"              : int(row["SKS"]),
            "ekspektasi_nilai" : float(row["Ekspektasi Nilai"]),
        }
        for _, row in edited_df.iterrows()
        if row["Mata Kuliah"] and row["SKS"] > 0
    ]

    st.markdown("---")
    tombol = st.button("🚀 Hitung Kombinasi Optimal", type="primary", use_container_width=True)

    st.markdown("---")
    st.caption("Algoritma: 0/1 Knapsack DP\nKompleksitas: O(n × W)")

# ─────────────────────────────────────────────
#  HEADER UTAMA
# ─────────────────────────────────────────────

st.title("🎓 Optimasi Pemilihan Mata Kuliah")
st.markdown(
    "**Algoritma Dynamic Programming** · 0/1 Knapsack Problem  \n"
    "Menentukan kombinasi mata kuliah pilihan yang **memaksimalkan ekspektasi IPK** "
    "dengan batasan SKS yang tersedia."
)
st.markdown("---")

# ─────────────────────────────────────────────
#  NAVIGASI TAB
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Hasil Optimal",
    "🧮 Tabel DP",
    "📈 Analisis Kompleksitas",
    "📖 Penjelasan Algoritma",
])

# ════════════════════════════════════════════════════════
#  TAB 1 — HASIL OPTIMAL
# ════════════════════════════════════════════════════════

with tab1:
    if not tombol:
        st.info("👈 Atur parameter di sidebar, lalu tekan **Hitung Kombinasi Optimal**.")
    else:
        if len(matkul_list) == 0:
            st.error("❌ Tidak ada data mata kuliah. Tambahkan di sidebar.")
        else:
            with st.spinner("Menjalankan algoritma DP..."):
                time.sleep(0.3)   # animasi loading kecil
                hasil = solve(matkul_list, batas_sks)

            st.success("✅ Optimasi selesai!")

            # ── Metric cards ─────────────────────────────────────────────
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📚 Matkul Dipilih",    len(hasil["dipilih"]))
            col2.metric("📋 Total SKS",          hasil["total_sks"], f"dari {batas_sks} SKS")
            col3.metric("⭐ Ekspektasi IPK",     f"{hasil['ekspektasi_ipk']:.2f}", "skala 4.0")
            col4.metric("⚡ Waktu Eksekusi",     f"{hasil['waktu_eksekusi_ms']} ms")

            st.markdown("---")

            # ── Dua kolom: dipilih vs tidak dipilih ──────────────────────
            left, right = st.columns(2)

            with left:
                st.subheader("✅ Mata Kuliah Dipilih")
                if hasil["dipilih"]:
                    df_dipilih = pd.DataFrame(hasil["dipilih"])
                    df_dipilih = df_dipilih.rename(columns={
                        "nama": "Mata Kuliah",
                        "sks": "SKS",
                        "ekspektasi_nilai": "Ekspektasi Nilai",
                        "kategori": "Kategori",
                    })
                    df_dipilih = df_dipilih[[
                        "Mata Kuliah",
                        "SKS",
                        "Ekspektasi Nilai",
                    ]]
                    df_dipilih["Bobot (Nilai×SKS)"] = (
                        df_dipilih["Ekspektasi Nilai"] * df_dipilih["SKS"]
                    ).round(1)
                    st.dataframe(df_dipilih, use_container_width=True, hide_index=True)
                    st.caption(f"Total: {hasil['total_sks']} SKS | Bobot total: {hasil['total_bobot']:.1f}")
                else:
                    st.warning("Tidak ada matkul yang dipilih.")

            with right:
                st.subheader("❌ Mata Kuliah Tidak Dipilih")
                if hasil["tidak_dipilih"]:
                    df_tidak = pd.DataFrame(hasil["tidak_dipilih"])
                    if "kategori" in df_tidak.columns:
                        df_tidak = df_tidak[["nama", "sks", "ekspektasi_nilai"]]
                    df_tidak.columns = ["Mata Kuliah", "SKS", "Ekspektasi Nilai"]
                    st.dataframe(df_tidak, use_container_width=True, hide_index=True)
                else:
                    st.success("Semua matkul berhasil masuk dalam batas SKS!")

            st.markdown("---")

            # ── Grafik perbandingan ───────────────────────────────────────
            st.subheader("📊 Visualisasi Pemilihan Matkul")

            semua = pd.DataFrame(matkul_list)
            semua["Status"] = semua["nama"].apply(
                lambda n: "Dipilih" if any(m["nama"] == n for m in hasil["dipilih"]) else "Tidak Dipilih"
            )
            semua["Bobot"] = (semua["ekspektasi_nilai"] * semua["sks"]).round(2)

            fig_bar = px.bar(
                semua,
                x="nama",
                y="Bobot",
                color="Status",
                color_discrete_map={"Dipilih": "#1D9E75", "Tidak Dipilih": "#B4B2A9"},
                labels={"nama": "Mata Kuliah", "Bobot": "Bobot (Nilai × SKS)"},
                title="Perbandingan Bobot Setiap Mata Kuliah",
            )
            fig_bar.update_layout(xaxis_tickangle=-30, legend_title="Status")
            st.plotly_chart(fig_bar, use_container_width=True)

            # ── Pie chart distribusi SKS ──────────────────────────────────
            col_pie1, col_pie2 = st.columns(2)

            with col_pie1:
                df_pie = pd.DataFrame({
                    "Kategori": ["SKS Terpakai", "SKS Sisa"],
                    "Nilai"   : [hasil["total_sks"], batas_sks - hasil["total_sks"]],
                })
                fig_pie = px.pie(
                    df_pie, values="Nilai", names="Kategori",
                    title="Distribusi SKS",
                    color_discrete_map={"SKS Terpakai": "#1D9E75", "SKS Sisa": "#D3D1C7"},
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_pie2:
                if hasil["dipilih"]:
                    df_sks = pd.DataFrame(hasil["dipilih"])
                    fig_sks = px.pie(
                        df_sks, values="sks", names="nama",
                        title="Proporsi SKS Matkul Dipilih",
                    )
                    st.plotly_chart(fig_sks, use_container_width=True)

# ════════════════════════════════════════════════════════
#  TAB 2 — TABEL DP
# ════════════════════════════════════════════════════════

with tab2:
    if not tombol:
        st.info("👈 Jalankan optimasi di Tab **Hasil Optimal** terlebih dahulu.")
    else:
        st.subheader("🧮 Tabel Dynamic Programming")
        st.markdown(
            "Setiap sel `dp[i][s]` = **bobot IPK tertinggi** dengan mempertimbangkan "
            "`i` mata kuliah pertama dan total SKS = `s`."
        )

        tabel = hasil["tabel_dp"]
        n     = hasil["n_matkul"]
        W     = hasil["batas_sks"]

        # Buat DataFrame untuk ditampilkan
        col_names = [f"SKS={s}" for s in range(W + 1)]
        row_names = ["Awal"] + [matkul_list[i]["nama"][:15] for i in range(n)]

        df_dp = pd.DataFrame(tabel, columns=col_names, index=row_names)
        df_dp = df_dp.round(2)

        st.dataframe(
            df_dp.style.background_gradient(cmap="Greens", axis=None),
            use_container_width=True,
            height=min(400, (n + 2) * 36),
        )

        st.caption(
            f"Ukuran tabel: ({n+1}) baris × ({W+1}) kolom = {(n+1)*(W+1)} sel  |  "
            f"Nilai optimal (pojok kanan bawah): **{tabel[n][W]:.2f}**"
        )

        # ── Heatmap interaktif ────────────────────────────────────────────
        st.subheader("🌡️ Heatmap Tabel DP")
        fig_heat = go.Figure(data=go.Heatmap(
            z          = [[tabel[i][s] for s in range(W + 1)] for i in range(n + 1)],
            x          = [f"SKS={s}" for s in range(W + 1)],
            y          = row_names,
            colorscale = "Teal",
            hoverongaps= False,
        ))
        fig_heat.update_layout(
            title  = "Heatmap Nilai DP (semakin gelap = semakin optimal)",
            height = max(300, (n + 1) * 40),
        )
        st.plotly_chart(fig_heat, use_container_width=True)

        # ── Penjelasan traceback ──────────────────────────────────────────
        st.subheader("🔍 Proses Traceback")
        st.markdown("Pelacakan mundur untuk menemukan kombinasi matkul yang dipilih:")

        steps = []
        s_cur = W
        for i in range(n, 0, -1):
            nama = matkul_list[i - 1]["nama"]
            sks  = matkul_list[i - 1]["sks"]
            if abs(tabel[i][s_cur] - tabel[i - 1][s_cur]) > 1e-9:
                steps.append(f"✅ **i={i}** ({nama}): dp[{i}][{s_cur}]={tabel[i][s_cur]:.1f} ≠ dp[{i-1}][{s_cur}]={tabel[i-1][s_cur]:.1f} → **DIPILIH**, SKS sisa {s_cur}→{s_cur-sks}")
                s_cur -= sks
            else:
                steps.append(f"⬜ **i={i}** ({nama}): dp[{i}][{s_cur}]={tabel[i][s_cur]:.1f} = dp[{i-1}][{s_cur}]={tabel[i-1][s_cur]:.1f} → skip")

        for step in steps:
            st.markdown(step)

# ════════════════════════════════════════════════════════
#  TAB 3 — ANALISIS KOMPLEKSITAS
# ════════════════════════════════════════════════════════

with tab3:
    st.subheader("📈 Analisis Kompleksitas Algoritma")

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
**Kompleksitas Waktu: O(n × W)**
- `n` = jumlah mata kuliah
- `W` = batas SKS (kapasitas)
- Dua nested loop → setiap sel dihitung satu kali

**Kompleksitas Ruang: O(n × W)**
- Tabel DP berukuran `(n+1) × (W+1)`
- Bisa dioptimasi ke **O(W)** dengan 1D array
        """)

    with col_r:
        st.markdown("""
**Sifat Algoritma:**
- ✅ Pseudo-polynomial time
- ✅ Optimal substructure
- ✅ Overlapping subproblems
- ✅ Solusi selalu optimal (bukan heuristik)

**Perbandingan dengan Greedy:**
| | DP | Greedy |
|---|---|---|
| Keoptimalan | ✅ Selalu optimal | ❌ Tidak selalu |
| Kompleksitas | O(n×W) | O(n log n) |
        """)

    st.markdown("---")

    # ── Grafik pertumbuhan kompleksitas ───────────────────────────────────
    st.subheader("📉 Grafik Pertumbuhan Jumlah Operasi vs Batas SKS")

    with st.spinner("Menghitung skenario kompleksitas..."):
        data_k = hitung_skenario_kompleksitas(matkul_list if matkul_list else MATKUL_DEFAULT)

    df_k = pd.DataFrame(data_k)

    fig_k = px.line(
        df_k, x="batas_sks", y="operasi",
        markers=True,
        labels={"batas_sks": "Batas SKS (W)", "operasi": "Jumlah Operasi (n × W)"},
        title=f"Pertumbuhan Operasi DP (n={len(matkul_list or MATKUL_DEFAULT)} matkul)",
        color_discrete_sequence=["#1D9E75"],
    )
    fig_k.update_traces(marker_size=8)
    st.plotly_chart(fig_k, use_container_width=True)

    # ── Grafik waktu eksekusi ─────────────────────────────────────────────
    st.subheader("⏱️ Grafik Waktu Eksekusi Aktual")

    fig_t = px.bar(
        df_k, x="batas_sks", y="waktu_ms",
        labels={"batas_sks": "Batas SKS (W)", "waktu_ms": "Waktu (ms)"},
        title="Waktu Eksekusi Nyata per Skenario",
        color="waktu_ms",
        color_continuous_scale="Teal",
    )
    st.plotly_chart(fig_t, use_container_width=True)

    # ── Tabel skenario uji ────────────────────────────────────────────────
    st.subheader("📋 Tabel Skenario Pengujian")

    skenario_labels = []
    for row in data_k:
        if row["batas_sks"] <= 8:
            skenario_labels.append("Kecil")
        elif row["batas_sks"] <= 16:
            skenario_labels.append("Sedang")
        else:
            skenario_labels.append("Besar")

    df_k["Skenario"]  = skenario_labels
    df_k.columns      = ["Batas SKS", "Jumlah Operasi", "Waktu (ms)", "Skenario"]
    st.dataframe(df_k[["Skenario", "Batas SKS", "Jumlah Operasi", "Waktu (ms)"]],
                 use_container_width=True, hide_index=True)

# ════════════════════════════════════════════════════════
#  TAB 4 — PENJELASAN ALGORITMA
# ════════════════════════════════════════════════════════

with tab4:
    st.subheader("📖 Penjelasan Algoritma Dynamic Programming")

    st.markdown("""
### 1. Konsep Dasar

Masalah pemilihan mata kuliah ini adalah variasi dari **0/1 Knapsack Problem**:

| Knapsack Klasik | Masalah Matkul |
|---|---|
| Kapasitas tas (W) | Batas SKS semester |
| Barang ke-i | Mata kuliah ke-i |
| Berat barang | SKS mata kuliah |
| Nilai barang | Ekspektasi Nilai × SKS |
| Ambil atau tidak (0/1) | Ambil atau skip matkul |

---

### 2. Formulasi Matematis

**Definisi subproblem:**

```
dp[i][s] = bobot IPK tertinggi dengan mempertimbangkan
           i mata kuliah pertama dan total SKS = s
```

**Recurrence Relation:**

```
dp[i][s] = max(
    dp[i-1][s],                              ← skip matkul ke-i
    dp[i-1][s - sks[i]] + nilai[i] × sks[i] ← ambil matkul ke-i
)

Syarat ambil: s >= sks[i]
```

**Base case:**
```
dp[0][s] = 0  untuk semua s  (belum ada matkul dipertimbangkan)
```

---

### 3. Pseudocode

```
FUNGSI solve(matkul[], batas_sks):
    n  ← panjang matkul
    dp ← array (n+1) × (batas_sks+1), isi 0

    UNTUK i dari 1 sampai n:
        sks_i   ← matkul[i].sks
        bobot_i ← matkul[i].nilai × sks_i

        UNTUK s dari 0 sampai batas_sks:
            dp[i][s] ← dp[i-1][s]              // default: skip
            JIKA s >= sks_i:
                ambil ← dp[i-1][s-sks_i] + bobot_i
                JIKA ambil > dp[i][s]:
                    dp[i][s] ← ambil            // update: ambil

    KEMBALIKAN dp[n][batas_sks]

FUNGSI traceback(dp, matkul[], batas_sks):
    dipilih ← []
    s       ← batas_sks

    UNTUK i dari n sampai 1:
        JIKA dp[i][s] ≠ dp[i-1][s]:
            tambah matkul[i] ke dipilih
            s ← s - matkul[i].sks

    KEMBALIKAN dipilih
```

---

### 4. Contoh Kecil (Manual)

Misalnya ada 3 matkul, batas 5 SKS:

| Matkul | SKS | Nilai | Bobot |
|---|---|---|---|
| A | 2 | 4.0 | 8.0 |
| B | 3 | 3.5 | 10.5 |
| C | 2 | 3.7 | 7.4 |

Tabel DP:

```
         SKS=0  SKS=1  SKS=2  SKS=3  SKS=4  SKS=5
Awal      0.0    0.0    0.0    0.0    0.0    0.0
+ A (2)   0.0    0.0    8.0    8.0    8.0    8.0
+ B (3)   0.0    0.0    8.0    10.5   10.5   18.5
+ C (2)   0.0    0.0    8.0    10.5   15.4   18.5
```

Hasil: **A + B = 18.5** → SKS 2+3=5, IPK = 18.5/5 = **3.70**

---

### 5. Mengapa DP Lebih Baik dari Greedy?

Greedy (pilih bobot per SKS terbesar dulu) **tidak selalu optimal** karena tidak
mempertimbangkan kombinasi antar item. DP menjamin solusi **selalu optimal** dengan
menyimpan hasil subproblem yang sudah dihitung (*memoization*).
    """)

    st.markdown("---")
    st.subheader("🔗 Referensi")
    st.markdown("""
- Cormen, T.H. et al. *Introduction to Algorithms* (CLRS), 3rd ed. — Bab 15: Dynamic Programming
- Kleinberg, J. & Tardos, E. *Algorithm Design* — Bab 6: Dynamic Programming
- GeeksforGeeks. [0-1 Knapsack Problem](https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/)
    """)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────

st.markdown("---")
st.caption(
    "Tubes Besar · Analisis dan Desain Algoritma · "
    "Algoritma: Dynamic Programming (0/1 Knapsack) · "
    "Built with Python & Streamlit"
)
