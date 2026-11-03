# Data Dictionary — Recruitment Intelligence & Workflow Automation

## Dataset Overview

| Item                    | Value                                                              |
| :---------------------- | :----------------------------------------------------------------- |
| **File Path**           | `data/raw/recruitment_mydata.csv`                                  |
| **Total Records**       | 1,493 rows                                                         |
| **Total Columns**       | 11 columns                                                         |
| **Missing Cells**       | 0 cells                                                            |
| **Duplicate Rows**      | 0 rows                                                             |
| **Target Distribution** | Not Hired (`0`): 1,031 (69.06%) \| Hired (`1`): 462 (30.94%)       |
| **Naming Format**       | Source CSV: `PascalCase` \| Automation Pipeline: `snake_case`      |

---

## Variables

| Source Column (`PascalCase`) | Normalized Column (`snake_case`) | Data Type | Description                             | Expected Values / Range                                         | Role                  |
| :--------------------------- | :------------------------------- | :-------- | :-------------------------------------- | :-------------------------------------------------------------- | :-------------------- |
| `Age`                        | `age`                            | `float64` | Usia kandidat pelamar                   | 20 – 50 tahun                                                   | Candidate Attribute   |
| `Gender`                     | `gender`                         | `str`     | Jenis kelamin kandidat                  | `Female`, `Male`                                                | Candidate Attribute   |
| `EducationLevel`             | `education_level`                | `str`     | Tingkat pendidikan formal terakhir      | `Bachelor's (Type 1)`, `Bachelor's (Type 2)`, `Master's`, `PhD` | Candidate Attribute   |
| `ExperienceYears`            | `experience_years`               | `float64` | Lama pengalaman kerja profesional       | 0 – 15 tahun                                                    | Candidate Attribute   |
| `PreviousCompanies`          | `previous_companies`             | `int64`   | Jumlah perusahaan tempat pernah bekerja | 1 – 5 perusahaan                                                | Candidate Attribute   |
| `DistanceFromCompany`        | `distance_from_company`          | `float64` | Jarak tempat tinggal kandidat ke kantor | ~1.03 – 50.99 km                                                | Candidate Attribute   |
| `InterviewScore`             | `interview_score`                | `float64` | Nilai hasil interview kandidat          | 0 – 100                                                         | Assessment Score      |
| `SkillScore`                 | `skill_score`                    | `float64` | Nilai kemampuan teknis kandidat         | 0 – 100                                                         | Assessment Score      |
| `PersonalityScore`           | `personality_score`              | `float64` | Nilai penilaian kepribadian kandidat    | 0 – 100                                                         | Assessment Score      |
| `RecruitmentStrategy`        | `recruitment_strategy`           | `str`     | Strategi recruitment yang digunakan     | `Aggressive`, `Moderate`, `Conservative`                        | Recruitment Attribute |
| `HiringDecision`             | `hiring_decision`                | `int64`   | Keputusan akhir recruitment (Target)    | `0` = Not Hired, `1` = Hired                                    | Target / Outcome      |

> **Catatan `candidate_id`:** Kolom `candidate_id` tidak ada pada file CSV mentah (`recruitment_mydata.csv`), melainkan di-generate secara otomatis sebagai surrogate Primary Key bertipe `SERIAL` saat diimpor ke database PostgreSQL atau saat diproses di tahap transformasi data.

---

## Notes & Observations

- **Target Imbalance**: Sekitar 69.06% kandidat berstatus _Not Hired_ (1,031) dan 30.94% _Hired_ (462).
- **Data Quality pada CSV Produksi**: Dataset aktif memiliki 1.493 record bersih tanpa missing value maupun baris duplikat.
- **Normalisasi Kolom**: Script pipeline otomatis (`01_candidate_data_validation.py`) mengonversi nama kolom sumber berformat `PascalCase` menjadi `snake_case` agar konsisten dengan standar database dan pemrosesan data Python/SQL.
- **Tipe Data Numerik**: Kolom numerik diskrit seperti `age` dan `experience_years` tersimpan sebagai floating point (`float64`) pada CSV dan dikonversi ke tipe integer/numeric yang sesuai pada database/pipeline.

---

## Data Quality & Validation Rules (Project 02)

