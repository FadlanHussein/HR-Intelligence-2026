# Data Dictionary — Recruitment Intelligence

## Dataset Overview

| Item                    | Value                                                  |
| :---------------------- | :----------------------------------------------------- |
| **File Path**           | `data/raw/recruitment_mydata.csv`                      |
| **Total Records**       | 1,500 rows                                             |
| **Total Columns**       | 11 columns                                             |
| **Missing Cells**       | 7 cells (1 per column across 7 features)               |
| **Duplicate Rows**      | 0 rows                                                 |
| **Target Distribution** | Not Hired (0): 1,035 (69.0%) \| Hired (1): 465 (31.0%) |

---

## Variables

| Column                | Data Type | Description                             | Expected Values / Range                                         | Role                  |
| :-------------------- | :-------- | :-------------------------------------- | :-------------------------------------------------------------- | :-------------------- |
| `Age`                 | `float64` | Usia kandidat pelamar                   | 20 – 50 tahun                                                   | Candidate Attribute   |
| `Gender`              | `str`     | Jenis kelamin kandidat                  | `Female`, `Male`                                                | Candidate Attribute   |
| `EducationLevel`      | `str`     | Tingkat pendidikan formal terakhir      | `Bachelor's (Type 1)`, `Bachelor's (Type 2)`, `Master's`, `PhD` | Candidate Attribute   |
| `ExperienceYears`     | `float64` | Lama pengalaman kerja profesional       | 0 – 15 tahun                                                    | Candidate Attribute   |
| `PreviousCompanies`   | `int64`   | Jumlah perusahaan tempat pernah bekerja | 1 – 5 perusahaan                                                | Candidate Attribute   |
| `DistanceFromCompany` | `float64` | Jarak tempat tinggal kandidat ke kantor | ~1.03 – 50.99 (km)                                              | Candidate Attribute   |
| `InterviewScore`      | `float64` | Nilai hasil interview kandidat          | 0 – 100                                                         | Assessment Score      |
| `SkillScore`          | `float64` | Nilai kemampuan kandidat                | 0 – 100                                                         | Assessment Score      |
| `PersonalityScore`    | `float64` | Nilai penilaian kepribadian kandidat    | 0 – 100                                                         | Assessment Score      |
| `RecruitmentStrategy` | `str`     | Strategi recruitment yang digunakan     | `Aggressive`, `Moderate`, `Conservative`                        | Recruitment Attribute |
| `HiringDecision`      | `int64`   | Keputusan akhir recruitment             | `0` = Not Hired, `1` = Hired                                    | Target / Outcome      |

---

## Notes & Observations

- **Target Imbalance**: Sekitar 69% kandidat berstatus _Not Hired_ dan 31% _Hired_.
- **Missing Values**: Terdapat 7 sel kosong (_NaN_) yang tersebar masing-masing 1 baris pada kolom: `Age`, `EducationLevel`, `ExperienceYears`, `InterviewScore`, `SkillScore`, `PersonalityScore`, dan `RecruitmentStrategy`.
- **Data Types**: Kolom numerik diskrit seperti `Age` dan `ExperienceYears` terbaca sebagai `float64` karena adanya nilai _NaN_ pada data mentah.

## Database Purpose

Database Recruitment Intelligence dirancang untuk menyimpan data kandidat, atribut recruitment, hasil assessment, dan keputusan hiring dalam struktur yang terorganisir.

Database ini akan digunakan sebagai sumber data utama untuk analisis recruitment, eksplorasi menggunakan SQL, pembuatan dashboard BI, dan mendukung pengambilan keputusan dalam proses recruitment.

## Desain Tabel

Database Recruitment Intelligence menggunakan satu tabel utama untuk menyimpan data kandidat dan informasi recruitment.

### Tabel Utama

**Nama tabel:** `recruitment_candidates`

Tabel ini menyimpan seluruh informasi yang tersedia pada dataset, mulai dari atribut kandidat, pengalaman, hasil assessment, strategi recruitment, hingga keputusan hiring.

### Alasan

Setiap baris pada dataset merepresentasikan satu kandidat. Seluruh kolom memiliki hubungan langsung dengan kandidat tersebut sehingga pada tahap awal database dapat menggunakan satu tabel utama.

Struktur database dapat dikembangkan menjadi beberapa tabel apabila pada tahap berikutnya terdapat kebutuhan untuk menyimpan data seperti lowongan, proses aplikasi, interview, assessment, atau riwayat recruitment secara terpisah.

