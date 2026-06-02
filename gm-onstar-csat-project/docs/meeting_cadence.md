# Meeting Cadence & Governance
## GM OnStar CSAT Improvement Project

---

## Recurring Meetings

### 1. Team Weekly Standup
- **Frequency:** Weekly, every Monday
- **Duration:** 30 minutes
- **Attendees:** BA Lead, Data Engineer, Ops Lead, QA Analyst
- **Format:** Status → Blockers → Decisions needed
- **Standing Agenda:**
  1. What each person completed last week (2 min each)
  2. Blockers or dependencies (5 min)
  3. Decisions or approvals needed from the group (5 min)
  4. This week's priorities (5 min)
- **Tool:** MS Teams, rotating notes in Confluence/SharePoint
- **BA Action:** Send brief recap email within 2 hours of meeting

---

### 2. Data & Analysis Working Session
- **Frequency:** Bi-weekly (alternating Wednesdays)
- **Duration:** 60 minutes
- **Attendees:** BA Lead + Data Engineer
- **Purpose:** Deep-dive on data pipeline, analysis logic, QA of outputs
- **Standing Agenda:**
  1. Review data quality report from last pipeline run (10 min)
  2. Work through current analysis track together (30 min)
  3. Review any anomalies or unexpected patterns (15 min)
  4. Agree on next two weeks' data deliverables (5 min)

---

### 3. Operations SME Sync
- **Frequency:** Bi-weekly (alternating Thursdays)
- **Duration:** 45 minutes
- **Attendees:** BA Lead, Call Center Ops Lead, QA/WFM Analyst
- **Purpose:** Validate findings against operational context; sanity-check data patterns
- **Standing Agenda:**
  1. BA shares 2–3 data patterns or anomalies (15 min)
  2. Ops validates or challenges with operational context (20 min)
  3. Open questions and action items (10 min)
- **Key Rule:** BA presents data; Ops interprets operations. Do not draw conclusions without Ops validation.

---

### 4. Executive Sponsor Monthly Update
- **Frequency:** Monthly, first Tuesday of each month
- **Duration:** 30 minutes
- **Attendees:** BA Lead + Project Sponsor (VP Customer Experience)
- **Format:** No live demos — pre-read deck sent 24 hours in advance
- **Standing Agenda:**
  1. Phase status and RAG (Red/Amber/Green) indicator (5 min)
  2. One key finding or insight from the month (10 min)
  3. Risks or decisions requiring sponsor action (10 min)
  4. Next month preview (5 min)
- **BA Action:** Send 3-slide pre-read the day before. Never surprise the sponsor.

---

### 5. Stakeholder Steering Committee
- **Frequency:** Monthly (last Thursday of each month)
- **Duration:** 60 minutes
- **Attendees:** All stakeholders (see PROJECT_CHARTER.md RACI)
- **Purpose:** Broader alignment, milestone review, risk escalation
- **Standing Agenda:**
  1. Phase milestone status (10 min)
  2. Key findings or analytical progress (20 min)
  3. Risks and issues (15 min)
  4. Decisions required from the group (15 min)

---

## One-Time Milestone Meetings

| Meeting | When | Duration | Attendees | Purpose |
|---------|------|----------|-----------|---------|
| **Project Kickoff** | Month 1, Week 1 | 90 min | All stakeholders | Scope, timeline, roles, data access |
| **Data Discovery Session** | Month 1, Week 2 | 60 min | BA + IT + CRM Admin | Map data sources, access path |
| **Mid-Point Preview** | Month 3, Week 2 | 60 min | Core team + Sponsor | Early pattern preview before full analysis |
| **Findings Readout** | Month 5, Week 2 | 90 min | All stakeholders | Full analysis, draft recommendations |
| **Recommendations Workshop** | Month 5, Week 3 | 2 hours | Ops + QA + BA | Prioritize and refine recommendations |
| **Executive Final Presentation** | Month 6, Week 1 | 45 min | Leadership | Final deck, decision on implementation |
| **Handoff & Closeout** | Month 6, Week 2 | 60 min | Core team | Documentation handoff, lessons learned |

---

## Communication Norms

| Channel | Purpose | Frequency |
|---------|---------|-----------|
| **Email** | Monthly executive update, milestone summaries | Monthly |
| **Teams Chat** | Day-to-day questions, quick decisions | As needed |
| **Confluence/SharePoint** | Meeting notes, deliverables, data dictionary | Ongoing |
| **Power BI Dashboard** | Self-serve metrics for sponsor and VPs | Live from Month 3 |
| **GitHub Actions** | Automated pipeline success/failure alerts | Automated (Monday AM) |

---

## Meeting Rules of Engagement

1. **BA Lead sends agenda 24 hours in advance** for all recurring meetings
2. **No PowerPoint for standups** — use a shared running notes doc
3. **Decisions are documented** in the meeting notes with owner and due date
4. **Data anomalies go to Ops SME before going to leadership** — never surface unvalidated surprises upward
5. **The sponsor is never surprised** — if a significant risk or finding emerges between scheduled meetings, send a brief Teams message within the same business day
