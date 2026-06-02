-- =============================================================================
-- FILE: 04_master_join.sql
-- PROJECT: GM OnStar CSAT Improvement
-- PURPOSE: Build the master analytical dataset by joining all source tables
-- AUTHOR: Chitra (Queen) Dubey
-- VERSION: 1.0
--
-- USAGE: Run in Snowflake (or adapt for Redshift / Azure Synapse)
-- DEPENDENCIES: Requires 01_ticket_extract.sql, 02_survey_extract.sql,
--               03_telephony_extract.sql to have been run first
-- =============================================================================

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 1: Set analysis window parameters
-- ─────────────────────────────────────────────────────────────────────────────
SET analysis_start = DATEADD('month', -6, CURRENT_DATE());
SET analysis_end   = CURRENT_DATE();

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 2: Deduplicate tickets (keep most recent close per ticket_id)
-- ─────────────────────────────────────────────────────────────────────────────
WITH deduped_tickets AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY ticket_id
               ORDER BY ticket_closed_at DESC
           ) AS row_num
    FROM staging.crm_tickets
    WHERE ticket_closed_at BETWEEN $analysis_start AND $analysis_end
      AND handle_time_seconds >= 30          -- exclude sub-30-second test calls
      AND account_type != 'TEST'             -- exclude test accounts
),

