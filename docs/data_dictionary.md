# Data Dictionary
## GM OnStar CSAT Improvement Project

**Version:** 1.0  
**Last Updated:** June 2026  
**Owner:** Chitra (Queen) Dubey, BA Lead

---

## Overview

This document defines every field in the master analytical dataset. Each field includes its source system, transformation logic, data type, and analytical purpose.

The master dataset is built by joining four source tables:
1. **CRM Tickets** (Salesforce or proprietary CRM)
2. **Survey Data** (Medallia or Qualtrics)
3. **Telephony / ACD Data** (Avaya, Genesys, or Cisco)
4. **Agent Reference Data** (Workforce Management system)

---

## Master Dataset: `onstar_csat_master`

### Primary Key
`ticket_id` — Unique identifier per customer interaction. Used as the join key across all source systems. Verify consistency between CRM and survey platform before joining.

---

### Section 1: Ticket / CRM Fields

| Field Name | Source | Data Type | Description | Notes |
|-----------|--------|-----------|-------------|-------|
| `ticket_id` | CRM | VARCHAR | Unique case/ticket identifier | Primary key |
| `agent_id` | CRM | VARCHAR | Unique identifier for the closing agent | Use closing agent, not opening agent, unless transferred |
| `agent_name` | Agent Reference | VARCHAR | Agent display name | Join from WFM reference table |
| `team_id` | Agent Reference | VARCHAR | Agent's team/pod assignment | For team-level aggregation |
| `supervisor_id` | Agent Reference | VARCHAR | Agent's direct supervisor | For escalation and coaching routing |
| `ticket_opened_at` | CRM | TIMESTAMP | Date and time ticket was created | UTC; convert to local call center timezone |
| `ticket_closed_at` | CRM | TIMESTAMP | Date and time ticket was closed | UTC |
| `handle_time_seconds` | CRM | INTEGER | Total handle time in seconds | Includes hold time in some systems — verify with CRM admin |
| `hold_time_seconds` | Telephony | INTEGER | Total hold time in seconds | May need to pull from ACD separately |
| `transfer_count` | Telephony | INTEGER | Number of times call was transferred | 0 = no transfer |
| `closure_reason_code` | CRM | VARCHAR | Agent-selected closure reason | **Key variable** — maps to survey trigger |
| `closure_reason_group` | Derived | VARCHAR | Logical grouping of closure codes | See `config/column_mappings.yaml` for mapping |
| `channel` | CRM | VARCHAR | Contact channel | Values: `phone`, `chat`, `app`, `email` |
| `issue_category` | CRM | VARCHAR | Primary issue type | e.g., Navigation, Connectivity, Emergency, Billing |
| `issue_subcategory` | CRM | VARCHAR | Secondary issue type | May be null for some categories |
| `resolution_status` | CRM | VARCHAR | Outcome of the interaction | Values: `resolved`, `escalated`, `transferred`, `abandoned`, `unresolved` |
| `is_first_contact_resolution` | Derived | BOOLEAN | True if resolved on first contact, no transfer | `transfer_count = 0 AND resolution_status = 'resolved'` |
| `is_transfer` | Derived | BOOLEAN | True if any transfer occurred | `transfer_count > 0` |
| `is_escalation` | CRM | BOOLEAN | True if escalated to supervisor or tier 2 | Check escalation flag in CRM |
| `reopened_flag` | CRM | BOOLEAN | True if ticket was reopened after initial close | Dedup logic: keep most recent close event |
| `day_of_week` | Derived | VARCHAR | Day of week ticket was closed | Derived from `ticket_closed_at` |
| `hour_of_day` | Derived | INTEGER | Hour of day ticket was closed (0–23) | Derived from `ticket_closed_at`, local time |
| `month_year` | Derived | VARCHAR | Month and year (e.g., 2025-01) | For trend analysis |

---

### Section 2: Survey Fields

| Field Name | Source | Data Type | Description | Notes |
|-----------|--------|-----------|-------------|-------|
| `survey_ticket_id` | Survey Platform | VARCHAR | Ticket ID as recorded in survey system | Join key to `ticket_id` — verify match rate |
| `survey_sent_flag` | Derived | INTEGER | 1 if survey was sent, 0 if not | NULL in survey table = 0 after LEFT JOIN |
| `survey_sent_at` | Survey Platform | TIMESTAMP | Timestamp survey was sent to customer | UTC |
| `survey_opened_flag` | Survey Platform | INTEGER | 1 if customer opened the survey | May not be available in all platforms |
| `survey_completed_flag` | Derived | INTEGER | 1 if customer completed the survey | NULL after join = 0 |
| `survey_completed_at` | Survey Platform | TIMESTAMP | Timestamp survey was completed | UTC |
| `csat_score` | Survey Platform | FLOAT | Customer satisfaction score | Typically 1–5 or 1–10; normalize to 1–5 if needed |
| `csat_score_normalized` | Derived | FLOAT | Score normalized to 1–5 scale | `(raw_score / max_scale) * 5` |
| `verbatim_comment` | Survey Platform | TEXT | Customer's open-text response | Nullable; used for AI theme classification |
| `survey_trigger_method` | Survey Platform | VARCHAR | What triggered the survey send | e.g., `closure_code`, `random_sample`, `manual` |
| `days_to_survey` | Derived | FLOAT | Days between ticket close and survey send | `(survey_sent_at - ticket_closed_at)` in days |

