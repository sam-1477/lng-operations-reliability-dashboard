# LNG Operations Technical Reliability Dashboard
## Complete Project Architecture Plan

**Author:** Samuel Talpa, B.Eng Mechanical Engineering  
**Target Role:** ExxonMobil PNG Graduate Engineer — Operations Technical  
**Date:** July 2026  
**Repository:** `lng-reliability-dashboard`

---

## 1. Project Objective

Build a credible, honest, GitHub-hosted portfolio project that demonstrates the engineering thinking
expected of an Operations Technical graduate engineer at an LNG facility. The dashboard uses
**publicly available industrial datasets** adapted into LNG-style equipment categories. It does NOT
claim to use, possess, or simulate ExxonMobil or PNG LNG confidential data.

The project shows that the candidate can:

- Think in terms of reliability engineering fundamentals (MTTR, MTBF, Availability)
- Structure an asset hierarchy used in LNG operations
- Perform condition monitoring analysis on rotating equipment (compressors)
- Assess pipeline and process safety incident risk from regulatory data
- Rank maintenance priorities using data, not gut feel
- Produce inspection-style summaries for mechanical integrity
- Use AI/LLM tools responsibly to generate engineering commentary
- Present technical work professionally on GitHub, CV, and LinkedIn

---

## 2. Version 1 Scope

### 2.1 In Scope

| Feature | Description |
|---------|-------------|
| Asset Register | 20–30 assets mapped to LNG equipment categories (compressors, turbines, pumps, heat exchangers, pipelines, storage tanks, instrumentation) |
| Downtime & Failure Summary | Bar charts, Pareto of failure causes, downtime hours by equipment type |
| Compressor Condition Monitoring | MetroPT-3 sensor data: vibration, temperature, pressure trends with threshold bands |
| Pipeline/LNG Incident Risk | PHMSA incident frequency, root cause distribution, consequence severity |
| Maintenance Priority Ranking | Risk-based ranking (likelihood consequence matrix) for each asset |
| Mechanical Integrity Summary | Inspection-style checklist summary (thickness, corrosion rate, next inspection date) |
| Reliability KPIs | MTTR, MTBF-estimate, Availability-estimate, Failure Count, Downtime Hours |
| AI-Assisted Recommendations | LLM-generated commentary on top-3 failure modes and suggested mitigations |
| Excel Workbook | All data, calculations, and charts in a single Excel workbook for non-Python reviewers |

### 2.2 Out of Scope (V2+)

- Real-time streaming data
- Interactive web dashboard (Streamlit/Dash)
- Machine learning predictive models (RUL, anomaly detection)
- Docker deployment
- Multi-tenancy

### 2.3 Technology Stack (V1)

- **Data Processing:** Python 3.11 (pandas, numpy)
- **Visualization:** matplotlib, seaborn, plotly express
- **Excel Integration:** openpyxl, xlsxwriter
- **LLM Integration:** OpenRouter API (Claude Sonnet 4) or local via Hermes
- **Version Control:** Git + GitHub
- **Documentation:** Markdown
- **Environment:** Windows 11, VS Code, Git Bash

---

## 3. Dataset Selection and Rationale

### 3.1 Primary Datasets

| # | Dataset | Source | Why Chosen | LNG Mapping |
|---|---------|--------|------------|-------------|
| 1 | **PHMSA Gas Transmission & LNG Incident Reports** | U.S. DOT Pipeline and Hazardous Materials Safety Administration (public) | Real, auditable pipeline incident data with root cause classification, consequence data, and regulatory findings. This is the strongest dataset for demonstrating pipeline risk thinking. | Direct mapping: gas transmission pipelines map to LNG feed/product pipelines. Incident causes (corrosion, equipment failure, excavation damage) are identical to LNG pipeline risks. |
| 2 | **MetroPT-3 Compressor Predictive Maintenance** | UCI Machine Learning Repository / Zenodo | Contains real sensor data from an industrial air compressor (pressure, temperature, vibration, RPM, electrical signals) at 1 Hz over multiple months. This is the closest public dataset to LNG refrigerant/propane compressor monitoring. | Map to LNG propane/MR compressor trains. The sensor types (vibration, temperature, pressure) are the same measurements taken on LNG compressor packages. |
| 3 | **Microsoft Azure Predictive Maintenance** | Kaggle / Microsoft Open Datasets | Contains failure histories, maintenance records, machine features, and telemetry for rotating equipment. Adds the maintenance-log dimension missing from MetroPT-3. | Map failure modes (bearing, seal, overheating) to LNG pump and turbine failure categories. |

