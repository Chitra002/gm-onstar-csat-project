# PROJECT CHARTER
## GM OnStar All Star — CSAT Improvement Initiative

**Document Version:** 1.0  
**Date:** June 2026  
**Project Sponsor:** VP, Customer Experience — OnStar  
**BA Lead:** Chitra (Queen) Dubey  
**Status:** Approved

---

## 1. Business Case

OnStar is a subscription-based connected vehicle services platform. Customer satisfaction directly impacts renewal rates, referral volume, and brand perception within GM's broader ecosystem. The call center is the primary human touchpoint for OnStar customers.

Current monitoring gaps:
- Survey response rates are below industry benchmark (believed to be approximately 15–25%; verify with vendor)
- Agent-reported insights suggest ticket closure method may suppress survey triggers
- Negative experiences may be systematically excluded from CSAT measurement
- Leadership is making service design decisions on incomplete satisfaction data

**Risk if unaddressed:** Churn risk is underestimated. Service failures go undetected. Performance management data is skewed in favor of agents who avoid surveys rather than those who deliver superior service.

---

## 2. Project Scope

### In Scope
- 6 months of historical call/ticket data from the OnStar call center
- CSAT survey send, open, and completion data for the same period
- Telephony (ACD) data: handle time, transfers, abandons
- QA scorecard data by agent
- Four analysis tracks:
  - Track 1: Survey trigger analysis by closure code
  - Track 2: Response rate drivers
  - Track 3: CSAT score patterns
  - Track 4: Agent closure behavior analysis

### Out of Scope
- Social media sentiment analysis
- IVR redesign
- Product/feature satisfaction analysis (separate workstream)
- Individual agent disciplinary actions (HR scope)

---

## 3. Success Criteria

| Metric | Target |
|--------|--------|
| Survey send rate visibility | Baseline established by Month 2 |
| Closure code → survey trigger mapping | 100% of active codes mapped by Month 3 |
| Response rate improvement (post-implementation) | +10 percentage points within 90 days of recommendation implementation |
| CSAT score improvement | +0.3 points on 1–5 scale within 90 days |
| Stakeholder satisfaction with project | Sponsor sign-off on findings and recommendations |

---

## 4. Team & RACI

| Role | Name | R | A | C | I |
|------|------|---|---|---|---|
| Project Sponsor | VP Customer Experience | | ✅ | | |
| BA Lead | Chitra (Queen) Dubey | ✅ | ✅ | | |
| Data Engineer | TBD | ✅ | | | |
| Call Center Ops Lead | TBD | | | ✅ | ✅ |
| QA / WFM Analyst | TBD | | | ✅ | |
| CRM Admin | TBD | ✅ | | | |
| IT / Data Access | TBD | ✅ | | | |
| Survey Platform Admin | TBD | ✅ | | | |

**R** = Responsible | **A** = Accountable | **C** = Consulted | **I** = Informed

---

## 5. Key Assumptions

- Data access will be provisioned within 3 weeks of project kickoff
- Ticket IDs are consistent across CRM and survey platform
- Survey platform vendor can provide trigger rule documentation
- Historical data is available and complete for the 6-month analysis window
- Agents are not aware this behavioral analysis is in progress (to avoid data contamination)

---

## 6. Key Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Data access delays | Medium | High | Escalate to sponsor at Week 3 if not resolved |
| Ticket ID mismatch across systems | Medium | High | Data reconciliation session with CRM admin in Week 2 |
| Agents modify closure behavior once project is known | Low | High | Limit project communication to leadership and core team |
| Survey vendor unable to provide trigger rules | Low | Medium | Reverse-engineer from data if necessary |
| Incomplete historical data (system gaps) | Medium | Medium | Document gaps; adjust analysis window if needed |

---

## 7. Timeline Summary

| Milestone | Target Date |
|-----------|-------------|
| Project kickoff | Month 1, Week 1 |
| Data access provisioned | Month 1, Week 3 |
| Master dataset complete | End of Month 2 |
| Analysis Tracks 1–2 complete | End of Month 3 |
| Analysis Tracks 3–4 complete | End of Month 4 |
| Findings report draft | Month 5, Week 2 |
| Recommendations workshop | Month 5, Week 3 |
| Executive final presentation | Month 6, Week 1 |
| Implementation roadmap delivered | Month 6, Week 2 |

---

## 8. Budget Considerations

*(To be confirmed with sponsor)*

- Data analyst contractor (if needed): TBD
- Survey platform API access / additional data exports: TBD
- Azure Text Analytics / AI API costs for verbatim analysis: Estimated low (< $500 for 6-month volume)
- Power BI Pro license (if not already provisioned): ~$10/user/month

---

## 9. Sign-Off

| Name | Role | Signature | Date |
|------|------|-----------|------|
| | VP Customer Experience | | |
| Chitra (Queen) Dubey | BA Lead | | |
| | Call Center Director | | |
