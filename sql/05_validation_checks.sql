-- =============================================================================
-- FILE: 05_validation_checks.sql
-- PROJECT: GM OnStar CSAT Improvement
-- PURPOSE: Data quality validation — run after master dataset is built
-- Run ALL checks before beginning analysis. Document any failures.
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- CHECK 1: Row count — compare to operations-reported volume
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    month_year,
    COUNT(*)                            AS ticket_count,
    SUM(survey_sent_flag)               AS surveys_sent,
    SUM(survey_completed_flag)          AS surveys_completed,
    ROUND(SUM(survey_sent_flag) * 100.0 / COUNT(*), 1)       AS pct_sent,
    ROUND(SUM(survey_completed_flag) * 100.0
          / NULLIF(SUM(survey_sent_flag), 0), 1)             AS response_rate_pct
FROM analytics.onstar_csat_master
GROUP BY month_year
ORDER BY month_year;
-- EXPECTED: Monthly ticket volume should match ops reporting +/- 2%

-- ─────────────────────────────────────────────────────────────────────────────
-- CHECK 2: Duplicate ticket IDs
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    COUNT(*)                            AS total_rows,
    COUNT(DISTINCT ticket_id)           AS unique_tickets,
    COUNT(*) - COUNT(DISTINCT ticket_id) AS duplicate_count
FROM analytics.onstar_csat_master;
-- EXPECTED: duplicate_count = 0

-- ─────────────────────────────────────────────────────────────────────────────
-- CHECK 3: CSAT score range validation
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    MIN(csat_score_normalized)          AS min_score,
    MAX(csat_score_normalized)          AS max_score,
    COUNT(CASE WHEN csat_score_normalized NOT BETWEEN 1 AND 5
               THEN 1 END)             AS out_of_range_count
FROM analytics.onstar_csat_master
WHERE survey_completed_flag = 1;
-- EXPECTED: min >= 1, max <= 5, out_of_range_count = 0

-- ─────────────────────────────────────────────────────────────────────────────
-- CHECK 4: Survey sent AFTER ticket close (logical sequence)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT COUNT(*) AS sequence_errors
FROM analytics.onstar_csat_master
WHERE survey_sent_at < ticket_closed_at;
-- EXPECTED: 0 — if not, flag for data investigation

-- ─────────────────────────────────────────────────────────────────────────────
-- CHECK 5: Agents with zero surveys sent (potential suppression flag)
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    agent_id,
    agent_name,
    COUNT(*)                            AS total_tickets,
    SUM(survey_sent_flag)               AS surveys_sent,
    ROUND(SUM(survey_sent_flag) * 100.0 / COUNT(*), 1) AS send_rate_pct
FROM analytics.onstar_csat_master
GROUP BY agent_id, agent_name
HAVING surveys_sent = 0 AND total_tickets >= 50   -- minimum volume threshold
ORDER BY total_tickets DESC;
-- EXPECTED: 0 agents with zero sends at >= 50 ticket volume
-- If agents appear here, flag for Track 4 (Agent Behavior Analysis)

-- ─────────────────────────────────────────────────────────────────────────────
-- CHECK 6: Closure code coverage
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    closure_reason_code,
    closure_reason_group,
    COUNT(*)                            AS ticket_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_total
FROM analytics.onstar_csat_master
GROUP BY closure_reason_code, closure_reason_group
ORDER BY ticket_count DESC;
-- EXPECTED: No closure_reason_group = 'Other' with > 5% of volume
-- If 'Other' is large, update column_mappings.yaml with additional code mappings

-- ─────────────────────────────────────────────────────────────────────────────
-- CHECK 7: Handle time outliers
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    COUNT(CASE WHEN handle_time_seconds < 30 THEN 1 END)    AS under_30s,
    COUNT(CASE WHEN handle_time_seconds > 7200 THEN 1 END)  AS over_2hours,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY handle_time_seconds) AS median_handle_time,
    AVG(handle_time_seconds)                                 AS avg_handle_time
FROM analytics.onstar_csat_master;
-- EXPECTED: under_30s should be 0 (excluded in dedup step)
-- Investigate over_2hours records — may be legitimate complex cases

-- ─────────────────────────────────────────────────────────────────────────────
-- CHECK 8: Verbatim coverage rate
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    COUNT(CASE WHEN survey_completed_flag = 1 THEN 1 END)               AS completed_surveys,
    COUNT(CASE WHEN verbatim_comment IS NOT NULL
               AND verbatim_comment != '' THEN 1 END)                   AS has_verbatim,
    ROUND(COUNT(CASE WHEN verbatim_comment IS NOT NULL
                     AND verbatim_comment != '' THEN 1 END) * 100.0
          / NULLIF(COUNT(CASE WHEN survey_completed_flag = 1
                              THEN 1 END), 0), 1)                       AS verbatim_rate_pct
FROM analytics.onstar_csat_master;
-- Informational only — understand verbatim volume for AI classification sizing

-- ─────────────────────────────────────────────────────────────────────────────
-- VALIDATION SUMMARY — run last, review with data engineer
-- ─────────────────────────────────────────────────────────────────────────────
SELECT 'Validation complete. Review each check output above.' AS status;
