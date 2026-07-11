# Portfolio Presentation Guide
## How to Present This Project on GitHub, CV, and LinkedIn

---

## Part 1: GitHub Repository

### README.md Structure

Your README.md is the first thing a reviewer sees. Structure it as:

```markdown
# LNG Operations Technical Reliability Dashboard
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)]
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]

## ⚠️ Important Notice
[Honesty disclaimer — prominent, above the fold]

## Overview
[2–3 sentences: what, why, who]

## What This Demonstrates
[Bullet list of engineering skills shown]

## Quick Start
[Clone, venv, pip install, run]

## Dashboard Sections
[Each section with screenshot]

## Data Sources
[Summary table with links]

## Repository Structure
[Folder tree]

## Technologies Used
[Python, pandas, matplotlib, seaborn, openpyxl, Jupyter, Excel, Power BI Desktop,
Power Query, DAX, star-schema data model, interactive drill-through,
report-page tooltips, Git]

## License
[MIT]

## Contact
Samuel Talpa, B.Eng Mechanical Engineering
GitHub: https://github.com/sam-1477/lng-operations-reliability-dashboard
```

### Repository Settings

- **Visibility:** Public
- **Topics/Tags:** `reliability-engineering` `lng` `predictive-maintenance` `pipeline-safety` `operations-technical` `portfolio-project`
- **About:** "Portfolio project: LNG-style reliability dashboard using public industrial datasets. MTTR, MTBF Estimate, Availability Estimate KPIs. Python, Jupyter, Excel, and Power BI."
- **Include in profile:** Yes (pin this repo)

### Commit History

- Clean, descriptive commit messages
- "docs: add project charter and architecture plan"
- "feat: implement asset register with LNG equipment mapping"
- "analysis: compute reliability KPIs from Azure PdM data"
- NOT "fixed stuff" or "update" or "wip"

---

## Part 2: CV Entry

### Placement

Under a section called "Technical Projects" or "Engineering Portfolio" — NOT under
"Work Experience" (it's a personal project, not employment).

### Format

```
LNG Operations Technical Reliability Dashboard          July 2026
Personal Portfolio Project | https://github.com/sam-1477/lng-operations-reliability-dashboard

* Built reliability analytics dashboard using Python (pandas, matplotlib, seaborn)
  and Power BI Desktop analyzing publicly available industrial datasets adapted
  to LNG equipment context
* Developed 30-asset register mapped to LNG equipment categories (compressors, turbines,
  pumps, pipelines, storage) with criticality ratings
* Computed reliability KPIs (MTTR, MTBF Estimate, Availability Estimate) from
  maintenance and failure records; generated a 0-100 risk-priority model and
  secondary 5x5 likelihood-consequence matrix
* Analyzed PHMSA pipeline incident data to identify root cause patterns relevant to
  LNG feed/product pipeline integrity
* Implemented risk-derived engineering recommendations with appropriate caveats,
  including engineering review and authorised work-order requirements
* Delivered Excel workbook for non-Python reviewers with embedded charts and conditional
  formatting
* Designed Power BI star-schema data model with Power Query transformations, DAX
  measures, interactive drill-through, report-page tooltips, Power BI screenshots,
  and PBIX/PBIT portfolio delivery path
```

### Tailoring for ExxonMobil PNG

The Operations Technical role description mentions:
- Process surveillance → show compressor monitoring section
- Machinery → show MetroPT-3 analysis
- Mechanical integrity → show inspection summary
- Pipelines → show PHMSA analysis
- Instrumentation and controls → mention in asset register
- Power systems → include gas turbine generator asset
- General operations support → show maintenance ranking and KPI dashboard

Map every section of your dashboard to one of these keywords in your CV bullet points.

---

## Part 3: LinkedIn Post

### When to Post

After the GitHub repo is complete with all 10 notebooks executed and the Excel workbook
generated. Ideally 1–2 weeks before any interview.

### Post Template

```
[No emoji overload — one or two max]

I built an LNG Operations Technical Reliability Dashboard while my graduate 
application is in progress.

The goal: demonstrate reliability engineering thinking using only publicly 
available industrial datasets — no confidential data, no shortcuts.

What's in it:
- 30-asset register mapped to LNG equipment categories
- Compressor condition monitoring (adapted from MetroPT-3 sensor data)
- Pipeline incident risk analysis (from PHMSA regulatory data)
- Reliability KPIs: MTTR, MTBF Estimate, Availability Estimate
- Risk-based maintenance priority matrix
- Risk-derived engineering recommendations
- Power BI report with drill-through pages and report-page tooltips
- Full Excel workbook for non-Python reviewers

Built with: Python (pandas, matplotlib, seaborn), Jupyter, openpyxl, Excel,
Power BI Desktop, Power Query, DAX

Full source and documentation on GitHub:
https://github.com/sam-1477/lng-operations-reliability-dashboard

This is a portfolio project — it uses PUBLIC datasets adapted into LNG context.
No ExxonMobil or PNG LNG data is used.

I built this because I believe a graduate engineer should show their thinking,
not just tell about it.

#ReliabilityEngineering #LNG #OperationsTechnical #Python #EngineeringPortfolio
#PNG
```

### What NOT to Do on LinkedIn

- DON'T tag ExxonMobil or PNG LNG official accounts (presumptuous)
- DON'T say "I analyzed PNG LNG data" (false)
- DON'T use ExxonMobil logo (trademark violation)
- DON'T ask for a job directly in the post (desperate)
- DON'T exaggerate ("revolutionary analysis", "groundbreaking insights")

### What TO Do

- Tag university alumni working in LNG if you know them
- Tag professors who might share
- Engage with comments professionally
- Connect your post to broader reliability engineering discussions

---

## Part 4: Interview Preparation

### The 5-Question Drill

Prepare concise (30–60 second) answers to:

1. **"Tell me about this project."**
   Start with the problem, then what you built, then what it proves.

2. **"Where did the data come from?"**
   Name all three datasets, explain why each was chosen, state clearly they're public.

3. **"How did you compute MTBF?"**
   Explain the formula, explain why it's called "MTBF Estimate" (operating hour limitation),
   explain what you'd need to make it accurate.

4. **"What would you do differently with real LNG data?"**
   Calibrate against actual operating hours, integrate with process data (DCS/PI),
   validate failure modes with SMEs, connect to CMMS work order history.

5. **"What did you learn?"**
   Reliability engineering fundamentals, industrial data cleaning challenges,
   Python data analysis, communicating technical results to non-technical audiences,
   the importance of transparent assumptions.

---

## Part 5: Screenshots for Portfolio

Capture these screenshots at high resolution (1920x1080 recommended):

1. **Dashboard Overview** — The executive summary page with KPIs
2. **Compressor Trends** — Multi-panel sensor plot with threshold bands
3. **Pipeline Risk** — PHMSA incident root cause bar chart
4. **Priority Matrix** — 5x5 risk matrix with asset labels
5. **Reliability KPI Summary** — KPI cards and equipment-category bar chart
6. **Power BI Executive Overview** — Power BI screenshot showing MTBF Estimate,
   Availability Estimate, downtime, and bad actors
7. **Engineering Recommendations** — Power BI page showing risk-derived
   recommendations and the disclaimer
8. **Asset Drill-through** — Power BI drill-through page or report-page tooltip

Save in `screenshots/` and reference in README.md as embedded images.

For portfolio delivery, include Power BI screenshots and provide either a PBIX
file, a PBIT template, or a documented external link if the PBIX is too large for
GitHub.

---

*Presentation matters as much as content. A reviewer who trusts your integrity will
trust your analysis.*
