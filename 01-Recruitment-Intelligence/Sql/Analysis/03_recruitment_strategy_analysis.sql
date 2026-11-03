
/*
====================================================
HR INTELLIGENCE 2026
PROJECT 01 - RECRUITMENT INTELLIGENCE

FILE    : 03_recruitment_strategy_analysis.sql
PURPOSE : Recruitment Strategy Analysis
====================================================
*/

SELECT
    recruitment_strategy,

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
    ) AS hiring_rate_pct

FROM public.recruitment_candidates

GROUP BY recruitment_strategy

ORDER BY hiring_rate_pct DESC;
