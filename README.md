# 📊 GM OnStar CSAT Improvement Project
### Business Analytics | AI-Augmented | Call Center Intelligence

> ⚠️ **Portfolio Project Disclaimer:** This is a portfolio project 
> demonstrating a business analytics methodology applied to a call 
> center CSAT scenario. All data is synthetic and generated for 
> demonstration purposes only. No real GM, OnStar, or customer data 
> is used anywhere in this project.
---

## 🔍 Project Overview

**Organization:** General Motors — OnStar All Star Project  
**Role:** Senior Business Analyst  
**Duration:** 6 months (Phases 0–5)  
**Objective:** Analyze 6 months of call center data and CSAT survey results to identify survey trigger gaps, response rate drivers, and actionable service improvements — with AI automation integrated at every viable step.

---

## 🧠 Problem Statement

> Customer satisfaction survey response rates and scores are inconsistently captured across the OnStar call center. Agent-reported ticket closure behaviors may be influencing which interactions receive surveys, creating blind spots in CSAT measurement and potentially masking service quality issues.

**Key Hypothesis:**  
The *method* by which an agent closes a ticket determines whether a CSAT survey is triggered. If agents — knowingly or unknowingly — use closure codes that suppress survey sends, we are systematically missing data on poor customer experiences.

---

## 🗂️ Repository Structure

```
gm-onstar-csat-project/
│
├── README.md                        ← You are here
├── PROJECT_CHARTER.md               ← Scope, stakeholders, success criteria
├── CHANGELOG.md                     ← Version history of deliverables
│
├── docs/
│   ├── data_dictionary.md           ← All fields, sources, transformations
│   ├── methodology.md               ← Analysis approach and statistical methods
│   ├── stakeholder_map.md           ← RACI matrix and communication plan
│   ├── meeting_cadence.md           ← All recurring and one-time meetings
│   ├── findings_report.md           ← Full narrative findings (Month 5)
│   └── recommendations.md           ← Prioritized recommendations + owners
│
├── data/
│   ├── raw/                         ← Source extracts (never modified)
│   │   └── .gitkeep
│   ├── processed/                   ← Cleaned, joined master dataset
│   │   └── .gitkeep
│   └── sample/
│       └── sample_data_generator.py ← Synthetic data for testing/demo
│
├── sql/
│   ├── 01_ticket_extract.sql        ← CRM/Salesforce ticket pull
│   ├── 02_survey_extract.sql        ← Survey platform data pull
│   ├── 03_telephony_extract.sql     ← ACD/call data pull
│   ├── 04_master_join.sql           ← Master dataset join logic
│   └── 05_validation_checks.sql     ← Data quality validation queries
│
├── src/
│   ├── ingestion/
│   │   ├── salesforce_connector.py  ← Salesforce API data pull
│   │   ├── medallia_connector.py    ← Survey platform connector
│   │   └── snowflake_loader.py      ← Data warehouse loader
│   │
│   ├── cleaning/
│   │   ├── deduplication.py         ← Ticket dedup logic
│   │   ├── feature_engineering.py   ← Derived columns and buckets
│   │   └── validation.py            ← Data quality checks
│   │
│   ├── analysis/
│   │   ├── survey_trigger_analysis.py     ← Track 1: closure code → survey rate
│   │   ├── response_rate_analysis.py      ← Track 2: response rate drivers
│   │   ├── csat_score_analysis.py         ← Track 3: score patterns
│   │   └── agent_behavior_analysis.py     ← Track 4: agent closure patterns
│   │
│   ├── ai_automation/
│   │   ├── verbatim_classifier.py         ← AI theme tagging for open text
│   │   ├── anomaly_detector.py            ← AI-powered outlier flagging
│   │   ├── insight_summarizer.py          ← LLM weekly insight digest
│   │   └── coaching_recommender.py        ← AI agent coaching suggestions
│   │
│   ├── visualization/
│   │   ├── dashboard_builder.py           ← Power BI / Plotly chart specs
│   │   └── executive_charts.py            ← Presentation-ready visuals
│   │
│   └── reporting/
│       ├── weekly_digest.py               ← Automated weekly email digest
│       └── monthly_deck_generator.py      ← Auto-generate stakeholder slides
│
├── notebooks/
│   ├── 01_data_exploration.ipynb          ← EDA and sanity checks
│   ├── 02_survey_trigger_analysis.ipynb   ← Track 1 analysis
│   ├── 03_response_rate_analysis.ipynb    ← Track 2 analysis
│   ├── 04_csat_score_deep_dive.ipynb      ← Track 3 analysis
│   └── 05_agent_behavior_analysis.ipynb   ← Track 4 analysis
│
├── dashboards/
│   └── powerbi_spec.md                    ← Power BI dashboard design spec
│
├── config/
│   ├── settings.yaml                      ← Environment and project config
│   └── column_mappings.yaml               ← Source-to-target field mapping
│
├── tests/
│   ├── test_cleaning.py                   ← Unit tests for data cleaning
│   ├── test_analysis.py                   ← Unit tests for analysis logic
│   └── test_ai_modules.py                 ← Unit tests for AI automation
│
└── .github/
    └── workflows/
        ├── data_pipeline.yml              ← Scheduled data refresh CI/CD
        └── weekly_digest.yml              ← Automated weekly digest trigger
```

