# CHANGELOG
## GM OnStar CSAT Improvement Project

All notable changes to this project are documented here.  
Format: `[Version] YYYY-MM-DD — Description`

---

## [1.0.0] — 2026-06-02 — Initial Repository Build

### Added
- `README.md` — Full project overview, structure, and getting started guide
- `PROJECT_CHARTER.md` — Scope, RACI, risks, success criteria
- `CHANGELOG.md` — This file
- `requirements.txt` — Python dependencies
- `.gitignore` — Data security and environment file exclusions
- `docs/data_dictionary.md` — Full field definitions for master dataset
- `docs/meeting_cadence.md` — All recurring and one-time meetings
- `docs/findings_report.md` — Findings report template (populated in Month 5)
- `docs/recommendations.md` — 8 prioritized recommendations + roadmap
- `sql/04_master_join.sql` — Master dataset join logic (Snowflake)
- `sql/05_validation_checks.sql` — 8 data quality validation queries
- `data/sample/sample_data_generator.py` — Synthetic data generator (3,000 rows default)
- `src/analysis/survey_trigger_analysis.py` — Track 1 analysis module
- `src/ai_automation/verbatim_classifier.py` — AI theme classification via Claude API
- `src/ai_automation/insight_summarizer.py` — AI weekly digest generator
- `src/ai_automation/coaching_recommender.py` — AI agent coaching note generator
- `dashboards/powerbi_spec.md` — 5-page Power BI dashboard specification
- `config/settings.yaml` — Central project configuration
- `.github/workflows/data_pipeline.yml` — Automated weekly CI/CD pipeline

---

## Upcoming

### [1.1.0] — Planned Month 2
- `sql/01_ticket_extract.sql`
- `sql/02_survey_extract.sql`
- `sql/03_telephony_extract.sql`
- `src/ingestion/salesforce_connector.py`
- `src/ingestion/medallia_connector.py`
- `src/cleaning/deduplication.py`
- `src/cleaning/feature_engineering.py`
- `src/cleaning/validation.py`
- `config/column_mappings.yaml`

### [1.2.0] — Planned Month 3–4
- `notebooks/01_data_exploration.ipynb`
- `notebooks/02_survey_trigger_analysis.ipynb`
- `src/analysis/response_rate_analysis.py`
- `src/analysis/csat_score_analysis.py`
- `src/analysis/agent_behavior_analysis.py`

### [1.3.0] — Planned Month 5
- `docs/findings_report.md` — Populated with real findings
- `src/ai_automation/anomaly_detector.py`
- `src/reporting/weekly_digest.py`
- `notebooks/05_agent_behavior_analysis.ipynb`

### [2.0.0] — Planned Month 6
- Final executive presentation assets
- Implementation roadmap with owner sign-offs
- Project closeout documentation