## Pemetaan Tipe Data PostgreSQL

Tipe data PostgreSQL ditentukan berdasarkan karakteristik dan makna data, bukan hanya berdasarkan tipe data yang ditampilkan oleh Pandas.

| Kolom                 | Tipe PostgreSQL | Alasan                                             |
| --------------------- | --------------- | -------------------------------------------------- |
| candidate_id          | INTEGER         | ID unik untuk setiap kandidat                      |
| age                   | INTEGER         | Umur kandidat berupa bilangan bulat                |
| gender                | VARCHAR(20)     | Data berupa kategori teks                          |
| education_level       | VARCHAR(50)     | Data berupa kategori tingkat pendidikan            |
| experience_years      | INTEGER         | Lama pengalaman berupa bilangan bulat              |
| previous_companies    | INTEGER         | Jumlah perusahaan sebelumnya berupa bilangan bulat |
| distance_from_company | NUMERIC         | Data berupa nilai numerik; satuan belum diketahui  |
| interview_score       | INTEGER         | Nilai assessment berada pada rentang 0–100         |
| skill_score           | INTEGER         | Nilai assessment berada pada rentang 0–100         |
| personality_score     | INTEGER         | Nilai assessment berada pada rentang 0–100         |
| recruitment_strategy  | VARCHAR(20)     | Data berupa kategori teks                          |
| hiring_decision       | INTEGER         | Nilai keputusan berupa 0 atau 1                    |

## Database Design

### Nama Database

`recruitment_intelligence`

Database ini digunakan sebagai tempat penyimpanan data untuk Project Recruitment Intelligence.

### Tabel Utama

`recruitment_candidates`

Tabel ini menyimpan informasi kandidat, atribut recruitment, hasil assessment, dan keputusan hiring.

### Struktur Tabel

| Kolom                 | Tipe PostgreSQL | Keterangan                     |
| --------------------- | --------------- | ------------------------------ |
| candidate_id          | SERIAL          | Primary Key dan ID otomatis    |
| age                   | INTEGER         | Usia kandidat                  |
| gender                | VARCHAR(20)     | Jenis kelamin kandidat         |
| education_level       | VARCHAR(50)     | Tingkat pendidikan             |
| experience_years      | INTEGER         | Lama pengalaman kerja          |
| previous_companies    | INTEGER         | Jumlah perusahaan sebelumnya   |
| distance_from_company | NUMERIC         | Jarak kandidat dari perusahaan |
| interview_score       | INTEGER         | Nilai interview                |
| skill_score           | INTEGER         | Nilai kemampuan kandidat       |
| personality_score     | INTEGER         | Nilai penilaian kepribadian    |
| recruitment_strategy  | VARCHAR(20)     | Strategi recruitment           |
| hiring_decision       | INTEGER         | Keputusan hiring: 0 atau 1     |

### Primary Key

`candidate_id` digunakan sebagai Primary Key untuk mengidentifikasi setiap record kandidat secara unik.

ID dibuat secara otomatis oleh PostgreSQL menggunakan `SERIAL`.

### Constraints

Database memiliki aturan validasi sebagai berikut:

- `age` harus berada pada rentang 20–50.
- `experience_years` harus berada pada rentang 0–15.
- `previous_companies` harus berada pada rentang 1–5.
- `interview_score` harus berada pada rentang 0–100.
- `skill_score` harus berada pada rentang 0–100.
- `personality_score` harus berada pada rentang 0–100.
- `hiring_decision` hanya boleh bernilai 0 atau 1.

### Struktur Konseptual

Data kandidat dikelompokkan menjadi:

**Candidate Attributes**

- age
- gender
- education_level
- experience_years
- previous_companies

**Recruitment Attributes**

- distance_from_company
- recruitment_strategy

**Assessment**

- interview_score
- skill_score
- personality_score

**Outcome**

- hiring_decision

### Pengembangan Database

Pada tahap berikutnya, database dapat dikembangkan menjadi beberapa tabel seperti `vacancies`, `applications`, `interviews`, dan `assessments` apabila kebutuhan sistem recruitment menjadi lebih kompleks.

Untuk dataset Project 01 saat ini, satu tabel `recruitment_candidates` sudah cukup untuk merepresentasikan struktur data yang tersedia.