---

## 🤖 AI Automation Integration

AI is embedded at 5 points in this project:

| Step | AI Application | Tool/Method |
|------|---------------|-------------|
| **Verbatim Analysis** | Theme classification of open-text survey responses | Claude API / Azure Text Analytics |
| **Anomaly Detection** | Flag agents or days with statistically unusual closure patterns | Isolation Forest (scikit-learn) |
| **Weekly Insight Digest** | Auto-generate plain-English summary of weekly CSAT trends | LLM prompt chain (Claude API) |
| **Coaching Suggestions** | Generate personalized coaching notes per agent based on pattern data | Claude API with structured prompt |
| **Slide Generation** | Auto-populate monthly executive PowerPoint from data outputs | python-pptx + LLM narrative |

---

## 📅 Project Phases

| Phase | Name | Timeline | Status |
|-------|------|----------|--------|
| 0 | Project Framing & Charter | Week 1 | ✅ Complete |
| 1 | Stakeholder Alignment & Team Assembly | Week 2–3 | ✅ Complete |
| 2 | Data Identification & Extraction | Month 1–2 | 🔄 In Progress |
| 3 | Data Cleaning & Master Dataset Build | Month 2 | ⏳ Pending |
| 4 | Analysis (4 Tracks) | Month 3–4 | ⏳ Pending |
| 5 | Findings, Recommendations & Delivery | Month 5–6 | ⏳ Pending |

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Data Extraction | Salesforce SOQL, Snowflake SQL, REST APIs |
| Data Processing | Python (pandas, numpy), SQL |
| Analysis | Python, Excel (pivot tables), Jupyter Notebooks |
| AI/ML | Claude API (Anthropic), scikit-learn, Azure Text Analytics |
| Visualization | Power BI, Plotly, Matplotlib |
| Reporting | python-pptx, Jinja2 templates |
| Automation | GitHub Actions, n8n workflows |
| Documentation | Markdown, Confluence-compatible |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/gm-onstar-csat-project.git
cd gm-onstar-csat-project

# Install dependencies
pip install -r requirements.txt

# Generate sample data for testing
python data/sample/sample_data_generator.py

# Run data validation
python src/cleaning/validation.py

# Launch analysis notebook
jupyter notebook notebooks/01_data_exploration.ipynb
```

---

## 📋 Key Deliverables

1. **Data Dictionary** — `docs/data_dictionary.md`
2. **Analytical Dashboard** — Power BI (spec in `dashboards/powerbi_spec.md`)
3. **Findings Report** — `docs/findings_report.md`
4. **Recommendations Deck** — `docs/recommendations.md`
5. **Implementation Roadmap** — Final section of `docs/recommendations.md`

---

## 👤 Author

**Chitra Dubey**  
Senior Business Analyst | Data & BI Analyst  
TechFios — Supporting Realty Income (S&P 500 Commercial REIT)  
M.S. Information Systems & Technology, University of North Texas  

Certifications: IBM Data Science | Google Prompt Engineering | ITIL V4 | CompTIA Security+ | Azure Fundamentals

---

## 📄 License

This project is for portfolio and demonstration purposes. All data used is synthetic.
