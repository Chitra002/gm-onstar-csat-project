# Recommendations & Implementation Roadmap
## GM OnStar CSAT Improvement Initiative

**Version:** DRAFT — Month 5, Week 3  
**Prepared by:** Chitra (Queen) Dubey, BA Lead  
**Status:** Post-Workshop Draft — Pending Sponsor Approval

---

## Recommendation Prioritization Framework

Each recommendation is scored on:
- **Impact:** Expected improvement to CSAT score or response rate
- **Effort:** Implementation complexity and resource requirement
- **Speed:** How quickly results would be visible
- **Priority:** Combined assessment — P1 (do now), P2 (do next), P3 (plan)

---

## Recommendations

### REC-01: Audit and Update Survey Trigger Rules *(P1)*
**Category:** Process  
**Owner:** Call Center Operations + Survey Platform Admin  
**Timeline:** 30 days

**What:** Work with the survey platform vendor to map every active closure code to its survey trigger behavior. Update trigger rules so that all "Resolved" category codes — regardless of follow-up sub-type — trigger a survey send.

**Why:** The data shows a [X]% gap in send rates between closure code groups. This is the single highest-leverage change available. Fixing the trigger rules does not require any agent behavior change.

**Success Metric:** Overall survey send rate increases to ≥ 70% within 60 days of implementation.

**Risk:** If the survey volume increase creates vendor cost implications, escalate to sponsor for budget approval before implementation.

---

### REC-02: Standardize Closure Code Usage with Decision Tree *(P1)*
**Category:** Process / Training  
**Owner:** Call Center Operations + QA  
**Timeline:** 45 days

**What:** Develop a one-page closure code decision tree — a simple flowchart agents follow to select the correct closure code. Integrate into the agent desktop as a quick-reference guide. Include in new hire onboarding.

**Why:** Agent-level analysis shows that many agents using low-trigger codes have lower QA closure sub-scores, suggesting the issue is inconsistent training rather than deliberate behavior. A decision tree removes ambiguity.

**Success Metric:** Variance in closure code selection across agents with similar call types decreases by 30% within 90 days.

---

### REC-03: Tighten Survey Send Window to Same-Day *(P1)*
**Category:** Timing / Vendor  
**Owner:** Survey Platform Admin  
**Timeline:** 2 weeks (vendor configuration change)

**What:** Configure the survey platform to send surveys within 2–4 hours of ticket close rather than the current [X]-hour average delay. For phone calls, send via SMS; for app interactions, send as push notification.

**Why:** Response rate analysis shows same-day sends achieve [X]% vs. [Y]% for 4+ day delays. This is a configuration change that does not require operational buy-in.

**Success Metric:** Average days-to-survey decreases to < 0.5 days. Response rate increases by ≥ 5 percentage points within 30 days.

---

### REC-04: Add Survey Send Rate to Agent Performance Scorecard *(P2)*
**Category:** Performance Management  
**Owner:** Call Center Operations + HR  
**Timeline:** 60 days (requires HR alignment)

**What:** Add "Survey Send Rate" as a measured metric on each agent's monthly performance scorecard, alongside CSAT score. An agent who achieves a great CSAT score but has a low send rate should not receive full credit — the score is not representative.

**Why:** Currently, agents are only measured on CSAT score — which creates an implicit incentive to close tickets in ways that avoid surveys from dissatisfied customers. Measuring send rate removes that incentive.

**Success Metric:** No agent with ≥ 50 tickets/month falls below 50% survey send rate.

**Note:** Requires HR alignment before implementation. Do not implement without their input.

---

### REC-05: Target Navigation and Connectivity with Root Cause Analysis *(P2)*
**Category:** Service Quality  
**Owner:** Product / Service Engineering + Operations  
**Timeline:** 90 days (separate workstream)

**What:** Initiate a targeted root cause analysis for the two lowest-scoring, highest-volume issue categories: Navigation and Connectivity. Use verbatim themes from this project as input to the RCA.

**Why:** CSAT score improvement requires both measurement accuracy (addressed in REC-01 through REC-04) and actual service quality improvement. Navigation and Connectivity represent the highest-impact service improvement opportunity.

**Success Metric:** Average CSAT score in these two categories improves by ≥ 0.3 points within 6 months of RCA-driven fixes.

---

