# Power BI Dashboard Specification
## GM OnStar CSAT Improvement Project

---

## Overview

The dashboard delivers a single source of truth for CSAT performance, survey
funnel health, and agent-level patterns. It is designed for three audiences:

| Audience | Pages Used | Access Level |
|----------|-----------|--------------|
| Executive / Sponsor | Executive Summary | Read-only |
| Operations Manager | All pages | Read-only |
| BA Lead | All pages | Edit |

---

## Page 1: Executive Summary

**Purpose:** One-screen status view for leadership. No scrolling required.

### KPI Cards (top row)
| Card | Measure | Format |
|------|---------|--------|
| CSAT Score (MTD) | `AVG(csat_score)` | `#.## / 5.0` |
| WoW Change | vs. same period last week | `▲/▼ #.##` with conditional color |
| Survey Send Rate | `SUM(survey_sent) / COUNT(ticket_id)` | `##.#%` |
| Response Rate | `SUM(survey_completed) / SUM(survey_sent)` | `##.#%` |
| Tickets This Month | `COUNT(ticket_id)` | `#,###` |

### Charts
1. **CSAT Trend Line** — 6-month monthly average, line chart, date on X axis
2. **Survey Funnel Bar** — Stacked bar: Tickets → Sent → Completed (3 segments)
3. **CSAT by Issue Category** — Horizontal bar chart, sorted descending

### Filters (top of page)
- Date range slicer (defaults to last 30 days)
- Channel filter (all, phone, chat, app)

---

## Page 2: Survey Trigger Analysis

**Purpose:** Answer "Which closure codes suppress survey sends?"

### Charts
1. **Send Rate by Closure Code Group** — Horizontal bar chart
   - Color: Green if send rate > 60%, Yellow 30–60%, Red < 30%
   - Data labels: `send_rate%` and `ticket_count`

2. **Suppression Gap Table** — Matrix visual
   - Rows: Closure Code Group
   - Columns: Ticket Count | Send Rate | Surveys Missed (vs. best group)
   - Conditional formatting on Send Rate column

3. **Send Rate Trend by Closure Group** — Small multiples line chart, one per closure group, 6-month trend

4. **Closure Code Distribution Donut** — Shows share of total tickets per closure group

### DAX Measures
```dax
Survey Send Rate =
    DIVIDE(
        SUM(onstar_csat_master[survey_sent_flag]),
        COUNTROWS(onstar_csat_master)
    )

Potential Surveys Missed =
    VAR MaxSendRate =
        MAXX(
            ALLSELECTED(onstar_csat_master[closure_reason_group]),
            [Survey Send Rate]
        )
    RETURN
        SUMX(
            SUMMARIZE(
                onstar_csat_master,
                onstar_csat_master[closure_reason_group]
            ),
            (MaxSendRate - [Survey Send Rate]) * COUNTROWS(RELATEDTABLE(onstar_csat_master))
        )
```

---

## Page 3: Response Rate Drivers

**Purpose:** What makes a customer respond to the survey?

### Charts
1. **Response Rate by Handle Time Bucket** — Column chart
   - X: 0-3min, 3-7min, 7-15min, 15+min
   - Y: Response rate %

2. **Response Rate by Days to Survey** — Column chart
   - X: Same Day, Next Day, 2-3 Days, 4+ Days
   - Y: Response rate %

3. **Response Rate by Transfer Count** — Column chart
   - X: 0 transfers, 1 transfer, 2+ transfers
   - Y: Response rate %

4. **Response Rate Scatter Plot** — Queue wait time (X) vs. Response rate (Y), one bubble per agent, size = ticket volume

---

## Page 4: Agent Performance

**Purpose:** Identify coaching opportunities and top performers.

### Charts
1. **Agent CSAT Distribution** — Box plot or violin chart per team
2. **Agent Survey Send Rate vs. Team Average** — Scatter, flagged agents highlighted in red
3. **Agent Performance Matrix** — Table with sparklines:
   - Agent Name | Tickets | Send Rate | Response Rate | Avg CSAT | QA Score | Flag

### Row-Level Security
- Team leads see only their team's agents
- Operations manager sees all agents
- Individual agents cannot access this page

---

## Page 5: Verbatim Intelligence (AI-Powered)

**Purpose:** Understand WHAT customers are saying, not just scores.

### Charts
1. **Theme Distribution Bar** — Count of verbatims per AI-classified theme
2. **Sentiment Breakdown Donut** — Positive / Neutral / Negative
3. **Theme vs. CSAT Score Heatmap** — Theme on Y, CSAT bucket on X, cell = count
4. **Priority Flag Count Card** — Count of `ai_priority_flag = TRUE` with drill-through to verbatim table
5. **Verbatim Table** (drill-through page) — Shows raw comments, score, theme, sentiment, agent, date

---

## Refresh Schedule
- **Full refresh:** Every Monday at 7:00 AM CT (aligned with pipeline run)
- **Incremental:** Daily at 6:00 AM CT for prior day's data

## Data Source
Power BI connects to Snowflake via DirectQuery on `analytics.onstar_csat_master`.
Verbatim themes table is imported (refreshed weekly).
