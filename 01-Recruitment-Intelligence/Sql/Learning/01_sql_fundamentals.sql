
/*
====================================================
HR INTELLIGENCE 2026
PROJECT 01 - RECRUITMENT INTELLIGENCE

FILE    : 01_sql_fundamentals.sql
PURPOSE : SQL Learning Documentation
DATABASE: recruitment_intelligence
TABLE   : public.recruitment_candidates

====================================================
*/


-- ==================================================
-- 01. SELECT & FROM
-- Mengambil data dari tabel
-- ==================================================

SELECT *
FROM public.recruitment_candidates;

SELECT
    candidate_id,
    age,
    gender,
    education_level,
    interview_score,
    skill_score,
    personality_score,
    hiring_decision
FROM public.recruitment_candidates;


-- ==================================================
-- 02. WHERE
-- Memfilter data berdasarkan kondisi
-- ==================================================

SELECT *
FROM public.recruitment_candidates
WHERE hiring_decision = 1;

SELECT *
FROM public.recruitment_candidates
WHERE age >= 30;

SELECT *
FROM public.recruitment_candidates
WHERE gender = 'Male';


-- ==================================================
-- 03. ORDER BY
-- Mengurutkan data
-- ==================================================

SELECT *
FROM public.recruitment_candidates
ORDER BY interview_score DESC;

SELECT *
FROM public.recruitment_candidates
ORDER BY age ASC;


-- ==================================================
-- 04. LIMIT
-- Membatasi jumlah hasil
-- ==================================================

SELECT *
FROM public.recruitment_candidates
LIMIT 10;


-- ==================================================
-- 05. DISTINCT
-- Mengambil nilai unik
-- ==================================================

SELECT DISTINCT gender
FROM public.recruitment_candidates;

SELECT DISTINCT education_level
FROM public.recruitment_candidates;

SELECT DISTINCT recruitment_strategy
FROM public.recruitment_candidates;


-- ==================================================
-- 06. AGGREGATE FUNCTIONS
-- Menghitung dan merangkum data
-- ==================================================

SELECT
    COUNT(*) AS total_candidates,
    AVG(age) AS average_age,
    MIN(age) AS minimum_age,
    MAX(age) AS maximum_age,
    SUM(hiring_decision) AS total_hired
FROM public.recruitment_candidates;


-- ==================================================
-- 07. GROUP BY
-- Mengelompokkan data
-- ==================================================

SELECT
    gender,
    COUNT(*) AS total_candidates
FROM public.recruitment_candidates
GROUP BY gender;

SELECT
    hiring_decision,
    COUNT(*) AS total_candidates
FROM public.recruitment_candidates
GROUP BY hiring_decision;


-- ==================================================
-- 08. HAVING
-- Memfilter hasil pengelompokan
-- ==================================================

SELECT
    education_level,
    COUNT(*) AS total_candidates
FROM public.recruitment_candidates
GROUP BY education_level
HAVING COUNT(*) > 100;


-- ==================================================
-- 09. CASE WHEN
-- Membuat kategori berdasarkan kondisi
-- ==================================================

SELECT
    candidate_id,
    interview_score,
    CASE
        WHEN interview_score >= 80 THEN 'High'
        WHEN interview_score >= 60 THEN 'Medium'
        ELSE 'Low'
    END AS interview_category
FROM public.recruitment_candidates;


-- ==================================================
-- END OF SQL FUNDAMENTALS
-- ==================================================