### REC-06: Implement AI-Powered Priority Verbatim Routing *(P2)*
**Category:** AI Automation  
**Owner:** BA Lead + Call Center Operations  
**Timeline:** 30 days (using existing AI pipeline)

**What:** The AI verbatim classifier already flags priority comments (unresolved issues, safety concerns, extreme dissatisfaction). Implement a workflow — via n8n or Power Automate — that automatically routes flagged verbatims to the relevant team lead within 24 hours of survey completion.

**Why:** Currently, priority comments sit in the survey platform and are reviewed monthly at best. 24-hour routing allows the team lead to do a service recovery call with the customer while the experience is still fresh.

**Success Metric:** 100% of priority-flagged verbatims routed to team lead within 24 hours. Service recovery call attempted within 48 hours.

---

### REC-07: Shorten the Survey to 2 Questions *(P3)*
**Category:** Survey Design  
**Owner:** Survey Platform Admin + VP Customer Experience  
**Timeline:** 60 days (requires brand/CX approval)

**What:** Test a two-question survey variant (CSAT + one optional verbatim) against the current [X]-question version using A/B testing on a 50% traffic split over 30 days.

**Why:** Response rate analysis suggests survey length may be a completion barrier. Industry research generally supports shorter surveys yielding higher completion rates — but this should be validated in the OnStar context before full rollout.

**Success Metric:** If short survey A/B test shows ≥ 5 percentage point improvement in completion rate with no significant change in score distribution, recommend full rollout.

---

### REC-08: Publish Live CSAT Dashboard to All Team Leads *(P3)*
**Category:** Visibility / Culture  
**Owner:** BA Lead + IT  
**Timeline:** 30 days (Power BI already built)

**What:** Grant read-only Power BI dashboard access to all team leads and the call center director. Include team-level (not agent-level) CSAT and send rate metrics updated daily.

**Why:** Teams that can see their own performance data in real time are better positioned to self-manage. Currently, team leads receive monthly reports. Daily visibility changes the feedback loop from monthly to continuous.

**Success Metric:** Dashboard is accessed at least 3x per week by ≥ 80% of team leads within 60 days of launch.

---

## Implementation Roadmap

```
MONTH 6        MONTH 7        MONTH 8        MONTH 9        MONTH 10
   │               │               │               │               │
   ├─ REC-03 ─────►│               │               │               │
   │  (Survey timing)              │               │               │
   │               │               │               │               │
   ├─ REC-01 ───────────────►│     │               │               │
   │  (Trigger rules)              │               │               │
   │               │               │               │               │
   ├─ REC-02 ────────────────────►││               │               │
   │  (Decision tree)              │               │               │
   │               │               │               │               │
   ├─ REC-06 ──────────────►│      │               │               │
   │  (Priority routing)           │               │               │
   │               │               │               │               │
   │               ├─ REC-04 ──────────────────►│  │               │
   │               │  (Scorecard update)           │               │
   │               │               │               │               │
   │               ├─ REC-05 ───────────────────────────────►│     │
   │               │  (Nav/Connectivity RCA)                       │
   │               │               │               │               │
   │               │               ├─ REC-07 A/B ─►│               │
   │               │               │  (Survey length)              │
   │               │               │               │               │
   ├─ REC-08 ──────►│              │               │               │
      (Dashboard)
```

---

## Expected Cumulative Impact (90 Days Post-Implementation)

| Metric | Current | Target | Recommendation Driving It |
|--------|---------|--------|--------------------------|
| Survey send rate | [X]% | ≥ 70% | REC-01, REC-02 |
| Response rate | [X]% | +5 pp | REC-03, REC-07 |
| Average CSAT | [X] / 5 | +0.3 | REC-04, REC-05 |
| Priority verbatim routing | Ad hoc | 100% within 24h | REC-06 |

---

## Appendix: Recommendation Scoring Matrix

| Rec | Impact | Effort | Speed | Priority |
|-----|--------|--------|-------|----------|
| REC-01 | High | Low | Fast | **P1** |
| REC-02 | High | Medium | Medium | **P1** |
| REC-03 | Medium | Low | Fast | **P1** |
| REC-04 | High | Medium | Medium | **P2** |
| REC-05 | High | High | Slow | **P2** |
| REC-06 | Medium | Low | Fast | **P2** |
| REC-07 | Medium | Medium | Medium | **P3** |
| REC-08 | Medium | Low | Fast | **P3** |