Workflow Automation menerapkan **Automated Data Quality Gate** dengan 6 kelompok pemeriksaan sebelum data diizinkan masuk ke proses downstream:

| Kelompok Validasi | Ruang Lingkup & Aturan | Severity | Status Jika Gagal |
| :--- | :--- | :--- | :--- |
| **Schema Validation** | Memastikan ke-11 kolom standar tersedia tanpa kolom tak dikenal | CRITICAL | FAIL |
| **Missing Value Validation** | Memeriksa ketiadaan sel bernilai null / NaN | WARNING | WARNING |
| **Duplicate Validation** | Memeriksa ketiadaan baris duplikat identik | WARNING | WARNING |
| **Data Type Validation** | Memastikan 8 kolom numerik dapat di-cast ke angka tanpa nilai invalid | CRITICAL | FAIL |
| **Range Validation** | Batasan nilai yang diizinkan:<br>• `age`: 20 – 50<br>• `experience_years`: 0 – 15<br>• `previous_companies`: 1 – 5<br>• `distance_from_company`: 0 – 100<br>• `interview_score`, `skill_score`, `personality_score`: 0 – 100<br>• `hiring_decision`: 0 – 1 | WARNING | WARNING |
| **Category Validation** | Nilai kategori yang diizinkan:<br>• `gender`: `Male`, `Female`<br>• `recruitment_strategy`: `Aggressive`, `Moderate`, `Conservative`<br>• `hiring_decision`: `0`, `1` | WARNING | WARNING |

### Logika Keputusan Data Quality Gate

```
Jika ada pemeriksaan berstatus "FAIL"    -> DECISION: REJECTED (Exit Code 1)
Jika ada pemeriksaan berstatus "WARNING" -> DECISION: ON HOLD  (Exit Code 2)
Jika seluruh pemeriksaan "PASS"         -> DECISION: APPROVED (Exit Code 0)
```

Laporan validasi dan catatan rinci setiap anomali diekspor secara otomatis ke direktori `data/processed/`:
- `data_quality_issue_log.csv` (Catatan detail isu per baris: `issue_id`, `row_index`, `column_name`, `issue_type`, `actual_value`, `severity`, `description`)
- `consolidated_validation_report.csv`
- `overall_validation_status.csv`
- Laporan per modul (`missing_values_report.csv`, `duplicate_records_report.csv`, `data_type_report.csv`, `range_validation_report.csv`, `category_validation_report.csv`)

---

## Database Design (PostgreSQL)

### Nama Database
`recruitment_intelligence`

### Tabel Utama: `recruitment_candidates`

| Kolom                 | Tipe PostgreSQL | Keterangan                                       |
| --------------------- | --------------- | ------------------------------------------------ |
| `candidate_id`        | `SERIAL`        | Primary Key dan auto-increment ID unik           |
| `age`                 | `INTEGER`       | Usia kandidat (20–50)                            |
| `gender`              | `VARCHAR(20)`   | Jenis kelamin kandidat                           |
| `education_level`     | `VARCHAR(50)`   | Tingkat pendidikan formal terakhir               |
| `experience_years`    | `INTEGER`       | Lama pengalaman kerja (0–15)                     |
| `previous_companies`  | `INTEGER`       | Jumlah perusahaan sebelumnya (1–5)               |
| `distance_from_company` | `NUMERIC`     | Jarak tempat tinggal ke kantor (km)              |
| `interview_score`     | `INTEGER`       | Nilai assessment wawancara (0–100)               |
| `skill_score`         | `INTEGER`       | Nilai assessment kemampuan teknis (0–100)        |
| `personality_score`   | `INTEGER`       | Nilai assessment kepribadian (0–100)             |
| `recruitment_strategy` | `VARCHAR(20)`  | Strategi recruitment                             |
| `hiring_decision`     | `INTEGER`       | Keputusan akhir: `0` (Not Hired) atau `1` (Hired)|

---

## SQL Analysis & Insights

Berdasarkan dataset aktual (1.493 kandidat):

| KPI                       | Value        |
| ------------------------- | -----------: |
| Total Candidates          | 1,493        |
| Hired Candidates          | 462          |
| Hiring Rate               | 30.94%       |
| Average Interview Score   | 50.63        |
| Average Skill Score       | 51.07        |
| Average Personality Score | 49.31        |
| Average Experience        | 7.69 tahun   |
