
/*
HR INTELLIGENCE 2026
PROJECT 01 - RECRUITMENT INTELLIGENCE
FILE: 06_experience_hiring_analysis.sql
PURPOSE: Experience & Hiring Analysis
*/

SELECT
    CASE
        WHEN experience_years < 2 THEN 'Entry Level'
        WHEN experience_years < 5 THEN 'Junior'
        WHEN experience_years < 10 THEN 'Mid Level'
        ELSE 'Senior'
    END AS experience_category,

    COUNT(*) AS total_candidates,

    COUNT(*) FILTER (
        WHERE hiring_decision = 1
    ) AS hired_candidates,

    ROUND(
        AVG(interview_score), 2
    ) AS avg_interview_score,

    ROUND(
        AVG(skill_score), 2
    ) AS avg_skill_score,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE hiring_decision = 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS hiring_rate_pct

FROM public.recruitment_candidates
GROUP BY experience_category
ORDER BY MIN(experience_years);
