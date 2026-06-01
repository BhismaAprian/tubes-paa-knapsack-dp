import time
from typing import List, Dict, Any


# ─────────────────────────────────────────────
#  FUNGSI UTAMA DP
# ─────────────────────────────────────────────

def solve(matkul_list: List[Dict], batas_sks: int) -> Dict[str, Any]:
    """
    Menyelesaikan masalah pemilihan mata kuliah optimal
    menggunakan algoritma Dynamic Programming (0/1 Knapsack).

    Parameter:
        matkul_list : list dict berisi 'nama', 'sks', 'ekspektasi_nilai'
        batas_sks   : batas maksimal SKS yang boleh diambil

    Return:
        dict berisi matkul dipilih, total SKS, ekspektasi IPK,
        tabel DP, dan analisis kompleksitas.3
    """
    start_time = time.perf_counter()

    n = len(matkul_list)

    # ── Bangun tabel DP ──────────────────────────────────────────────────
    # dp[i][s] = bobot IPK tertinggi dengan mempertimbangkan i matkul pertama
    #            dan total SKS = s
    # Bobot = ekspektasi_nilai × SKS (agar SKS yang lebih besar diberi bobot proporsional)
    dp = [[0.0] * (batas_sks + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        sks_i   = matkul_list[i - 1]["sks"]
        nilai_i = matkul_list[i - 1]["ekspektasi_nilai"]
        bobot_i = nilai_i * sks_i  # bobot kontribusi

        for s in range(batas_sks + 1):
            # Pilihan 1: Skip matkul ke-i
            dp[i][s] = dp[i - 1][s]

            # Pilihan 2: Ambil matkul ke-i (jika kapasitas SKS mencukupi)
            if s >= sks_i:
                nilai_ambil = dp[i - 1][s - sks_i] + bobot_i
                if nilai_ambil > dp[i][s]:
                    dp[i][s] = nilai_ambil

    # ── Traceback: cari matkul mana yang dipilih ─────────────────────────
    dipilih = []
    s = batas_sks
    for i in range(n, 0, -1):
        if abs(dp[i][s] - dp[i - 1][s]) > 1e-9:   # floating-point safe compare
            dipilih.append(matkul_list[i - 1])
            s -= matkul_list[i - 1]["sks"]

    # ── Hitung ringkasan hasil ───────────────────────────────────────────
    total_sks   = sum(m["sks"] for m in dipilih)
    total_bobot = dp[n][batas_sks]
    ekspektasi_ipk = round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    return {
        "dipilih"          : dipilih,
        "tidak_dipilih"    : [m for m in matkul_list if m not in dipilih],
        "total_sks"        : total_sks,
        "ekspektasi_ipk"   : ekspektasi_ipk,
        "total_bobot"      : round(total_bobot, 2),
        "tabel_dp"         : dp,
        "n_matkul"         : n,
        "batas_sks"        : batas_sks,
        "waktu_eksekusi_ms": elapsed_ms,
        # Analisis kompleksitas
        "kompleksitas_waktu": f"O(n × W) = O({n} × {batas_sks}) = O({n * batas_sks})",
        "kompleksitas_ruang": f"O(n × W) = O({n} × {batas_sks}) = O({n * batas_sks})",
    }


# ─────────────────────────────────────────────
#  FUNGSI UTILITAS
# ─────────────────────────────────────────────

def format_tabel_dp(tabel_dp: List[List[float]], n: int, batas_sks: int) -> List[List[str]]:
    """Mengubah tabel DP float menjadi string rapi untuk ditampilkan."""
    header = ["Matkul ke-i \\ SKS →"] + [str(s) for s in range(batas_sks + 1)]
    rows   = [header]
    for i in range(n + 1):
        label = f"i = {i}" if i > 0 else "Awal (i=0)"
        row   = [label] + [f"{v:.1f}" for v in tabel_dp[i]]
        rows.append(row)
    return rows


def hitung_skenario_kompleksitas(matkul_list: List[Dict]) -> List[Dict]:
    """
    Menghasilkan data kompleksitas untuk berbagai batas SKS
    (digunakan untuk grafik analisis).
    """
    hasil = []
    for batas in range(4, 25, 2):
        start = time.perf_counter()
        solve(matkul_list, batas)
        elapsed = (time.perf_counter() - start) * 1000
        hasil.append({
            "batas_sks"    : batas,
            "operasi"      : len(matkul_list) * batas,
            "waktu_ms"     : round(elapsed, 4),
        })
    return hasil


# ─────────────────────────────────────────────
#  QUICK TEST (jalankan langsung: python dp_solver.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import json, os

    with open(os.path.join("data", "matkul.json")) as f:
        data = json.load(f)

    hasil = solve(data, batas_sks=10)

    print("=" * 50)
    print("HASIL OPTIMASI MATKUL (DP)")
    print("=" * 50)
    print(f"Batas SKS      : {hasil['batas_sks']}")
    print(f"Total SKS      : {hasil['total_sks']}")
    print(f"Ekspektasi IPK : {hasil['ekspektasi_ipk']:.2f}")
    print(f"Waktu eksekusi : {hasil['waktu_eksekusi_ms']} ms")
    print(f"Kompleksitas   : {hasil['kompleksitas_waktu']}")
    print("\nMata kuliah dipilih:")
    for m in hasil["dipilih"]:
        print(f"  ✓ {m['nama']} ({m['sks']} SKS, nilai {m['ekspektasi_nilai']})")