### 3.2 Why These Three Together

- PHMSA gives you **process safety and regulatory credibility** — an ExxonMobil reviewer will recognize PHMSA data
- MetroPT-3 gives you **rotating equipment depth** — compressors are the heart of any LNG plant
- Azure PdM gives you **maintenance-log richness** — failure codes, maintenance actions, component replacements

No single public dataset covers all three. Combined, they simulate the multi-source data an Operations Technical engineer works with daily.

### 3.3 Future Additions (V2)

- **UCI Hydraulic System Condition Monitoring:** For LNG hydraulic valve actuator and blowdown system simulation
- **NASA CMAPSS (Turbofan RUL):** For remaining useful life prediction on gas turbine drivers

---

## 4. Repository Folder Structure

```
lng-reliability-dashboard/
│
├── README.md                          # Project overview, badge, quick-start
├── LICENSE                            # MIT License
├── .gitignore                         # Python, Excel temp files, venv
├── requirements.txt                   # Python dependencies
│
├── docs/
│   ├── project_charter.md             # Why this project, who it's for, what it proves
│   ├── architecture_plan.md           # THIS FILE — complete architecture
│   ├── data_sources.md                # Dataset details, download links, attribution
│   ├── assumptions_and_limitations.md # Honesty document — what's real, what's simulated
│   └── portfolio_presentation_guide.md # How to present on GitHub/CV/LinkedIn
│
├── data/
│   ├── raw/
│   │   ├── phmsa_incidents.csv        # Downloaded PHMSA incident data
│   │   ├── metropt3_sensors.csv       # Downloaded MetroPT-3 sensor readings
│   │   └── azure_pdm_maint.csv        # Downloaded Azure PdM maintenance records
│   ├── processed/
│   │   ├── asset_register.csv         # Cleaned asset register with LNG mapping
│   │   ├── downtime_log.csv           # Aggregated downtime events
│   │   ├── failure_summary.csv        # Failure count by asset/type
│   │   ├── compressor_health.csv      # MetroPT-3 derived health indicators
│   │   ├── pipeline_risk_scores.csv   # PHMSA-derived risk scores
│   │   └── reliability_kpis.csv       # Computed MTTR, MTBF, Availability
│   └── README.md                      # Data dictionary
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb         # Load raw datasets, clean, validate
│   ├── 02_asset_register.ipynb        # Build LNG-style asset hierarchy
│   ├── 03_downtime_analysis.ipynb     # Failure/downtime EDA
│   ├── 04_compressor_monitoring.ipynb # MetroPT-3 sensor trends
│   ├── 05_pipeline_risk.ipynb         # PHMSA incident analysis
│   ├── 06_maintenance_ranking.ipynb   # Priority ranking logic
│   ├── 07_reliability_kpis.ipynb      # MTTR, MTBF, Availability computation
│   ├── 08_mechanical_integrity.ipynb  # Inspection summary
│   ├── 09_ai_recommendations.ipynb    # LLM-assisted engineering comments
│   └── 10_export_excel.ipynb          # Generate final Excel workbook
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py                 # Functions to load raw datasets
│   ├── data_cleaner.py                # Standardize, impute, validate
│   ├── kpi_calculator.py              # MTTR, MTBF, Availability functions
│   ├── risk_matrix.py                 # Likelihood consequence scoring
│   ├── plot_templates.py              # Reusable matplotlib/seaborn plot configs
│   └── lng_mappings.py                # Equipment category lookup tables
│
├── excel/
│   └── lng_reliability_dashboard.xlsx # Master Excel workbook (see Section 7)
│
├── reports/
│   └── reliability_summary_report.md  # Generated summary report
│
└── screenshots/
    ├── dashboard_overview.png
    ├── compressor_trends.png
    ├── pipeline_risk_heatmap.png
    ├── maintenance_priority_matrix.png
    └── reliability_kpi_summary.png
```

---

## 5. File List — Creation Order

Build in this exact order. Each step must succeed before moving to the next.

