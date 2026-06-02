# Findings Report
## GM OnStar CSAT Improvement Initiative

**Version:** DRAFT — Month 5  
**Prepared by:** Chitra (Queen) Dubey, BA Lead  
**Analysis Period:** [Start Date] – [End Date]  
**Status:** Pending Ops Validation

---

## Executive Summary

*(3–4 sentences maximum. Written last. Sponsor reads this first.)*

This analysis of [X] calls and [Y] survey interactions across the OnStar call center confirms the central hypothesis: ticket closure method is a statistically significant driver of whether a customer receives a CSAT survey. The gap between highest and lowest closure code groups is [X]%, representing an estimated [N] missing survey responses per month. Agent-level patterns suggest a subset of agents are disproportionately using closure codes that suppress survey triggers, whether intentional or through inadequate training. Four tracks of analysis yield eight prioritized recommendations.

---

## 1. Analysis Overview

### Data Summary
| Source | Records | Date Range | Quality |
|--------|---------|-----------|---------|
| CRM Tickets | | | % clean |
| Survey Data | | | % match rate to tickets |
| Telephony | | | % match rate |
| QA Scorecards | | | % coverage |

### Key Metrics — Analysis Period
| Metric | Value | Industry Benchmark* |
|--------|-------|-------------------|
| Total tickets | | N/A |
| Overall survey send rate | | ~60–80% |
| Overall survey response rate | | ~15–25% |
| Average CSAT score | / 5.0 | ~4.0 / 5.0 |
| First contact resolution rate | | ~70–75% |

*Industry benchmarks are approximate. Verify with Medallia/Qualtrics vendor for current contact center norms.*

---

## 2. Track 1 Findings — Survey Trigger Analysis

### 2.1 Closure Code Survey Send Rates

**Key Finding:** Survey send rates vary significantly across closure code groups, ranging from [X]% to [Y]%. This difference is statistically significant (χ² = [value], p < 0.01), meaning it is not due to random variation.

*(Insert closure_code_survey_rates table here)*

**Interpretation:** The variation in send rates maps directly to whether the call center's survey trigger rules fire for a given closure code. Codes grouped as "Resolved - No Follow-Up" and "Administrative" consistently suppress survey sends. This is partially by design (administrative closures should not trigger surveys) but the volume of tickets closed with low-trigger codes appears inflated relative to what the operational context would predict.

### 2.2 Survey Suppression Estimate

Using the best-performing closure group as a baseline:
- **Estimated surveys missed per month:** [N]
- **Estimated surveys missed over 6-month period:** [N]
- **Implication for CSAT score reliability:** If suppressed interactions skew negative (which Transfer and Escalation data suggest), reported CSAT may be overstating true satisfaction by approximately [X] points.

*(This estimate should be validated with Ops before presenting to leadership.)*

---

## 3. Track 2 Findings — Response Rate Drivers

### 3.1 Handle Time vs. Response Rate
Calls in the **3–7 minute bucket** showed the highest survey response rate at [X]%. Very short calls (0–3 min) had the lowest at [Y]%, suggesting customers feel insufficient time was invested in their issue.

### 3.2 Survey Timing vs. Response Rate
Response rates drop significantly when surveys are sent more than 24 hours after ticket closure. **Same-day sends achieved [X]%** response rate vs. [Y]% for 4+ day delays.

**Recommendation implication:** Tighten survey send window with vendor.

### 3.3 Transfer Count vs. Response Rate
Customers who experienced 2+ transfers had a **[X]% lower response rate** than zero-transfer calls. However, when they did respond, their CSAT scores were significantly lower ([avg score] vs [avg score]).

---

## 4. Track 3 Findings — CSAT Score Patterns

### 4.1 CSAT by Issue Category
*(Insert chart/table here)*

**Navigation** and **Connectivity** issues show the lowest average scores. These are also the highest-volume categories, making them priority targets for service improvement.

### 4.2 First Contact Resolution Impact
FCR calls scored **[X] points higher** on average than non-FCR calls. FCR is the single strongest predictor of CSAT score in the dataset.

### 4.3 Verbatim Theme Analysis (AI-Classified)

Top themes in negative verbatims:
1. **[Theme 1]** — [X]% of negative comments
2. **[Theme 2]** — [X]%
3. **[Theme 3]** — [X]%

[N] verbatims were flagged by the AI classifier as priority escalation comments — indicating unresolved issues or safety-adjacent concerns. These were reviewed and [N] were routed to operations.

---

## 5. Track 4 Findings — Agent Behavior Analysis

*This section presents distributional data only. Individual agent findings are handled separately through the team lead coaching process.*

### 5.1 Survey Send Rate Distribution
Agent survey send rates follow an approximately normal distribution with a mean of [X]% and standard deviation of [Y]%. [N] agents (out of [total]) fell more than 2 standard deviations below the mean, indicating statistically anomalous low send rates.

### 5.2 Closure Code Patterns
Agents with low survey send rates showed a disproportionate use of "Resolved - No Follow-Up" and "Resolved - Administrative" closure codes ([X]% of their closures vs. [Y]% team average).

### 5.3 QA Score Correlation
Agents with low survey send rates also trended toward lower QA scores in the **call closure** subcategory ([avg] vs. [avg] team average), suggesting a potential training gap around proper closure technique rather than deliberate avoidance in most cases.

---

## 6. Summary of Key Findings

| # | Finding | Track | Confidence |
|---|---------|-------|-----------|
| 1 | Survey send rate varies from [X]% to [Y]% by closure code — statistically significant | 1 | High |
| 2 | Estimated [N] surveys missed per month due to low-trigger closure code usage | 1 | Medium |
| 3 | Same-day survey sends achieve [X]% higher response rate than 4+ day delays | 2 | High |
| 4 | FCR calls score [X] points higher in CSAT than non-FCR calls | 3 | High |
| 5 | Navigation and Connectivity are lowest-scoring, highest-volume categories | 3 | High |
| 6 | [N] agents show statistically anomalous low survey send rates | 4 | Medium |
| 7 | Low send rate agents correlate with lower QA closure subscores | 4 | Medium |
| 8 | [N] priority-flag verbatims identified requiring follow-up | 3 | High |

---

## 7. Limitations & Caveats

- Industry benchmarks cited are approximate and sourced from general contact center literature. Verify with survey vendor for OnStar-specific benchmarks.
- QA scores are available for only [X]% of tickets, limiting correlation analysis.
- Causal direction between closure code usage and low CSAT cannot be fully established from this data — it is possible that harder calls (which naturally score lower) also use different closure codes.
- AI verbatim classifications were validated on a 10% sample with [X]% agreement rate. Full manual audit was not performed.

---

## 8. Next Steps

See `docs/recommendations.md` for the full prioritized recommendation set and implementation roadmap.
