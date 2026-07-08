# LNG Operations Technical Reliability Dashboard

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> ⚠️ **Important:** This project uses **publicly available industrial datasets**
> (PHMSA, MetroPT-3, Microsoft Azure PdM) adapted into LNG-style equipment
> categories for **portfolio demonstration purposes**.
>
> It does **NOT** contain, use, or claim to use any ExxonMobil, PNG LNG, or
> other confidential operational data. All equipment names, failure events, and
> operating data are adapted from public sources. This project is not affiliated
> with or endorsed by ExxonMobil.

## Overview

A reliability engineering dashboard that demonstrates operations technical support
thinking — built for a graduate engineer application to the LNG sector. The project
adapts publicly available industrial datasets to an LNG equipment context, computing
reliability KPIs, analyzing condition monitoring data, assessing pipeline risk, and
generating maintenance priorities.

## What This Demonstrates

- **Asset Hierarchy Design** — 30-asset LNG-style equipment register with criticality ratings
- **Reliability KPI Computation** — MTTR, MTBF-estimate, Availability-estimate, failure rates
- **Condition Monitoring** — Compressor sensor trend analysis with threshold bands
- **Pipeline Risk Assessment** — PHMSA incident root cause and consequence analysis
- **Risk-Based Maintenance** — Likelihood consequence matrix with priority ranking
- **Mechanical Integrity** — Inspection-style status summary
- **AI-Assisted Analysis** — LLM-generated engineering recommendations with appropriate caveats
- **Professional Communication** — Excel workbook for non-Python reviewers, documented assumptions

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/lng-reliability-dashboard.git
cd lng-reliability-dashboard

# Setup virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# OR: venv\Scripts\activate   # Windows CMD

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook

# Run notebooks in order: 01 → 02 → ... → 10
```

## Data Sources

| Dataset | Source | Used For |
|---------|--------|----------|
| PHMSA Gas Transmission Incidents | U.S. DOT PHMSA (public) | Pipeline risk analysis |
| MetroPT-3 | UCI ML Repository (CC BY 4.0) | Compressor condition monitoring |
| Azure PdM | Microsoft/Kaggle (DbCL) | Maintenance records, failure analysis |

See `docs/data_sources.md` for full attribution and download instructions.

## Repository Structure

```
├── docs/               # Project charter, architecture plan, data sources
├── data/raw/           # Downloaded public datasets (not committed)
├── data/processed/     # Cleaned data files (committed)
├── notebooks/          # Jupyter analysis (01–10)
├── src/                # Python modules
├── excel/              # Master Excel workbook
├── reports/            # Generated summary reports
└── screenshots/        # Dashboard screenshots
```

## Technologies

Python 3.11 · pandas · matplotlib · seaborn · plotly · openpyxl · Jupyter · Git

## License

MIT — see [LICENSE](LICENSE)

## Author

[Your Name], B.Eng Mechanical Engineering
Papua New Guinea

[LinkedIn Profile URL]

---

*Built while my graduate application is in progress. The best time to learn reliability
engineering is before you need it on the job.*