| Step | File | Purpose | Dependencies |
|------|------|---------|--------------|
| 1 | `.gitignore` | Prevent committing venv, __pycache__, Excel temp files, .ipynb_checkpoints | None |
| 2 | `requirements.txt` | Pin all Python package versions | None |
| 3 | `docs/project_charter.md` | Project vision, scope, target audience | None |
| 4 | `docs/data_sources.md` | Dataset descriptions, download links, attribution | None |
| 5 | `docs/assumptions_and_limitations.md` | Honesty document | None |
| 6 | `docs/architecture_plan.md` | This document | None |
| 7 | `docs/portfolio_presentation_guide.md` | CV/LinkedIn/GitHub presentation strategy | None |
| 8 | `data/README.md` | Data dictionary | None |
| 9 | `src/lng_mappings.py` | Equipment category dictionaries | None |
| 10 | `src/data_loader.py` | CSV loading with validation | None |
| 11 | `src/data_cleaner.py` | Cleaning pipeline functions | None |
| 12 | `notebooks/01_data_cleaning.ipynb` | Execute cleaning, produce processed CSVs | 8, 9, 10 |
| 13 | `notebooks/02_asset_register.ipynb` | Build and validate asset register | 11 |
| 14 | `src/kpi_calculator.py` | KPI computation functions | None |
| 15 | `src/risk_matrix.py` | Risk scoring functions | None |
| 16 | `src/plot_templates.py` | Standardized plot styling (ExxonMobil-like colors) | None |
| 17 | `notebooks/03_downtime_analysis.ipynb` | Downtime EDA and Pareto | 12 |
| 18 | `notebooks/04_compressor_monitoring.ipynb` | Sensor trend analysis | 12 |
| 19 | `notebooks/05_pipeline_risk.ipynb` | PHMSA incident analysis | 12 |
| 20 | `notebooks/06_maintenance_ranking.ipynb` | Priority matrix | 12, 14 |
| 21 | `notebooks/07_reliability_kpis.ipynb` | KPI computation and visualization | 12, 13 |
| 22 | `notebooks/08_mechanical_integrity.ipynb` | Inspection summary | 12, 14 |
| 23 | `notebooks/09_ai_recommendations.ipynb` | LLM commentary on top failures | 11-21 (all analysis) |
| 24 | `notebooks/10_export_excel.ipynb` | Generate Excel workbook | All above |
| 25 | `README.md` | Project landing page (write LAST) | All above |
| 26 | `LICENSE` | MIT License | None |

---

## 6. Dashboard Pages / Tabs

The "dashboard" in V1 is a combination of Jupyter notebook outputs (saved as PNG screenshots) and
an Excel workbook. There is no web UI in V1. Each "page" below is either a notebook section or
an Excel sheet.

### 6.1 Dashboard Overview Page

- Project title and subtitle
- Date of last data refresh
- Asset count, total downtime (hours), total failure count
- Overall Availability % (gauge-style if in Excel)
- Quick links to detailed sections

### 6.2 Asset Register

- Table: Asset ID, Equipment Name, LNG Category, Subsystem, Criticality Rating (A/B/C)
- LNG categories: Compressor Trains, Gas Turbines, Centrifugal Pumps, Air-Cooled Heat Exchangers, Cryogenic Heat Exchangers, Pressure Vessels, Storage Tanks, Pipelines, Instrumentation & Control, Electrical Systems
- Color coding by criticality

### 6.3 Downtime & Failure Summary

- Bar chart: Downtime hours by equipment category
- Pareto chart: Failure causes ranked
- Table: Top-10 failure events with duration and consequence
- Monthly failure trend line

### 6.4 Compressor Condition Monitoring

- Multi-panel trend plot: vibration (mm/s RMS), discharge temperature (°C), suction pressure (bar), motor current (A)
- Threshold bands: Green (< warning), Amber (warning → alarm), Red (> alarm)
- Data source: MetroPT-3 adapted to "LNG Propane Compressor A"

### 6.5 Pipeline / LNG Incident Risk

- Bar chart: PHMSA incidents by root cause category
- Pie chart: Incident consequence (fire, explosion, gas release, no consequence)
- Map-style table: Incident frequency by state/location (as proxy for geographic risk)
- Text summary: Top-3 lessons for LNG pipeline integrity

### 6.6 Maintenance Priority Ranking