clean_tickets AS (
    SELECT * FROM deduped_tickets WHERE row_num = 1
),

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 3: Prepare survey data — treat non-joins as "no survey sent"
-- ─────────────────────────────────────────────────────────────────────────────
survey_prep AS (
    SELECT
        ticket_id                                          AS survey_ticket_id,
        sent_at                                            AS survey_sent_at,
        opened_at                                          AS survey_opened_at,
        completed_at                                       AS survey_completed_at,
        raw_score                                          AS csat_score_raw,
        -- Normalize to 1–5 scale (adjust denominator if platform uses 1–10)
        ROUND((raw_score / 10.0) * 5, 2)                  AS csat_score_normalized,
        verbatim_text                                      AS verbatim_comment,
        trigger_method                                     AS survey_trigger_method,
        1                                                  AS survey_sent_flag,
        CASE WHEN completed_at IS NOT NULL THEN 1 ELSE 0 END AS survey_completed_flag,
        CASE WHEN opened_at IS NOT NULL THEN 1 ELSE 0 END    AS survey_opened_flag
    FROM staging.survey_data
),

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 4: Closure code grouping
-- (Map raw closure codes to logical groups — maintain in config/column_mappings.yaml)
-- ─────────────────────────────────────────────────────────────────────────────
closure_groups AS (
    SELECT
        closure_reason_code,
        CASE
            WHEN closure_reason_code IN ('RES_CONF', 'RES_CUST_VERIFIED', 'SOLVED_FIRST')
                THEN 'Resolved - Customer Confirmed'
            WHEN closure_reason_code IN ('RES_NO_FU', 'SOLVED_SILENT', 'CLOSED_AUTO')
                THEN 'Resolved - No Follow-Up'
            WHEN closure_reason_code IN ('ESCALATED_T2', 'ESCALATED_SUP')
                THEN 'Escalated'
            WHEN closure_reason_code IN ('TRANSFERRED_DEPT', 'TRANSFERRED_EXT')
                THEN 'Transferred'
            WHEN closure_reason_code IN ('ABANDON', 'CUST_HANGUP')
                THEN 'Customer Abandoned'
            WHEN closure_reason_code IN ('DUPLICATE', 'TEST_CALL')
                THEN 'Administrative'
            ELSE 'Other'
        END AS closure_reason_group
    FROM (SELECT DISTINCT closure_reason_code FROM staging.crm_tickets)
),

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 5: Master join
-- ─────────────────────────────────────────────────────────────────────────────
master_join AS (
    SELECT
        -- ── Ticket Core ──────────────────────────────────────────────────────
        t.ticket_id,
        t.agent_id,
        a.agent_name,
        a.team_id,
        a.supervisor_id,
        t.ticket_opened_at,
        t.ticket_closed_at,

        -- ── Handle Time ──────────────────────────────────────────────────────
        t.handle_time_seconds,
        p.hold_time_seconds,
        CASE
            WHEN t.handle_time_seconds < 180  THEN '0-3min'
            WHEN t.handle_time_seconds < 420  THEN '3-7min'
            WHEN t.handle_time_seconds < 900  THEN '7-15min'
            ELSE '15+min'
        END AS handle_time_bucket,

        -- ── Transfer / Escalation ────────────────────────────────────────────
        COALESCE(p.transfer_count, 0)                       AS transfer_count,
        CASE WHEN COALESCE(p.transfer_count, 0) > 0
             THEN TRUE ELSE FALSE END                       AS is_transfer,
        COALESCE(t.escalation_flag, FALSE)                  AS is_escalation,

        -- ── Closure Codes ────────────────────────────────────────────────────
        t.closure_reason_code,
        cg.closure_reason_group,

        -- ── Issue Classification ─────────────────────────────────────────────
        t.channel,
        t.issue_category,
        t.issue_subcategory,
        t.resolution_status,
        CASE WHEN COALESCE(p.transfer_count, 0) = 0
              AND t.resolution_status = 'resolved'
             THEN TRUE ELSE FALSE END                       AS is_first_contact_resolution,

        -- ── Time Dimensions ──────────────────────────────────────────────────
        DAYNAME(t.ticket_closed_at)                         AS day_of_week,
        HOUR(t.ticket_closed_at)                            AS hour_of_day,
        TO_CHAR(t.ticket_closed_at, 'YYYY-MM')             AS month_year,

        -- ── Survey Fields ────────────────────────────────────────────────────
        COALESCE(s.survey_sent_flag, 0)                     AS survey_sent_flag,
        s.survey_sent_at,
        COALESCE(s.survey_opened_flag, 0)                   AS survey_opened_flag,
        COALESCE(s.survey_completed_flag, 0)                AS survey_completed_flag,
        s.survey_completed_at,
        s.csat_score_raw,
        s.csat_score_normalized,
        s.verbatim_comment,
        s.survey_trigger_method,

        -- ── Days to Survey ───────────────────────────────────────────────────
        DATEDIFF('day', t.ticket_closed_at, s.survey_sent_at) AS days_to_survey,
        CASE
            WHEN s.survey_sent_at IS NULL THEN NULL
            WHEN DATEDIFF('day', t.ticket_closed_at, s.survey_sent_at) = 0 THEN 'Same Day'
            WHEN DATEDIFF('day', t.ticket_closed_at, s.survey_sent_at) = 1 THEN 'Next Day'
            WHEN DATEDIFF('day', t.ticket_closed_at, s.survey_sent_at) <= 3 THEN '2-3 Days'
            ELSE '4+ Days'
        END AS days_to_survey_bucket,

        -- ── Telephony ────────────────────────────────────────────────────────
        p.ivr_path,
        COALESCE(p.queue_wait_seconds, 0)                   AS queue_wait_seconds,

        -- ── QA ───────────────────────────────────────────────────────────────
        q.qa_score,
        CASE WHEN q.qa_score IS NOT NULL THEN 1 ELSE 0 END  AS qa_evaluated_flag,
        q.qa_category_greeting,
        q.qa_category_resolution,
        q.qa_category_empathy,
        q.qa_category_closure

    FROM clean_tickets t
    LEFT JOIN survey_prep s
        ON t.ticket_id = s.survey_ticket_id
    LEFT JOIN staging.telephony_calls p
        ON t.ticket_id = p.ticket_id
    LEFT JOIN staging.agent_reference a
        ON t.agent_id = a.agent_id
    LEFT JOIN staging.qa_scorecards q
        ON t.ticket_id = q.ticket_id
    LEFT JOIN closure_groups cg
        ON t.closure_reason_code = cg.closure_reason_code
)

-- ─────────────────────────────────────────────────────────────────────────────
-- STEP 6: Write to analytical layer
-- ─────────────────────────────────────────────────────────────────────────────
SELECT * FROM master_join;

-- To persist:
-- CREATE OR REPLACE TABLE analytics.onstar_csat_master AS
-- SELECT * FROM master_join;
