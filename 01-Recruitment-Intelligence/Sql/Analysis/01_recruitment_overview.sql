
/*
====================================================
HR INTELLIGENCE 2026
PROJECT 01 - RECRUITMENT INTELLIGENCE

FILE    : 01_recruitment_overview.sql
PURPOSE : Recruitment Overview Analysis
DATABASE: recruitment_intelligence

====================================================
*/

-- 01. Recruitment Overview

SELECT
    COUNT(*) AS total_candidates,

    COUNT(*) FILTER (
        WHERE hiring_decision = 1
    ) AS hired_candidates,

    COUNT(*) FILTER (
        WHERE hiring_decision = 0
    ) AS rejected_candidates,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE hiring_decision = 1
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS hiring_rate_pct,

    ROUND(AVG(interview_score), 2)
        AS avg_interview_score,

    ROUND(AVG(skill_score), 2)
        AS avg_skill_score,

    ROUND(AVG(personality_score), 2)
        AS avg_personality_score

FROM public.recruitment_candidates;
