
/*
HR INTELLIGENCE 2026
PROJECT 01 - RECRUITMENT INTELLIGENCE
FILE: 04_assessment_score_distribution.sql
PURPOSE: Assessment Score Distribution
*/

SELECT
    CASE
        WHEN interview_score >= 80 THEN 'High'
        WHEN interview_score >= 60 THEN 'Medium'
        ELSE 'Low'
    END AS interview_band,

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

GROUP BY interview_band

ORDER BY
    CASE interview_band
        WHEN 'High' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'Low' THEN 3
    END;
