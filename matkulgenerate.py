import json
import random

def generate_courses():
    dataset = {}
    
    # Kumpulan topik berdasarkan tingkat semester untuk Sistem Informasi / Informatika
    topics_smt_1_2 = ["Kalkulus", "Aljabar Linear", "Pengantar Sistem Informasi", "Fisika Dasar", 
                      "Matematika Diskrit", "Logika Informatika", "Pemrograman Dasar", "Pancasila", 
                      "Bahasa Inggris", "Kewarganegaraan", "Literasi Digital", "Konsep Teknologi",
                      "Keterampilan Interpersonal", "Pengantar Manajemen", "Algoritma Pemrograman"]
                      
    topics_smt_3_4 = ["Struktur Data", "Jaringan Komputer", "Sistem Operasi", "Basis Data", 
                      "Pemrograman Berorientasi Objek (Java)", "Rekayasa Perangkat Lunak", 
                      "Arsitektur Komputer", "Analisis Proses Bisnis", "Desain Antarmuka",
                      "Statistika Probabilitas", "Sistem Informasi Manajemen", "Pengembangan Web",
                      "Pemrograman Lanjut", "Manajemen Proyek TI", "Keamanan Informasi Dasar"]
                      
    topics_smt_5_6 = ["Machine Learning", "Data Science", "Kriptografi", "Web Security", 
                      "Perancangan dan Analisis Algoritma", "Keamanan Siber", "Kecerdasan Buatan", 
                      "Data Mining", "Cloud Computing", "Internet of Things", "Audit Sistem Informasi",
                      "Tata Kelola TI", "Pengujian Perangkat Lunak", "Etika Profesi", "Sistem Enterprise"]
                      
    topics_smt_7_8 = ["Metodologi Penelitian", "Kerja Praktik", "Skripsi", "Seminar Proposal", 
                      "Kapita Selekta", "Technopreneurship", "Manajemen Risiko TI", "Sertifikasi Profesional",
                      "Proyek Independen", "Publikasi Ilmiah"]

    modifiers = ["Teori", "Praktikum", "Proyek", "Studi Kasus", "Terapan", "Lanjut", "Dasar"]

    course_id = 1

    for semester in range(1, 9):
        semester_data = []
        target_courses = 40 if semester <= 6 else 10
        
        # Pilih base topic sesuai rentang semester
        if semester in [1, 2]: base_topics = topics_smt_1_2
        elif semester in [3, 4]: base_topics = topics_smt_3_4
        elif semester in [5, 6]: base_topics = topics_smt_5_6
        else: base_topics = topics_smt_7_8

        # Generate matkul hingga mencapai target_courses
        generated_names = set()
        while len(generated_names) < target_courses:
            topic = random.choice(base_topics)
            # Acak nama agar unik (misal: "Praktikum Jaringan Komputer")
            if random.random() > 0.4 and semester <= 6:
                modifier = random.choice(modifiers)
                if random.random() > 0.5:
                    course_name = f"{modifier} {topic}"
                else:
                    course_name = f"{topic} {modifier}"
            else:
                course_name = topic
                
            # Pastikan nama unik di semester ini, jika duplikat, tambahkan angka
            if course_name in generated_names:
                course_name = f"{course_name} {random.randint(1, 5)}"
                
            generated_names.add(course_name)

        # Buat format dictionary untuk setiap matkul
        for name in generated_names:
            # SKS realistis antara 2 sampai 4
            sks = random.choice([2, 3, 3, 4]) 
            # Nilai prioritas/bobot matkul (skala 10-100)
            prioritas = random.randint(50, 100) if sks >= 3 else random.randint(10, 60)
            
            semester_data.append({
                "id": f"MK{course_id:03d}",
                "nama_matkul": name,
                "sks": sks,
                "prioritas": prioritas
            })
            course_id += 1
            
        dataset[f"Semester {semester}"] = semester_data

    return dataset

# Jalankan dan simpan ke JSON
data_matkul = generate_courses()
with open('dataset_matkul.json', 'w') as f:
    json.dump(data_matkul, f, indent=4)

print("Dataset berhasil dibuat: dataset_matkul.json dengan total 260 matkul.")