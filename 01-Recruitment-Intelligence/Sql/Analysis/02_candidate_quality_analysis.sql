
/*
====================================================
HR INTELLIGENCE 2026
PROJECT 01 - RECRUITMENT INTELLIGENCE

FILE    : 02_candidate_quality_analysis.sql
PURPOSE : Candidate Quality Analysis
====================================================
*/

SELECT
    CASE
        WHEN hiring_decision = 1 THEN 'Hired'
        WHEN hiring_decision = 0 THEN 'Rejected'
    END AS hiring_outcome,

    COUNT(*) AS total_candidates,

    ROUND(AVG(interview_score), 2)
        AS avg_interview_score,

    ROUND(AVG(skill_score), 2)
        AS avg_skill_score,

    ROUND(AVG(personality_score), 2)
        AS avg_personality_score

FROM public.recruitment_candidates

GROUP BY hiring_decision

ORDER BY hiring_decision DESC;