---

### Section 3: Telephony / ACD Fields

| Field Name | Source | Data Type | Description | Notes |
|-----------|--------|-----------|-------------|-------|
| `call_id` | ACD | VARCHAR | Unique call leg identifier | May differ from ticket ID |
| `ivr_path` | ACD | VARCHAR | IVR menu path taken before agent | For channel experience analysis |
| `queue_wait_seconds` | ACD | INTEGER | Time in queue before agent pickup | High wait may correlate with lower CSAT |
| `call_recording_flag` | ACD | BOOLEAN | Whether call was recorded | For QA cross-reference |
| `abandon_flag` | ACD | BOOLEAN | Whether customer abandoned before agent | Abandoned calls typically don't get tickets |

---

### Section 4: QA Fields

| Field Name | Source | Data Type | Description | Notes |
|-----------|--------|-----------|-------------|-------|
| `qa_score` | QA Scorecard | FLOAT | QA evaluation score for this interaction | 0–100 scale typical |
| `qa_evaluated_flag` | Derived | INTEGER | 1 if this interaction was QA evaluated | Not all interactions are QA'd |
| `qa_category_greeting` | QA Scorecard | FLOAT | Sub-score: greeting and opening | |
| `qa_category_resolution` | QA Scorecard | FLOAT | Sub-score: resolution quality | |
| `qa_category_empathy` | QA Scorecard | FLOAT | Sub-score: empathy and tone | |
| `qa_category_closure` | QA Scorecard | FLOAT | Sub-score: call closure technique | **Watch this field** — low closure scores may correlate with survey suppression behavior |

---

### Section 5: Derived / Calculated Fields

| Field Name | Formula / Logic | Purpose |
|-----------|----------------|---------|
| `handle_time_bucket` | `CASE WHEN handle_time_seconds < 180 THEN '0-3min' WHEN handle_time_seconds < 420 THEN '3-7min' WHEN handle_time_seconds < 900 THEN '7-15min' ELSE '15+min' END` | Binned handle time for pattern analysis |
| `survey_response_rate` | `SUM(survey_completed_flag) / NULLIF(SUM(survey_sent_flag), 0)` | Calculated at agent or closure_code group level |
| `survey_suppression_rate` | `1 - (SUM(survey_sent_flag) / COUNT(ticket_id))` | Rate at which tickets did NOT generate a survey |
| `days_to_survey_bucket` | `CASE WHEN days_to_survey = 0 THEN 'Same Day' WHEN days_to_survey <= 1 THEN 'Next Day' WHEN days_to_survey <= 3 THEN '2-3 Days' ELSE '4+ Days' END` | For timing analysis |
| `ai_verbatim_theme` | AI classifier output | Assigned theme: `resolution_quality`, `wait_time`, `agent_attitude`, `technical_issue`, `billing`, `other` |
| `ai_verbatim_sentiment` | AI classifier output | `positive`, `neutral`, `negative` |
| `ai_coaching_flag` | AI recommendation | `TRUE` if agent-level pattern warrants coaching review |

---

## Data Quality Rules

| Rule | Check Query | Action if Fails |
|------|-------------|-----------------|
| No duplicate ticket IDs | `COUNT(*) != COUNT(DISTINCT ticket_id)` | Apply dedup logic — keep most recent close |
| CSAT score in valid range | `csat_score NOT BETWEEN 1 AND 5` | Flag for vendor review |
| Ticket close date within analysis window | `ticket_closed_at < analysis_start OR > analysis_end` | Exclude from analysis |
| Agent ID present on all tickets | `agent_id IS NULL` | Flag; exclude from agent-level analysis only |
| Handle time non-negative | `handle_time_seconds < 0` | Investigate; likely data entry error |
| Survey sent date after ticket close date | `survey_sent_at < ticket_closed_at` | Flag as data anomaly |

---

## Analysis Window

- **Start Date:** 6 months prior to project data extraction date
- **End Date:** Date of data extraction
- **Timezone:** All timestamps normalized to call center local time (verify with IT)
- **Exclusions:** Test accounts, internal QA test calls, calls lasting < 30 seconds

---

## Change Log

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | June 2026 | Initial version | Chitra Dubey |
