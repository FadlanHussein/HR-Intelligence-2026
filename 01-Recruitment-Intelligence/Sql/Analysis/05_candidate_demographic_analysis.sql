
/*
HR INTELLIGENCE 2026
PROJECT 01 - RECRUITMENT INTELLIGENCE
FILE: 05_candidate_demographic_analysis.sql
PURPOSE: Candidate Demographic Analysis
*/

-- Gender Analysis
SELECT
    gender,
    COUNT(*) AS total_candidates,

    COUNT(*) FILTER (
        WHERE hiring_decision = 1
    ) AS hired_candidates,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE hiring_decision = 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS hiring_rate_pct

FROM public.recruitment_candidates
GROUP BY gender
ORDER BY total_candidates DESC;


-- Age Group Analysis
SELECT
    CASE
        WHEN age < 25 THEN 'Under 25'
        WHEN age < 35 THEN '25-34'
        WHEN age < 45 THEN '35-44'
        ELSE '45 and Above'
    END AS age_group,

    COUNT(*) AS total_candidates,

    COUNT(*) FILTER (
        WHERE hiring_decision = 1
    ) AS hired_candidates,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE hiring_decision = 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS hiring_rate_pct

FROM public.recruitment_candidates
GROUP BY age_group
ORDER BY
    MIN(age);
