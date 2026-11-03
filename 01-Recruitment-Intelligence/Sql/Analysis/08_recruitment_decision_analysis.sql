
/*
HR INTELLIGENCE 2026
PROJECT 01 - RECRUITMENT INTELLIGENCE
FILE: 08_recruitment_decision_analysis.sql
PURPOSE: Recruitment Decision Analysis
*/

SELECT
    CASE
        WHEN hiring_decision = 1 THEN 'Hired'
        ELSE 'Rejected'
    END AS hiring_outcome,

    COUNT(*) AS total_candidates,

    ROUND(
        AVG(interview_score), 2
    ) AS avg_interview_score,

    ROUND(
        AVG(skill_score), 2
    ) AS avg_skill_score,

    ROUND(
        AVG(personality_score), 2
    ) AS avg_personality_score,

    ROUND(
        AVG(
            (
                interview_score +
                skill_score +
                personality_score
            ) / 3.0
        ), 2
    ) AS avg_composite_score

FROM public.recruitment_candidates

GROUP BY hiring_decision

ORDER BY hiring_decision DESC;