- Risk matrix plot: Likelihood vs. Consequence (5x5 grid)
- Table: All assets with likelihood score, consequence score, risk index, priority rank
- Color coding: Red (Priority 1), Amber (Priority 2), Green (Priority 3)

### 6.7 Mechanical Integrity Summary

- Table: Asset ID, Equipment Name, Last Inspection Date, Wall Thickness (mm), Corrosion Rate (mm/yr), Remaining Life (yrs), Next Inspection Due
- Status indicators: Satisfactory, Monitor, Action Required
- Note: These values are adapted (not real inspection data) — clearly disclosed

### 6.8 Reliability KPIs

- Summary cards: Overall MTTR (hours), Overall MTBF (days), Overall Availability (%)
- Table: KPI breakdown by equipment category
- Bar chart: Availability % by equipment type

### 6.9 AI-Assisted Engineering Recommendations

- Top-3 failure modes identified from data
- For each: failure description, probable root cause (from data), recommended mitigation
- Clearly labeled: "Generated by [LLM Model] on [Date]. Review by qualified engineer required."

---

## 7. Excel Workbook Sheet Structure

The Excel workbook (`excel/lng_reliability_dashboard.xlsx`) is the single-file deliverable for
non-Python reviewers. It contains all data and charts.

| Sheet Name | Content |
|------------|---------|
| **Dashboard** | Executive summary with key KPIs, mini charts, hyperlinks to detail sheets |
| **Asset Register** | Full asset list with LNG category, criticality, location |
| **Downtime Log** | All downtime events: start, end, duration, cause, consequence |
| **Failure Summary** | Aggregated failure counts, pivot tables, Pareto data |
| **Compressor Trends** | Tabulated MetroPT-3 data (sampled), summary statistics, embedded trend chart |
| **Pipeline Risk** | PHMSA incident summary table, root cause distribution, embedded charts |
| **Priority Matrix** | Risk-ranked asset list with likelihood/consequence scores |
| **Inspection Summary** | Mechanical integrity table with conditional formatting (red/amber/green) |
| **Reliability KPIs** | MTTR, MTBF, Availability by equipment category, embedded charts |
| **AI Recommendations** | LLM-generated text, failure mode analysis, caveats |
| **Data Dictionary** | Column definitions, units, data source references |

### Excel Formatting Standards

- Header row: Dark blue background (#003366 — ExxonMobil-style navy), white text, bold
- Green: #10b981 (cells meeting target)
- Amber: #f59e0b (cells at warning)
- Red: #ef4444 (cells needing action)
- All charts embedded on their sheets, not as separate chart sheets
- Print layout set to landscape, fit-to-width
- Sheet protection ON (no password) to prevent accidental edits

---

## 8. Data Cleaning Plan

### 8.1 PHMSA Incident Data

| Step | Action | Rationale |
|------|--------|-----------|
| 1 | Load CSV, inspect columns | Understand raw schema |
| 2 | Filter to gas transmission + LNG incidents only | Remove hazardous liquid pipelines (not LNG-relevant) |
| 3 | Standardize date formats (MM/DD/YYYY → YYYY-MM-DD) | Consistent ISO format |
| 4 | Map root cause codes to LNG-recognized categories | External Corrosion, Internal Corrosion, Equipment Failure, Operational Error, Third Party Damage, Natural Force, Other |
| 5 | Standardize consequence: None → 0, Minor → 1, Significant → 2, Major → 3 | Numeric for risk scoring |
| 6 | Drop rows with >50% missing critical fields | Data quality threshold |
| 7 | Save as `data/processed/pipeline_risk_scores.csv` | |

### 8.2 MetroPT-3 Sensor Data

| Step | Action | Rationale |
|------|--------|-----------|
| 1 | Load all sensor CSV files | Multi-file dataset |
| 2 | Merge on timestamp, forward-fill gaps <10 seconds | Handle sensor sampling jitter |
| 3 | Resample to 1-minute averages for trend clarity | 1 Hz → 1 min reduces 86,400 rows/day to 1,440 |
| 4 | Calculate derived signals: rolling mean (1 hr), rolling std (1 hr) | Health indicator baselines |
| 5 | Flag values exceeding 2σ and 3σ from rolling mean | Automated threshold detection |
| 6 | Label known fault periods from MetroPT-3 documentation | Ground truth for validation |
| 7 | Save as `data/processed/compressor_health.csv` | |

### 8.3 Azure PdM Maintenance Data

| Step | Action | Rationale |
|------|--------|-----------|
| 1 | Load telemetry, errors, maintenance, machines, failures CSVs | Multi-table dataset |
| 2 | Merge tables on machine_id and datetime | Build complete event timeline |
| 3 | Map machine models to LNG equipment categories | Compressor → Compressor Train, Pump → Centrifugal Pump, etc. |
| 4 | Calculate downtime duration from error start/end timestamps | Needed for MTTR |
| 5 | Derive failure mode from error codes | Bearing, Seal Leak, Overheating, Vibration, Electrical |
| 6 | Save as `data/processed/downtime_log.csv` and `data/processed/failure_summary.csv` | |

---

## 9. Reliability KPI Plan

### 9.1 Definitions

| KPI | Formula | Units | Data Source |
|-----|---------|-------|-------------|
| **MTTR** (Mean Time To Repair) | Σ(Repair Duration) / Number of Failures | Hours | `downtime_log.csv` |
| **MTBF** (Mean Time Between Failures — estimated) | Total Operating Time / Number of Failures | Days | `downtime_log.csv` + asset register |
| **Availability** (estimated) | MTBF / (MTBF + MTTR) | % | Derived from MTBF, MTTR |
| **Downtime Hours** | Σ(All downtime durations) | Hours | `downtime_log.csv` |
| **Failure Count** | Count of distinct failure events | Count | `failure_summary.csv` |
| **Failure Rate** | Failure Count / Total Operating Hours | Failures/1000 hrs | Derived |

### 9.2 Computation Notes

- **Total Operating Time** = Time window from first data point to last data point, minus planned shutdown periods (if identifiable). If not identifiable, estimate based on 24/7 LNG operations assumption (disclosed in assumptions doc).
- **MTBF is approximate** because public datasets do not track operating hours perfectly. This is disclosed as "MTBF-estimate."
- **Availability is approximate** for the same reason. Labeled as "Availability-estimate."
- Compute KPIs at three levels: (a) Plant-level, (b) Equipment Category, (c) Individual Asset (where data permits).

### 9.3 Industry Benchmark Context

To add credibility, include a table of typical LNG industry benchmarks (publicly sourced from
conference papers, not ExxonMobil internal):

| KPI | LNG Industry Typical Range | Source |
|-----|---------------------------|--------|
| Compressor Availability | 96–99% | GPA/GPSA Engineering Data Book |
| Overall Plant Availability | 92–98% | LNG Industry Conference Papers |
| MTTR (mechanical) | 8–48 hours | Public reliability engineering texts |
| Pipeline Incident Rate | <0.5 per 1000 km-yr | PHMSA Annual Reports |

Your computed values will differ from industry benchmarks — that's fine and expected with adapted public data. Explain the gap honestly.

---

## 10. How to Present This Honestly

This section is critical. ExxonMobil values integrity. Misrepresenting this project damages your
application more than not having it.

### 10.1 On GitHub

**README.md must state prominently (above the fold):**

> ⚠️ **Important:** This project uses publicly available industrial datasets (PHMSA, MetroPT-3, Microsoft Azure PdM) adapted into LNG-style equipment categories for portfolio demonstration purposes. It does NOT contain, use, or claim to use any ExxonMobil, PNG LNG, or other confidential operational data. All equipment names, failure events, and operating data are adapted from public sources. This project is not affiliated with or endorsed by ExxonMobil.

**In every notebook header:**

```python
# DATA SOURCE: [dataset name] — publicly available from [source URL]
# Adapted for LNG equipment context — not real LNG operational data
```

**In the data/ directory README:**

```markdown
## Data Provenance
All raw data in this directory is sourced from publicly available datasets.
See `docs/data_sources.md` for full attribution and download links.
No proprietary or confidential data is stored in this repository.
```

### 10.2 On Your CV

Place under "Projects" or "Technical Portfolio":

> **LNG Operations Technical Reliability Dashboard** | Personal Portfolio Project  
> Built a reliability analytics dashboard using Python (pandas, matplotlib) analyzing publicly available industrial datasets (PHMSA pipeline incident data, MetroPT-3 compressor monitoring data). Developed asset register mapped to LNG equipment categories, computed MTTR/MTBF/Availability KPIs, and implemented risk-based maintenance priority ranking. Used LLM-assisted engineering analysis for failure mode recommendations. Demonstrates operations technical support, reliability engineering, and process safety thinking applicable to LNG facility operations.

**Do NOT say:**
- "Analyzed PNG LNG data"
- "Built for ExxonMobil"
- "Real LNG plant data"

**DO say:**
- "Adapted public industrial datasets to LNG context"
- "Demonstrates skills applicable to LNG operations"
- "Portfolio project"

### 10.3 On LinkedIn

**Post template:**

> I built an LNG Operations Technical Reliability Dashboard as a portfolio project while my graduate application is being processed.
>
> It uses publicly available industrial datasets (PHMSA incident data + MetroPT-3 compressor data) adapted into LNG-style equipment categories. The dashboard computes reliability KPIs (MTTR, MTBF, Availability), ranks maintenance priorities, and includes AI-assisted engineering recommendations.
>
> Built with Python (pandas, matplotlib, seaborn), Jupyter notebooks, and Excel integration. Full source on GitHub.
>
> This project demonstrates the reliability engineering and operations technical thinking I'd bring to a graduate engineer role in the LNG sector.
>
> [Link to GitHub]

**Why this works:**
- Shows initiative during the waiting period
- Demonstrates relevant technical skills
- Honest about data sources
- Professional, not presumptuous

---

## 11. Risks and Limitations

### 11.1 Data Limitations

| Risk | Impact | Mitigation |
|------|--------|------------|
| MetroPT-3 is an air compressor, not a refrigerant compressor | Operating conditions differ significantly | Disclose clearly. Focus on sensor monitoring methodology, not absolute values. |
| PHMSA data is U.S.-centric, not PNG | Geographic and regulatory context differs | Disclose. Focus on incident cause patterns which are universal (corrosion, equipment failure). |
| No real LNG process data | KPIs are approximate and not calibratable to real LNG operations | Label as "estimates." Never imply these are real LNG plant metrics. |
| Small asset count (20–30) | Statistical significance limited for failure rate analysis | Disclose. Present as "illustrative asset register" not "comprehensive plant model." |

### 11.2 Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Windows Python environment issues | Can't run notebooks | Use venv + requirements.txt with pinned versions |
| Large MetroPT-3 dataset (>1 GB) | Slow processing on laptop | Resample to 1-minute in first notebook; commit only processed data |
| LLM API cost (OpenRouter) | Unexpected charges if runaway prompts | Set hard token limits; use cached responses after first run |
| GitHub repo accidentally commits large files | Repo bloat, slow clone | .gitignore for data/raw/*.csv; use Git LFS or just commit processed CSVs |

### 11.3 Professional Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Reviewer thinks data is real ExxonMobil data | Integrity concern, rejection | Prominent disclaimers everywhere |
| Project scope creep (trying to do too much) | Never finishes, no deliverable | Strict V1 scope; defer everything else to V2 roadmap |
| LLM output reads as AI-generated fluff | Hurts credibility | Review and edit all AI-generated text; label clearly |
| Poor code quality | Reflects badly on engineering rigor | Use consistent style, docstrings, type hints, comments |

---

## 12. Step-by-Step Execution Plan

This plan assumes Windows 11, Git Bash, Python 3.11, VS Code, and Hermes CLI with Codex CLI.

### Phase A: Environment Setup (Day 1)

```
# A1. Open Git Bash at project root
cd ~/projects/lng-reliability-dashboard

# A2. Initialize Git
git init
git checkout -b main

# A3. Create Python virtual environment
python -m venv venv
source venv/Scripts/activate

# A4. Create requirements.txt first, then install
pip install -r requirements.txt

# A5. Create .gitignore
```

### Phase B: Documentation (Day 1–2)

```
# B1. Write docs/project_charter.md
# B2. Write docs/data_sources.md
# B3. Write docs/assumptions_and_limitations.md
# B4. Write docs/portfolio_presentation_guide.md
# B5. Write data/README.md
```

### Phase C: Data Download & Cleaning (Day 2–3)

```
# C1. Download PHMSA data → data/raw/phmsa_incidents.csv
# C2. Download MetroPT-3 → data/raw/metropt3_sensors.csv
# C3. Download Azure PdM → data/raw/azure_pdm_maint.csv
# C4. Run notebook 01_data_cleaning.ipynb
# C5. Verify processed CSVs appear in data/processed/
```

### Phase D: Analysis (Day 3–7)

```
# D1. 02_asset_register.ipynb → asset_register.csv
# D2. 03_downtime_analysis.ipynb → charts + downtime_log.csv
# D3. 04_compressor_monitoring.ipynb → charts + compressor_health.csv
# D4. 05_pipeline_risk.ipynb → charts + pipeline_risk_scores.csv
# D5. 06_maintenance_ranking.ipynb → priority matrix chart
# D6. 07_reliability_kpis.ipynb → KPIs + charts
# D7. 08_mechanical_integrity.ipynb → inspection table
```

### Phase E: AI Integration & Export (Day 7–8)

```
# E1. 09_ai_recommendations.ipynb → LLM commentary
# E2. 10_export_excel.ipynb → Excel workbook
# E3. Capture screenshots → screenshots/
```

### Phase F: Final Polish (Day 8–9)

```
# F1. Write README.md (LAST — after all analysis done)
# F2. Write reports/reliability_summary_report.md
# F3. Add LICENSE (MIT)
# F4. Review all notebooks (clear output, restart + run all)
# F5. Final Git commit and push to GitHub
```

### Phase G: Deploy & Present (Day 9–10)

```
# G1. Push to public GitHub repo
# G2. Update CV with project entry
# G3. Post on LinkedIn
# G4. Add GitHub link to any application portal if possible
```

### Using Codex CLI (Delegation Model)

For each notebook or Python module, you (as architect) will:

1. Write the specification (what the notebook/module should do, inputs, outputs, key logic)
2. Delegate implementation to Codex CLI
3. Review Codex output — does it match spec? Is it modular?
4. Run verification — does it compile/run? Do outputs look correct?
5. Commit only after verification

Hermes will coordinate this workflow. Codex is the implementer; Hermes is the PM/Reviewer.

---

## Appendix A: LNG Equipment Category Mapping

| Public Dataset Equipment | Mapped LNG Category | LNG Subsystem |
|--------------------------|---------------------|---------------|
| MetroPT-3 Air Compressor | Propane Compressor | Refrigeration Train 1 |
| Azure PdM Machine 1 | MR Compressor | Refrigeration Train 2 |
| Azure PdM Machine 2 | Boil-Off Gas Compressor | BOG Handling |
| Azure PdM Machine 3 | Gas Turbine Generator | Power Generation |
| Azure PdM Machine 4 | Seawater Lift Pump | Cooling Water |
| Azure PdM Machine 5 | LNG Transfer Pump | LNG Storage & Loading |
| Azure PdM Machine 6 | Amine Circulation Pump | Acid Gas Removal |
| PHMSA Gas Transmission Pipe | Feed Gas Pipeline | Inlet Facilities |
| PHMSA Gas Transmission Pipe | Product Pipeline | LNG Export |
| Azure PdM Machine 7 | Air-Cooled Heat Exchanger | Propane Condenser |
| Azure PdM Machine 8 | Cryogenic Heat Exchanger | Main Cryogenic Heat Exchanger |
| Azure PdM Machine 9 | Instrument Air Compressor | Utilities |
| Azure PdM Machine 10 | Nitrogen Generator | Inert Gas System |
| (Simulated) | LNG Storage Tank | Storage & Loading |
| (Simulated) | Flare System | Relief & Blowdown |
| (Simulated) | DCS/SIS | Instrumentation & Control |

---

## Appendix B: Quick-Start Commands (Windows)

```bash
# Clone (after push)
git clone https://github.com/sam-1477/lng-operations-reliability-dashboard.git
cd lng-operations-reliability-dashboard

# Setup
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

# Run all notebooks (verify pipeline works)
jupyter nbconvert --to notebook --execute notebooks/01_data_cleaning.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_asset_register.ipynb
# ... repeat for all notebooks in order

# Generate Excel
jupyter nbconvert --to notebook --execute notebooks/10_export_excel.ipynb
```

---

*End of Architecture Plan. This document serves as the single source of truth for V1 planning.
All implementation decisions should reference this plan. Deviations must be documented in
`docs/assumptions_and_limitations.md`.*
