# LNG Operations Technical Reliability Dashboard
## Power BI v0.2 — Architecture & Upgrade Plan

**Author:** [Your Name], B.Eng Mechanical Engineering  
**Target Role:** ExxonMobil PNG Graduate Engineer — Operations Technical  
**Date:** July 2026  
**Repository:** `lng-reliability-dashboard`  
**Document Version:** 1.0  

---

> **IMPORTANT:** This document describes an upgrade from a Jupyter/Excel-based v0.1
> reliability analysis (which was the "dashboard" for V1) to a **professional Power BI
> dashboard (v0.2)**. The original v0.1 project used publicly available industrial
> datasets (PHMSA, MetroPT-3, Azure PdM) adapted into LNG-style equipment categories
> for portfolio demonstration. Power BI v0.2 uses the same cleaned processed data but
> adds interactivity, drill-through, tooltips, and professional visual design.
>
> This project does NOT contain, use, or claim to use any ExxonMobil, PNG LNG, or
> other confidential operational data.

---

## Table of Contents

- [A. Current-State Assumptions](#a-current-state-assumptions)
- [B. V0.2 Page Structure](#b-v02-page-structure)
- [C. Data Model](#c-data-model)
- [D. KPI and DAX Specification](#d-kpi-and-dax-specification)
- [E. Risk and Criticality Logic](#e-risk-and-criticality-logic)
- [F. Professional Visual Design](#f-professional-visual-design)
- [G. Power Query Plan](#g-power-query-plan)
- [H. Build Sequence](#h-build-sequence)
- [I. Acceptance Criteria](#i-acceptance-criteria)
- [J. Portfolio Value](#j-portfolio-value)
- [First Action & Pre-Work Checklist](#first-action--pre-work-checklist)

---

## A. Current-State Assumptions

### A.1 What v0.1 (Jupyter + Excel) Probably Contains

The following assumptions are based on the existing architecture plan, data sources
document, and project structure. **Each assumption must be verified** by opening the
v0.1 notebook outputs and Excel workbook before starting Power BI v0.2.

| # | Assumption | Data Source | How to Verify |
|---|-----------|-------------|---------------|
| A1 | v0.1 has 20-30 assets mapped to LNG equipment categories (Compressor Trains, Gas Turbines, Centrifugal Pumps, Air-Cooled Heat Exchangers, Cryogenic Heat Exchangers, Pressure Vessels, Storage Tanks, Pipelines, Instrumentation & Control, Electrical Systems) | `notebooks/02_asset_register.ipynb` or Excel Asset Register sheet | Open the Excel workbook and check Asset Register sheet |
| A2 | v0.1 contains downtime event records with: Asset ID, Start Date, End Date, Downtime Hours, Failure Cause, Failure Mode, Consequence | `notebooks/03_downtime_analysis.ipynb` or Excel Downtime Log sheet | Check Excel Downtime Log sheet for column names |
| A3 | v0.1 computes MTTR, MTBF Estimate, and Availability Estimate at plant and category level | `notebooks/07_reliability_kpis.ipynb` or Excel Reliability KPIs sheet | Check KPI table has MTTR (hours), MTBF Estimate (days), Availability Estimate (%) |
| A4 | v0.1 has a risk matrix with Likelihood and Consequence scores per asset | `notebooks/06_maintenance_ranking.ipynb` or Excel Priority Matrix sheet | Check if scores are numeric (1-5) or categorical (Low/Medium/High) |
| A5 | v0.1 has MetroPT-3 compressor condition monitoring data with vibration, temperature, pressure, and motor current trends | `notebooks/04_compressor_monitoring.ipynb` or Excel Compressor Trends sheet | Look for time-series sensor columns |
| A6 | v0.1 has PHMSA pipeline incident data with root cause categories and consequence levels | `notebooks/05_pipeline_risk.ipynb` or Excel Pipeline Risk sheet | Check incident date, cause, consequence columns |
| A7 | v0.1 has failure mode labels (Bearing, Seal, Overheating, Vibration, Electrical) mapped from Azure PdM error codes | `notebooks/01_data_cleaning.ipynb` | Check failure_mode column in downtime log |
| A8 | v0.1 has mechanical integrity data (wall thickness, corrosion rate, remaining life, next inspection date) — these are illustrative values | `notebooks/08_mechanical_integrity.ipynb` or Excel Inspection Summary sheet | Check column names |
| A9 | v0.1 has LLM-generated engineering recommendations for top-3 failure modes | `notebooks/09_ai_recommendations.ipynb` or Excel AI Recommendations sheet | Check if recommendations are stored as text |
| A10 | v0.1 exports a single Excel workbook with 11 sheets | `notebooks/10_export_excel.ipynb` | Confirm `excel/lng_reliability_dashboard.xlsx` exists |
| A11 | v0.1 does NOT distinguish planned vs unplanned downtime | Assumptions document (A2) | Verify in downtime log |
| A12 | v0.1 assumes 24/7 continuous operation for operating hour calculation | Assumptions document (A2) | Verify in KPI computation notebook |
| A13 | v0.1 datasets have some null values, duplicate records, and inconsistent date formats that were handled in cleaning | Cleaning plan in architecture plan | Check cleaning notebooks |

### A.2 Power BI v0.2 Starting Point

- **v0.1 has cleaned, processed data files** in `data/processed/` (CSV format)
- **v0.1 has the complete asset register** as a CSV or Excel sheet
- **No existing .pbix file** — v0.2 is the first Power BI version
- **All data is flat/denormalized** — v0.2 will restructure into a star schema
- **Time-series compressor data** exists at 1-minute averages (resampled from 1 Hz)
- **The user has Power BI Desktop** (free version, November 2023 or later)

### A.3 What v0.2 Adds That v0.1 Did Not Have

| Capability | v0.1 (Jupyter/Excel) | v0.2 (Power BI) |
|-----------|---------------------|------------------|
| Interactivity | Static charts + Excel slicers | Cross-filtering, drill-through, dynamic tooltips |
| Navigation | Excel sheet tabs | Page navigation with buttons and bookmarks |
| KPI Cards | Excel cells with formulas | Dedicated KPI cards with conditional formatting |
| Drill-through | Manual sheet-switching | One-click drill-through to asset detail page |
| Tooltips | None | Custom report-page tooltips on all key visuals |
| Visual Hierarchy | Standard Excel layout | Grid-based professional layout with white space |
| Dynamic Titles | Static text | DAX-driven titles showing current filter context |
| Data Model | Flat CSV files | Star schema with relationships |
| Measures | Excel formulas | Named DAX measures with consistent formatting |
| Conditional Formatting | Excel cell coloring | Rule-based visual formatting on all report pages |
| Bookmarks | None | View switchers, show/hide panels |

---

## B. V0.2 Page Structure

The dashboard has **7 report pages** plus **2 drill-through pages** and **2 tooltip pages**.

### B.1 Page 1: Executive Reliability Overview

| Field | Specification |
|-------|---------------|
| **Purpose** | One-page plant reliability snapshot. Answers "Is our plant getting more or less reliable?" |
| **Target User** | Maintenance Manager, Operations Technical Manager, Plant Superintendent |
| **Engineering Question Answered** | "What is the current state of plant reliability, and is it improving?" |

**KPI Cards (Top Row — 4 cards):**

1. **MTBF Estimate** — Days; Red if <30, Amber 30-90, Green >90
2. **Mean Time To Repair (MTTR)** — Hours; Green if <8, Amber 8-24, Red >24
3. **Availability Estimate** — Percentage; Green if >97%, Amber 95-97%, Red <95%
4. **Total Downtime (Current Period)** — Hours; Red if increasing trend, Green if decreasing

**Visuals:**

| Visual | Type | Position | Content |
|--------|------|----------|---------|
| Monthly Downtime Trend | Line + Column clustered | Left center | Total downtime hours by month, with failure count overlay |
| Availability Estimate by Equipment Category | Bar chart (horizontal) | Right center | Sorted by availability estimate, ascending (worst first) |
| Top-5 Bad Actors | Bar chart | Bottom left | Assets with most downtime hours |
| Current Period KPI vs Previous | Multi-row card | Bottom right | MTBF Estimate, MTTR, Availability Estimate showing current, previous, % change |
| Compact P1-P4 Priority Summary | Four compact cards | Bottom right | P1-P4 counts using Measure_HighRiskAssetCount, Measure_P2AssetCount, Measure_P3AssetCount, Measure_P4AssetCount |

**Slicers:**
- Year-Month (hierarchy dropdown, default: last 12 months)
- Equipment Category (dropdown, multi-select)

**Drill-through:** None (this is the landing page)

**Tooltips:**
- "Bad Actor tooltip" — shows MTTR, failure count, risk score for hovered asset

**Navigation:** Button row at top: Overview | Equipment | Downtime | Failures | PM | Risk | Recommendations

---

### B.2 Page 2: Equipment Performance

| Field | Specification |
|-------|---------------|
| **Purpose** | Deep dive into each equipment category's reliability performance with trend context |
| **Target User** | Reliability Engineer, Mechanical Engineer, Area Maintenance Lead |
| **Engineering Question Answered** | "Which equipment categories are driving our reliability losses, and what are the specific failure patterns?" |

**KPI Cards (Top Row — 4 cards):**
1. **Failure Count (Selected Equipment)** — Count
2. **Total Downtime (Selected Equipment)** — Hours
3. **MTTR (Selected Equipment)** — Hours
4. **Availability Estimate (Selected Equipment)** — %

**Visuals:**

| Visual | Type | Position | Content |
|--------|------|----------|---------|
| Equipment Category Performance Matrix | Scatter plot (MTBF Estimate vs Availability Estimate) | Full left | Each bubble = equipment category, size = failure count |
| Failure Mode Distribution | Stacked bar (100%) | Top right | Failure mode % by equipment category |
| Monthly Failure Frequency | Line chart | Bottom right | Failures per month by category |
| Equipment Detail Table | Table | Bottom | Asset ID, Name, Category, Failure Count, Downtime, MTTR, MTBF Estimate, Availability Estimate, Risk Score |

**Slicers:**
- Equipment Category (dropdown)
- Asset ID (dropdown, dependent on category)
- Date Range (between dates)

**Drill-through:** Right-click asset → "Asset Detail" drill-through page

**Tooltips:**
- "Failure Mode tooltip" — shows failure mode breakdown for hovered category

---

### B.3 Page 3: Downtime and Bad Actors

| Field | Specification |
|-------|---------------|
| **Purpose** | Identify which assets cause the greatest operational loss and which failure modes repeat |
| **Target User** | Reliability Engineer, Maintenance Planner, Shift Supervisor |
| **Engineering Question Answered** | "Where should we focus our reliability improvement resources to achieve the greatest downtime reduction?" |

**KPI Cards (Top Row — 4 cards):**
1. **Total Downtime (All Assets)** — Hours
2. **Downtime Cost (Estimated)** — $ (uses assumed cost/hour from assumptions doc)
3. **Repeat Failure Count** — Count (assets with 3+ failures)
4. **Corrective-to-Preventive Ratio** — Ratio (C/P, portfolio demonstration threshold <1.0)

**Visuals:**

| Visual | Type | Position | Content |
|--------|------|----------|---------|
| Downtime Pareto | Pareto chart (bar + cumulative line) | Top left | Assets ranked by downtime hours, with cumulative % line |
| Bad Actor Ranking | Bar chart (horizontal) | Top right | Top-10 assets by downtime, colored by risk category |
| Failure Frequency Heatmap | Matrix/Heatmap | Bottom left | Asset (rows) x Failure Mode (columns), color intensity = count |
| Repeat Failure Trend | Line chart | Bottom right | Repeat failure count by month (assets failing 3+ times in window) |

**Slicers:**
- Equipment Category (dropdown)
- Time Period (relative: Last 3 months, 6 months, 12 months, All)
- Failure Mode (dropdown, multi-select)

**Drill-through:** Right-click asset bar → "Asset Detail" drill-through

**Tooltips:**
- "Pareto tooltip" — shows asset name, downtime hours, % of total, rank

---

### B.4 Page 4: Failure Modes and Root Causes

| Field | Specification |
|-------|---------------|
| **Purpose** | Understand what is failing, why, and whether failure patterns are changing |
| **Target User** | Reliability Engineer, Mechanical Engineer, Integrity Engineer |
| **Engineering Question Answered** | "What are the dominant failure modes, what root causes drive them, and are we seeing improvement after interventions?" |

**KPI Cards (Top Row — 4 cards):**
1. **Most Frequent Failure Mode** — Text (e.g., "Bearing — 34% of failures")
2. **Total Failure Count** — Count
3. **Mean Downtime Per Failure** — Hours
4. **Worst Month Failure Count** — Count + month label

**Visuals:**

| Visual | Type | Position | Content |
|--------|------|----------|---------|
| Failure Mode Pareto | Pareto chart | Top left | Failure modes ranked by frequency |
| Root Cause Distribution | Treemap or Pie chart | Top right | Root cause breakdown (Design, Manufacturing, Installation, Operation, Maintenance, Unknown) |
| Failure Mode by Equipment Category | Stacked bar (100%) | Middle left | How failure modes differ across equipment types |
| Failure Trend Over Time | Line chart | Middle right | Failure count by month, colored by failure mode |
| Asset Failure History Timeline | Gantt-style scatter | Bottom | Each row = asset, dots = failure events over time |

**Slicers:**
- Failure Mode (dropdown)
- Equipment Category (dropdown)
- Year-Month (hierarchy)
- Root Cause (dropdown)

**Drill-through:** Right-click failure mode → "Failure Detail" drill-through page

**Tooltips:**
- "Root cause tooltip" — distribution of root causes for hovered failure mode

---

### B.5 Page 5: PM Performance

| Field | Specification |
|-------|---------------|
| **Purpose** | Track preventive maintenance completion rates and their correlation with equipment reliability |
| **Target User** | Maintenance Planner, Supervisor, Reliability Engineer |
| **Engineering Question Answered** | "Are we doing enough PM, and is it actually reducing failures?" |

**KPI Cards (Top Row — 4 cards):**
1. **PM Compliance %** — Percentage; Green >90%, Amber 80-90%, Red <80%
2. **PMs Overdue** — Count
3. **PMs Completed This Period** — Count
4. **Corrective Actions (Same Period)** — Count

**Visuals:**

| Visual | Type | Position | Content |
|--------|------|----------|---------|
| PM Compliance by Equipment Category | Bar chart | Left | % compliance by category with illustrative project threshold line at 90% |
| PM Completion Trend | Line + Column | Top right | PMs scheduled vs completed by month |
| PM vs Corrective Correlation | Scatter plot | Bottom left | Each dot = month; x=PM compliance %, y=Corrective work count |
| Overdue PM Table | Table | Bottom right | Asset, PM Name, Due Date, Days Overdue, Responsible Team |

**Slicers:**
- Equipment Category (dropdown)
- PM Status (dropdown: On Time, Completed Late, Overdue, Upcoming)
- Date Range (between dates)

**Drill-through:** Right-click category bar → "Asset Detail" drill-through

**Tooltips:**
- "Compliance tooltip" — shows scheduled count, completed count, overdue count

**Important Engineering Note:** PM compliance is a process metric, not a reliability outcome.
High PM compliance does not guarantee reliability improvement if the PM tasks themselves
are incorrect. This page helps identify that correlation, but root-cause investigation
is always required.

---

### B.6 Page 6: Maintenance Risk and Priority

| Field | Specification |
|-------|---------------|
| **Purpose** | Visualize asset risk and prioritize maintenance actions using a Likelihood-Consequence matrix |
| **Target User** | Reliability Engineer, Maintenance Manager, Area Lead |
| **Engineering Question Answered** | "Which assets need immediate engineering attention based on failure risk and consequence?" |

**KPI Cards (Top Row — 4 cards):**
1. **High-Risk Assets (P1)** — Count (Red)
2. **Medium-High Risk Assets (P2)** — Count (Amber)
3. **Medium Risk Assets (P3)** — Count (Yellow)
4. **Low Risk Assets (P4)** — Count (Green)

**Visuals:**

| Visual | Type | Position | Content |
|--------|------|----------|---------|
| Risk Matrix (5x5) | Scatter plot with background shading | Left | Likelihood (x) vs Consequence (y). Quadrants colored Red/Amber/Yellow/Green |
| Risk Score by Equipment | Bar chart | Top right | Assets ranked by risk score |
| Risk Category Distribution | Donut chart | Middle right | % of assets in each risk band |
| Priority Recommendation Table | Table | Bottom | Asset, Risk Score, Priority Level, Suggested Action |

**Slicers:**
- Risk Category (dropdown)
- Equipment Category (dropdown)
- Asset Criticality (dropdown: A/B/C)

**Drill-through:** Right-click asset in table → "Asset Detail" drill-through

**Tooltips:**
- "Risk matrix tooltip" — shows asset name, likelihood score, consequence score, risk score
- "Priority action tooltip" — shows recommended action text

**Critical Safety Warning:** This risk matrix is an illustrative prioritization tool
based on adapted public data. It is NOT a formal safety risk assessment. It does NOT
comply with IEC 61511, ISA 84, or any site-specific risk management procedure. All
maintenance prioritization decisions must be verified by an authorised engineer
following site procedures.

---

### B.7 Page 7: Engineering Recommendations

| Field | Specification |
|-------|---------------|
| **Purpose** | Present risk-derived engineering recommendations, their evidence basis, and suggested priority |
| **Target User** | All users — visibility into what the data suggests |
| **Engineering Question Answered** | "What actions are recommended based on the data, what is the evidence for each, and which assets need attention?" |

**Important:** This page provides **risk-derived recommendations**, not a formal
action register. Every recommendation requires engineering review and a site-authorised
work order before execution.

**KPI Cards (Top Row — 4 cards):**
1. **High-Risk Assets P1** — Count (Red)
2. **Needs Review P2** — Count (Amber)
3. **Needs Monitoring P3** — Count (Yellow)
4. **Low-Risk Assets P4** — Count (Green)

**Visuals:**

| Visual | Type | Position | Content |
|--------|------|----------|---------|
| Recommendation Distribution Summary | Four compact cards or text panel | Top left | P1-P4 counts using the P1-P4 asset count measures |
| Priority Summary panel | Text/card panel | Top right | P1-P4 recommendation counts without using a measure as a categorical axis or legend |
| Engineering Interpretation panel | Card/text panel | Middle left | Data-backed interpretation of risk drivers |
| Recommended Action panel | Card/text panel | Middle right | Risk-derived action guidance and review caveat |
| Asset Recommendation Table | Table | Bottom | Asset Name, Equipment Category, Risk Score, Priority Level, Total Downtime, Repeat Failure Count, Suggested Action |

**Slicers:**
- Priority (dropdown)
- Equipment Category (dropdown)
- Asset Criticality (dropdown)

**Drill-through:** Right-click asset row → "Asset Detail" drill-through page

**Tooltips:**
- "Recommendation tooltip" — shows suggested action text

**Design note:** This page distinguishes three types of content:
1. **Operational Facts** — data-driven metrics (blue accent)
2. **Engineering Interpretation** — analysis-based conclusions (amber accent)
3. **Recommended Actions** — risk-derived suggestions (green accent)

**Required disclaimer (must be visible on page):**  
*"This is a risk-derived recommendation list. It is not a formal action register. All recommendations require engineering review and site-authorised work orders before execution."*

---

### B.8 Drill-Through Page 1: Asset Detail

| Field | Specification |
|-------|---------------|
| **Purpose** | Complete reliability profile for a single asset |
| **Triggered From** | Any asset name or bar in Pages 2, 3, 4, 5, 6 |
| **Drill-Through Fields** | Asset ID, Equipment Category |

**Visuals:**
- Page header: Asset Name + Category + Criticality badge (dynamic DAX title)
- KPI row: Failure Count, Total Downtime, MTTR, MTBF Estimate, Availability Estimate, Risk Score
- Failure history timeline (line chart)
- Downtime Pareto for sub-components (if data exists)
- PM history: Last 5 PMs with dates and results
- Risk-derived recommendations related to this asset
- Engineering notes section

**Back navigation:** Button → "Back to Report"

---

### B.9 Drill-Through Page 2: Failure Mode Detail

| Field | Specification |
|-------|---------------|
| **Purpose** | Deep dive into a specific failure mode across all assets |
| **Triggered From** | Failure mode name in Page 4 |
| **Drill-Through Fields** | Failure Mode |

**Visuals:**
- Page header: Failure Mode name
- KPI row: Total occurrences, Assets affected, Avg Downtime per occurrence
- Assets affected table with individual MTTR per asset
- Root cause distribution (pie/treemap)
- Trend over time (line chart)
- Cost impact estimate

---

### B.10 Tooltip Pages

| Tooltip | Content | Used On |
|---------|---------|---------|
| **Asset Tooltip** | Asset Name, Category, Criticality, Failure Count, MTTR, Risk Score (mini card layout, ~300x200px) | All page tables and bar charts |
| **KPI Definition Tooltip** | KPI name, formula, current value, interpretation, and project threshold assumptions | Hover over KPI card info icons |

---

## C. Data Model

### C.1 Design Philosophy

A **star schema** with two mandatory dimensions, two optional lookup dimensions,
and three fact tables: `dim_Date`, `dim_Asset`, optional `dim_FailureMode`,
optional `dim_MaintenanceAction`, `fact_Failure`, `fact_Maintenance`, and
`fact_PM_Compliance`. The separate `Measures` table is used only to organise DAX
measures. This is intentionally beginner-friendly: `EquipmentCategory` and
`CategoryGroup` remain columns in `dim_Asset`, six core relationships are
mandatory, and the two lookup relationships are conditional on the optional
lookup tables being loaded.

### C.2 Tables and Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                        DIMENSIONS                           │
│                                                             │
│  dim_Asset ──┐                                              │
│  (Asset ID)  │                                              │
│              │                                              │
│  dim_Date ───┤──→ fact_Failure ──→ dim_FailureMode          │
│  (Date)      │      (Event ID)       (Failure Mode)         │
│              │                                              │
│  dim_Asset ──┘                                              │
│                                                              │
│  dim_Asset ──→ fact_Maintenance ←── dim_Date                │
│                  (Work Order)                                │
│                                                              │
│  dim_Asset ──→ fact_PM_Compliance ←── dim_Date              │
│                  (PM Record)                                 │
└─────────────────────────────────────────────────────────────┘
```

### C.3 Table Definitions

#### C.3.1 dim_Date (Date Table)

| Column Name | Data Type | Description | Required? |
|-------------|-----------|-------------|-----------|
| Date | Date (YYYY-MM-DD) | Single day, no time component | Yes - PK |
| Year | Integer | Calendar year | Yes |
| Month | Integer | 1-12 | Yes |
| MonthName | Text | "January", "February", ... | Yes |
| Quarter | Integer | 1-4 | Yes |
| QuarterLabel | Text | "Q1", "Q2", ... | Yes |
| YearMonth | Text | "2026-07" format for sorting | Yes |
| YearMonthLabel | Text | "Jul 2026" for display | Yes |
| DayOfWeek | Integer | 1=Monday ... 7=Sunday | No |
| IsWeekend | Boolean | TRUE if Sat/Sun | No |
| MonthSort | Integer | 1-12 for correct sort order | Yes |

**Creation method:** CALENDAR() DAX function, not Power Query
**Date range:** Fixed project-bound range suitable for the current portfolio
dataset. This is not a reusable production strategy; a production model should
derive bounds from fact-table dates or use an approved wider enterprise date
range.
**Mark as Date Table:** Yes — set the Date column as the date table column

#### C.3.2 dim_Asset (Equipment Dimension)

| Column Name | Data Type | Description | PK/FK |
|-------------|-----------|-------------|-------|
| AssetID | Text | Unique asset identifier (e.g., "CMP-001") | PK |
| AssetName | Text | Friendly name (e.g., "Propane Compressor A") | |
| EquipmentCategory | Text | LNG category (Compressor Train, Gas Turbine, etc.) | |
| CategoryGroup | Text | Rotating, Static, Electrical, I&C, Piping | |
| Subsystem | Text | Production, Utility, Offsites, etc. | |
| CriticalityRating | Text | A (High), B (Medium), C (Low) | |
| Manufacturer | Text | (Illustrative) | |
| InstallDate | Date | (Illustrative) | |
| OperatingHours | Integer | Total estimated operating hours | |
| Location | Text | Unit/Area within plant | |
| CurrentStatus | Text | Operating, Standby, Under Repair, Decommissioned | |

#### C.3.3 dim_FailureMode

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| FailureModeID | Integer | Surrogate key |
| FailureMode | Text | Bearing, Seal Leak, Overheating, Vibration, Electrical, Corrosion, Erosion, Blockage, Control Failure, Other |
| FailureMechanism | Text | Fatigue, Wear, Corrosion, Overload, Contamination |
| FailureClass | Text | Mechanical, Electrical, Process, Instrument, Structural |
| TypicalRootCause | Text | Design, Manufacturing, Installation, Operation, Maintenance, Unknown |

#### C.3.4 dim_MaintenanceAction

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| ActionID | Integer | Surrogate key |
| ActionDescription | Text | What was done (Replace bearing, Realign shaft, etc.) |
| ActionType | Text | Corrective, Preventive, Predictive, Condition-Based |
| ActionCategory | Text | Mechanical, Electrical, Instrument, Lubrication, Inspection |

#### C.3.5 fact_Failure (Main Fact Table)

| Column Name | Data Type | Description | FK |
|-------------|-----------|-------------|----|
| EventID | Integer | Unique failure event ID | PK |
| AssetID | Text | Which asset failed | FK → dim_Asset[AssetID] |
| FailureDate | Date | When failure occurred | FK → dim_Date[Date] |
| FailureModeID | Integer | Type of failure | FK → dim_FailureMode[FailureModeID] |
| DowntimeStart | DateTime | When downtime began | |
| DowntimeEnd | DateTime | When asset returned to service | |
| DowntimeHours | Decimal | Total downtime (calculated) | |
| RepairHours | Decimal | Active repair time (not counting delays) | |
| FailureCause | Text | Root cause description | |
| ProductionLoss | Decimal | Estimated production loss (tons or $) | |
| RepairCost | Decimal | Estimated repair cost | |
| IsRepeatFailure | Boolean | TRUE if same asset + failure mode within 90 days | |
| FailureConsequence | Text | Low, Medium, High, Critical | |

#### C.3.6 fact_Maintenance (Work Order Fact)

| Column Name | Data Type | Description | FK |
|-------------|-----------|-------------|----|
| WorkOrderID | Integer | Unique work order ID | PK |
| AssetID | Text | Asset being maintained | FK → dim_Asset[AssetID] |
| MaintenanceDate | Date | Date of maintenance | FK → dim_Date[Date] |
| ActionID | Integer | What was done | FK → dim_MaintenanceAction[ActionID] |
| MaintenanceType | Text | Corrective, Preventive, Predictive, CBM | |
| LaborHours | Decimal | Labor hours charged | |
| PartsCost | Decimal | Cost of replacement parts | |
| TotalCost | Decimal | Labor + Parts + Contract | |
| WorkOrderStatus | Text | Completed, In Progress, Cancelled | |
| CompletionDate | Date | When work was finished | |
| PerformedBy | Text | Internal crew or contractor | |

#### C.3.7 fact_PM_Compliance (PM Record Fact)

| Column Name | Data Type | Description | FK |
|-------------|-----------|-------------|----|
| PMRecordID | Integer | Unique PM record ID | PK |
| AssetID | Text | Asset requiring PM | FK → dim_Asset[AssetID] |
| PMDueDate | Date | When PM was due | FK → dim_Date[Date] |
| PMCompletedDate | Date | When PM was actually done (nullable) | |
| PMCategory | Text | Inspection, Lubrication, Calibration, Overhaul | |
| PMFrequency | Text | Weekly, Monthly, Quarterly, Annually | |
| AssignedTeam | Text | Mech, Elec, I&C, Ops | |
| CompletionStatus | Text | "Completed" (PMCompletedDate not null), "Open" (PMCompletedDate null, PMDueDate >= today or future), "Cancelled" (explicitly marked) | |
| ScheduleStatus | Text | "On Time" (completed on or before due date), "Completed Late" (completed after due date), "Overdue" (not completed, past due date), "Upcoming" (due in future, not yet completed) | |
| DaysOverdue | Whole Number | Days overdue when ScheduleStatus = "Overdue"; null otherwise. Prefer creating in Power Query as a row-level preparation field | |

**PM Compliance Definition:** Ratio of on-time completed PMs to valid scheduled
PMs, excluding Cancelled and Upcoming records.

```dax
[Measure_PMCompliance] =
VAR ValidScheduled =
    CALCULATE(
        COUNTROWS(fact_PM_Compliance),
        fact_PM_Compliance[CompletionStatus] <> "Cancelled",
        fact_PM_Compliance[ScheduleStatus] <> "Upcoming"
    )
VAR CompletedOnTime =
    CALCULATE(
        COUNTROWS(fact_PM_Compliance),
        fact_PM_Compliance[ScheduleStatus] = "On Time"
    )
RETURN
    DIVIDE(CompletedOnTime, ValidScheduled, BLANK())
```

### C.4 Relationships Summary

Six relationships are mandatory:

| From | To | Cardinality | Cross-Filter | Active? |
|------|----|-------------|--------------|---------|
| dim_Date[Date] | fact_Failure[FailureDate] | 1:* | Single | Yes |
| dim_Asset[AssetID] | fact_Failure[AssetID] | 1:* | Single | Yes |
| dim_Date[Date] | fact_Maintenance[MaintenanceDate] | 1:* | Single | Yes |
| dim_Asset[AssetID] | fact_Maintenance[AssetID] | 1:* | Single | Yes |
| dim_Date[Date] | fact_PM_Compliance[PMDueDate] | 1:* | Single | Yes |
| dim_Asset[AssetID] | fact_PM_Compliance[AssetID] | 1:* | Single | Yes |

Two lookup relationships are conditional:

| From | To | Cardinality | Cross-Filter | Active? | Condition |
|------|----|-------------|--------------|---------|-----------|
| dim_FailureMode[FailureModeID] | fact_Failure[FailureModeID] | 1:* | Single | Yes | Only if `dim_FailureMode` is loaded |
| dim_MaintenanceAction[ActionID] | fact_Maintenance[ActionID] | 1:* | Single | Yes | Only if `dim_MaintenanceAction` is loaded |

### C.5 Calculated Columns (Required, Not Measures)

These MUST be created as calculated columns (evaluation per row):

| Column | Table | Formula | Purpose |
|--------|-------|---------|---------|
| DowntimeHours | fact_Failure | `= DATEDIFF([DowntimeStart], [DowntimeEnd], HOUR)` | Duration per event |
| RepairHours | fact_Failure | `= DATEDIFF([DowntimeStart], [DowntimeEnd], HOUR) * 0.8` (if not directly available) | Approximate active repair |
| IsRepeatFailure | fact_Failure | `= COUNTROWS(FILTER(fact_Failure, [AssetID] = EARLIER([AssetID]) && [FailureModeID] = EARLIER([FailureModeID]) && [FailureDate] < EARLIER([FailureDate]) && [FailureDate] > EARLIER([FailureDate]) - 90)) > 0` | TRUE if same failure in 90 days |
| YearMonth | dim_Date | `= FORMAT([Date], "YYYY-MM")` | Sortable period field |
| YearMonthLabel | dim_Date | `= FORMAT([Date], "mmm YYYY")` | Display period field |

### C.6 What Should Be a Measure (Not a Column)

These must be measures because they must respond to slicer/filter context:

- Total Downtime Hours
- Failure Count
- MTTR, MTBF Estimate, Availability Estimate
- All KPI calculations
- Risk Score
- Percentage Change
- Previous Period comparisons
- Ranks (RANKX)

---

## D. KPI and DAX Specification

### D.1 DAX Conventions

- All measures use **consistent naming**: `Measure_[Name]`
- Use `CALCULATE` with explicit filter arguments (not implicit)
- All percentage measures return a decimal (0.95 not 95) — format in the visual
- Use `VAR` / `RETURN` pattern for readability
- Add measure descriptions (viewable in Power BI Model view)

### D.2 Measure Definitions

---

**M1: Measure_TotalDowntimeHours**

| Field | Value |
|-------|-------|
| **Business Definition** | Sum of all unplanned downtime hours across all failure events in the current filter context |
| **Units** | Hours |
| **DAX** | `Measure_TotalDowntimeHours = SUM(fact_Failure[DowntimeHours])` |
| **Required Columns** | fact_Failure[DowntimeHours] (must exist as a column) |
| **Interpretation** | Higher = worse plant performance. Compare period-over-period |
| **Warning** | This should be unplanned downtime only. If planned and unplanned are mixed, this will overstate reliability losses |

---

**M2: Measure_FailureCount**

| Field | Value |
|-------|-------|
| **Business Definition** | Count of distinct failure events in the current filter context |
| **Units** | Count |
| **DAX** | `Measure_FailureCount = COUNTROWS(fact_Failure)` |
| **Required Columns** | fact_Failure[EventID] |
| **Interpretation** | Total number of failures. Compare to previous period — decreasing = improving |
| **Warning** | Counts ALL failures equally. A 1-hour bearing failure and a 7-day turbine overhaul both count as 1 |

---

**M3: Measure_TotalRepairHours**

| Field | Value |
|-------|-------|
| **Business Definition** | Sum of active repair hours (time actually spent working, not waiting-for-parts time) |
| **Units** | Hours |
| **DAX** | `Measure_TotalRepairHours = SUM(fact_Failure[RepairHours])` |
| **Required Columns** | fact_Failure[RepairHours] |
| **Interpretation** | Direct maintenance labor time. Higher = more intensive repairs needed |
| **Warning** | May be estimated as 80% of total downtime if direct repair hours are not tracked |

---

**M4: Measure_AvgRepairTime**

| Field | Value |
|-------|-------|
| **Business Definition** | Average repair hours per failure event |
| **Units** | Hours |
| **DAX** | `Measure_AvgRepairTime = DIVIDE([Measure_TotalRepairHours], [Measure_FailureCount], BLANK())` |
| **Required Columns** | fact_Failure[RepairHours], fact_Failure[EventID] |
| **Interpretation** | Trend: decreasing means more efficient repairs or simpler failures. Increasing means failures are getting harder to fix |
| **Warning** | DIVIDE handles division-by-zero. Returns BLANK() if no failures exist because the ratio is unavailable, not zero |

---

**M5: Measure_MTTR**

| Field | Value |
|-------|-------|
| **Business Definition** | Mean Time To Repair — average active repair time per failure. Industry-standard reliability metric |
| **Units** | Hours |
| **DAX** | `Measure_MTTR = [Measure_AvgRepairTime]` |
| **Required Columns** | Same as M4 |
| **Interpretation** | Lower = better. Any MTTR threshold used here is an illustrative project threshold that requires site validation |
| **Warning** | MTTR should ideally exclude logistics/waiting time. If your data only has total downtime, MTTR will be overstated. Label clearly |

---

**M6: Measure_MTBF_Estimate**

| Field | Value |
|-------|-------|
| **Business Definition** | Mean Time Between Failures estimate — estimated operating days divided by number of failures |
| **Units** | Days |
| **DAX** | ```dax
[Measure_MTBF_Estimate] =
VAR SelectedAssetCount =
    CALCULATE(
        DISTINCTCOUNT(dim_Asset[AssetID]),
        ALLSELECTED(dim_Asset[AssetID])
    )
VAR ObservationStart =
    MIN(dim_Date[Date])
VAR ObservationEnd =
    MAX(dim_Date[Date])
VAR ObservationDays =
    DATEDIFF(ObservationStart, ObservationEnd + 1, DAY)
VAR EstimatedOperatingDays =
    ObservationDays * SelectedAssetCount * 0.95
RETURN
    DIVIDE(
        EstimatedOperatingDays,
        [Measure_FailureCount],
        BLANK()
    )
```
| **Required Columns** | dim_Date[Date], fact_Failure[FailureDate], fact_Failure[EventID], dim_Asset[AssetID] |
| **Interpretation** | Higher = better. This is an **MTBF Estimate** based on selected assets and the selected observation period |
| **Warning** | This is an estimate. It assumes selected assets were available for the full observation period, and the 0.95 factor is an assumption. True MTBF requires actual operating hours and confirmed failure-event definitions. Always label as "MTBF Estimate" |

---

**M7: Measure_Availability_Estimate**

| Field | Value |
|-------|-------|
| **Business Definition** | Operational availability — proportion of total time the equipment was available for service. Estimated from MTBF and MTTR |
| **Units** | Decimal (0-1), format as % in visual |
| **DAX** | ```dax
[Measure_Availability_Estimate] =
VAR MTBF_Days = [Measure_MTBF_Estimate]
VAR MTTR_Days = DIVIDE([Measure_MTTR], 24, BLANK())
RETURN
    DIVIDE(
        MTBF_Days,
        MTBF_Days + MTTR_Days,
        BLANK()
    )
``` |
| **Required Columns** | Same as M5, M6 |
| **Interpretation** | Higher = better. Any availability threshold used in visuals is an illustrative project threshold that requires site validation |
| **Warning** | This is an Availability Estimate. True availability requires accurate planned vs unplanned downtime and actual operating-hour data. See assumptions and limitations document |

---

**M8: Measure_PMCompliance**

| Field | Value |
|-------|-------|
| **Business Definition** | Percentage of scheduled preventive maintenance tasks completed on or before their due date |
| **Units** | Decimal (0-1), format as % |
| **DAX** | ```dax
[Measure_PMCompliance] =
VAR ValidScheduled =
    CALCULATE(
        COUNTROWS(fact_PM_Compliance),
        fact_PM_Compliance[CompletionStatus] <> "Cancelled",
        fact_PM_Compliance[ScheduleStatus] <> "Upcoming"
    )
VAR CompletedOnTime =
    CALCULATE(
        COUNTROWS(fact_PM_Compliance),
        fact_PM_Compliance[ScheduleStatus] = "On Time"
    )
RETURN
    DIVIDE(CompletedOnTime, ValidScheduled, BLANK())
``` |
| **Required Columns** | fact_PM_Compliance[PMRecordID], fact_PM_Compliance[CompletionStatus], fact_PM_Compliance[ScheduleStatus] |
| **Interpretation** | Higher = better. The 90%/80% thresholds are portfolio demonstration thresholds requiring site validation |
| **Warning** | High PM compliance does not guarantee reliability. Poor PM content will not prevent failures regardless of completion rates |

---

**M9: Measure_RepeatFailureCount**

| Field | Value |
|-------|-------|
| **Business Definition** | Count of failure events where the same asset failed with the same failure mode within 90 days of a previous identical failure |
| **Units** | Count |
| **DAX** | ```dax
Measure_RepeatFailureCount =
CALCULATE(
    COUNTROWS(fact_Failure),
    fact_Failure[IsRepeatFailure] = TRUE
)
``` |
| **Required Columns** | fact_Failure[IsRepeatFailure] (calculated column — see C.5) |
| **Interpretation** | High repeat failure count = poor root cause analysis or ineffective repairs. Each repeat failure signals that corrective actions did not address the true root cause |
| **Warning** | The 90-day window is a threshold assumption. Some failure modes naturally recur beyond 90 days. This measure flags the worst offenders within a reasonable investigation window |

---

**M10: Measure_CorrectiveToPreventiveRatio**

| Field | Value |
|-------|-------|
| **Business Definition** | Ratio of corrective maintenance actions to preventive maintenance actions in the current period |
| **Units** | Ratio (pure number) |
| **DAX** | ```dax
Measure_CorrectiveToPreventiveRatio =
VAR CorrectiveCount =
    CALCULATE(
        COUNTROWS(fact_Maintenance),
        fact_Maintenance[MaintenanceType] = "Corrective"
    )
VAR PreventiveCount =
    CALCULATE(
        COUNTROWS(fact_Maintenance),
        fact_Maintenance[MaintenanceType] = "Preventive"
    )
RETURN
    DIVIDE(CorrectiveCount, PreventiveCount, BLANK())
``` |
| **Required Columns** | fact_Maintenance[WorkOrderID], fact_Maintenance[MaintenanceType] |
| **Interpretation** | Target < 1.0 (more preventive than corrective). Ratio > 1.5 signals reactive maintenance culture. Trending down = improving |
| **Warning** | Some maintenance defies simple C/P classification (condition-based, predictive). If your data has more than two categories, adjust the CALCULATE filters accordingly |

---

**M11: Measure_MaintenanceCost**

| Field | Value |
|-------|-------|
| **Business Definition** | Total cost of all maintenance activities (labor + parts + contracts) in the current filter context |
| **Units** | Dollars ($) |
| **DAX** | `Measure_MaintenanceCost = SUM(fact_Maintenance[TotalCost])` |
| **Required Columns** | fact_Maintenance[TotalCost] |
| **Interpretation** | Higher = more maintenance spend. Use with failure count to assess cost-effectiveness. Decreasing cost with stable failure count = good cost control |
| **Warning** | Cost data from public datasets is illustrative. If your dataset lacks cost fields, use estimated values and CLEARLY label them. This measure is meaningless without context (fleet size, industry) |

---

**M12: Measure_CostPerDowntimeHour**

| Field | Value |
|-------|-------|
| **Business Definition** | Total maintenance cost divided by total downtime hours — a measure of cost-effectiveness of downtime |
| **Units** | $/hour |
| **DAX** | `Measure_CostPerDowntimeHour = DIVIDE([Measure_MaintenanceCost], [Measure_TotalDowntimeHours], BLANK())` |
| **Required Columns** | fact_Maintenance[TotalCost], fact_Failure[DowntimeHours] |
| **Interpretation** | Lower = more cost-effective downtime management. Very high values may indicate expensive repairs on low-downtime assets (worth investigating) |
| **Warning** | This is an EFFICIENCY metric, not a cost metric. A single catastrophic failure will produce a low $/hour (high downtime, high cost) — this does NOT mean it was cheap |

---

**M13: P1-P4 Asset Count Measures**

| Field | Value |
|-------|-------|
| **Business Definition** | Count of assets in each 0-100 risk-priority band (see Section E) |
| **Units** | Count |
| **DAX** | ```dax
[Measure_HighRiskAssetCount] =
COUNTROWS(
    FILTER(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_RiskScore]) >= 60
    )
)

[Measure_P2AssetCount] =
COUNTROWS(
    FILTER(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_RiskScore]) >= 40 &&
        CALCULATE([Measure_RiskScore]) < 60
    )
)

[Measure_P3AssetCount] =
COUNTROWS(
    FILTER(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_RiskScore]) >= 20 &&
        CALCULATE([Measure_RiskScore]) < 40
    )
)

[Measure_P4AssetCount] =
COUNTROWS(
    FILTER(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_RiskScore]) >= 0 &&
        CALCULATE([Measure_RiskScore]) < 20
    )
)
``` |
| **Required Columns** | dim_Asset[AssetID], [Measure_RiskScore] |
| **Interpretation** | Number of assets in each risk-derived priority band. Decreasing P1/P2 trend suggests risk reduction, subject to engineering review |
| **Warning** | Thresholds are engineering assumptions based on the 0-100 scale. Site-specific risk criteria may differ. This is NOT a safety risk assessment — see Section E |

---

**M14: Measure_BadActorRanking**

| Field | Value |
|-------|-------|
| **Business Definition** | Ranking of assets by a weighted combination of downtime, failure frequency, and repair cost |
| **Units** | Rank (1 = worst actor) |
| **DAX** | ```dax
[Measure_BadActorRanking] =
RANKX(
    ALLSELECTED(dim_Asset[AssetID]),
    [Measure_BadActorScore],
    ,
    DESC,
    DENSE
)
``` |

**Supporting measure — this must be created first:**

```dax
[Measure_BadActorScore] =
VAR MaxDowntime =
    MAXX(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_TotalDowntimeHours])
    )
VAR MaxFrequency =
    MAXX(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_FailureCount])
    )
VAR MaxCost =
    MAXX(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_MaintenanceCost])
    )
VAR DowntimeScore =
    DIVIDE([Measure_TotalDowntimeHours], MaxDowntime, BLANK()) * 40
VAR FrequencyScore =
    DIVIDE([Measure_FailureCount], MaxFrequency, BLANK()) * 35
VAR CostScore =
    DIVIDE([Measure_MaintenanceCost], MaxCost, BLANK()) * 25
RETURN
    DowntimeScore + FrequencyScore + CostScore
```

**Weights:** Downtime = 40%, Failure Frequency = 35%, Repair Cost = 25%
**Interpretation:** Bad Actor Rank #1 is the asset causing the greatest overall operational impact
**Warning:** The weighting is an engineering assumption. Review with site reliability team to adjust for local priorities
**Note:** BLANK() is returned for assets with no failures or no costs, preventing them from distorting the ranking.
---

**M15: Measure_PreviousPeriodComparison**

| Field | Value |
|-------|-------|
| **Business Definition** | Computes the selected measure's value for the previous equivalent period (previous month, previous quarter, etc.) |
| **Units** | Same as source measure |
| **DAX** | ```dax
Measure_PreviousPeriodDowntime =
CALCULATE(
    [Measure_TotalDowntimeHours],
    PREVIOUSMONTH(dim_Date[Date])
)
``` |

**Template pattern for any metric:**
```dax
Measure_PreviousPeriod =
VAR CurrentMeasure = [Measure_TotalDowntimeHours]  -- Replace with any metric
VAR PriorPeriod =
    CALCULATE(
        [Measure_TotalDowntimeHours],
        DATEADD(dim_Date[Date], -1, MONTH)  -- Adjust: -1 MONTH, -1 QUARTER, -1 YEAR
    )
RETURN
    PriorPeriod
```

| **Required Columns** | dim_Date[Date] (marked as date table) |
| **Interpretation** | Positive = metric increased = worse for downtime/cost, better for availability |
| **Warning** | DATEADD requires a contiguous date table. Gaps in dates may produce unexpected results. PREVIOUSMONTH works best at month granularity |

---

**M16: Measure_PercentageChange**

| Field | Value |
|-------|-------|
| **Business Definition** | Percentage change of a metric compared to the previous equivalent period |
| **Units** | % (decimal, format as % in visual) |
| **DAX** | ```dax
Measure_DowntimeChange =
VAR CurrentValue = [Measure_TotalDowntimeHours]
VAR PriorValue = [Measure_PreviousPeriodDowntime]
RETURN
    DIVIDE(CurrentValue - PriorValue, PriorValue, BLANK())
``` |

**Alternative with arrow indicator:**
```dax
Measure_DowntimeChange_WithDirection =
VAR CurrentValue = [Measure_TotalDowntimeHours]
VAR PriorValue = [Measure_PreviousPeriodDowntime]
VAR ChangePct = DIVIDE(CurrentValue - PriorValue, PriorValue, BLANK())
VAR Direction = IF(ChangePct > 0, " ▲ ", IF(ChangePct < 0, " ▼ ", " → "))
RETURN
    Direction & FORMAT(ABS(ChangePct), "0.0%")
```

| **Required Columns** | dim_Date[Date], and the metric being compared |
| **Interpretation** | For downtime: positive % = more downtime = worse. For availability: positive % = improvement |
| **Warning** | Percentage change is misleading when prior period is zero or very small. Use DIVIDE to handle division by zero. The direction interpretation REVERSES for "good = high" metrics (availability) vs "good = low" metrics (downtime) |

---

### D.3 Additional Supporting Measures

**Measure_TotalOperatingDays (used by MTBF):**
```dax
Measure_TotalOperatingDays =
VAR MinDate = MIN(fact_Failure[FailureDate])
VAR MaxDate = MAX(fact_Failure[FailureDate])
RETURN
    CALCULATE(
        COUNTROWS(dim_Date),
        DATESBETWEEN(dim_Date[Date], MinDate, MaxDate)
    ) * 0.95  -- Assumption: 95% of calendar days = operating days
```

**Measure_YearToDateDowntime:**
```dax
Measure_YearToDateDowntime =
TOTALYTD(
    [Measure_TotalDowntimeHours],
    dim_Date[Date]
)
```

**Measure_Rolling12MonthAvail (for trend):**
```dax
Measure_Rolling12MonthAvail =
CALCULATE(
    [Measure_Availability_Estimate],
    DATESINPERIOD(dim_Date[Date], MAX(dim_Date[Date]), -12, MONTH)
)
```

---

## E. Risk and Criticality Logic

### E.1 Design Principles

1. **Transparent** — the score formula is published, not a black box
2. **Multi-factor** — combines downtime, frequency, consequence, and cost
3. **Auditable** — every component can be inspected individually
4. **Non-safety-critical** — explicitly NOT a safety risk assessment
5. **Adjustable** — weights can be changed as the user learns

### E.2 Risk Score Formula

The risk score uses a **0–100 scale**. Each component is normalised to a 0–100
sub-score, then weighted. The formula:

```dax
Measure_RiskScore =
VAR DT_Score =
    DIVIDE([Measure_TotalDowntimeHours],
        MAXX(ALLSELECTED(dim_Asset[AssetID]), CALCULATE([Measure_TotalDowntimeHours])), BLANK()) * 30
VAR Freq_Score =
    DIVIDE([Measure_FailureCount],
        MAXX(ALLSELECTED(dim_Asset[AssetID]), CALCULATE([Measure_FailureCount])), BLANK()) * 25
VAR Cost_Score =
    DIVIDE([Measure_MaintenanceCost],
        MAXX(ALLSELECTED(dim_Asset[AssetID]), CALCULATE([Measure_MaintenanceCost])), BLANK()) * 15
VAR Cons_Score = [Measure_ConsequenceScore] * 2  -- Scale consequence points to 0-20, Weight: 20%
VAR Repeat_Score = IF([Measure_RepeatFailureCount] > 0, 10, 0) -- Weight: 10%
RETURN
    DT_Score + Freq_Score + Cost_Score + Cons_Score + Repeat_Score
```

Each sub-score contributes a maximum of its weight (30 + 25 + 15 + 20 + 10 = 100).

### E.3 Risk Categories (0–100 Scale)

Primary risk thresholds:
- P1: 60-100
- P2: 40-59.99
- P3: 20-39.99
- P4: 0-19.99

| Risk Score Range | Category | Color | Priority Level |
|-----------------|----------|-------|----------------|
| 0 – 19.99 | Low | Green | P4 — Routine |
| 20 – 39.99 | Medium | Yellow | P3 — Scheduled |
| 40 – 59.99 | Medium-High | Amber | P2 — High Priority |
| 60 – 100 | High | Red | P1 — Immediate Action |

### E.4 Risk Score DAX Measure

```dax
Measure_ConsequenceScore =
VAR HasSafetyConsequence =
    CALCULATE(
        COUNTROWS(fact_Failure),
        fact_Failure[FailureConsequence] IN {"High", "Critical"}
    )
VAR HasProductionConsequence =
    CALCULATE(
        COUNTROWS(fact_Failure),
        fact_Failure[FailureConsequence] = "Medium"
    )
RETURN
    IF(HasSafetyConsequence > 0, 10,
       IF(HasProductionConsequence > 0, 7,
          IF(CALCULATE(COUNTROWS(fact_Failure)) > 0, 3, 0)
       )
    )
```

### E.5 Likelihood-Consequence Matrix (For Page 6 Visual)

**Note:** The 5x5 matrix below produces a 1-25 matrix score for a visual
likelihood-consequence heatmap. It is a secondary visual aid, not the primary
ranking measure. The primary asset ranking and priority thresholds must use the
0-100 risk score defined in E.2 and E.3.

**Likelihood Categories (based on failure frequency):**

| Frequency (failures/year) | Likelihood Rating | Score |
|--------------------------|-------------------|-------|
| > 6 per year | Almost Certain | 5 |
| 3 – 6 per year | Likely | 4 |
| 1 – 3 per year | Possible | 3 |
| 1 per 1–3 years | Unlikely | 2 |
| < 1 per 3 years | Rare | 1 |

**Consequence Categories:**

| Criteria | Consequence Rating | Score |
|----------|-------------------|-------|
| Safety incident + >7 days downtime | Catastrophic | 5 |
| >7 days downtime or major production loss | Major | 4 |
| 2–7 days downtime | Moderate | 3 |
| < 2 days downtime | Minor | 2 |
| No production impact | Insignificant | 1 |

**5×5 Matrix Scoring:**

The P1-P4 labels inside this matrix are visual cues only. They must not override
the primary 0-100 risk ranking measure.

| | Rare (1) | Unlikely (2) | Possible (3) | Likely (4) | Almost Certain (5) |
|--|----------|--------------|--------------|------------|-------------------|
| **Catastrophic (5)** | 5 (P2) | 10 (P1) | 15 (P1) | 20 (P1) | 25 (P1) |
| **Major (4)** | 4 (P3) | 8 (P2) | 12 (P1) | 16 (P1) | 20 (P1) |
| **Moderate (3)** | 3 (P4) | 6 (P3) | 9 (P2) | 12 (P1) | 15 (P1) |
| **Minor (2)** | 2 (P4) | 4 (P3) | 6 (P3) | 8 (P2) | 10 (P1) |
| **Insignificant (1)** | 1 (P4) | 2 (P4) | 3 (P4) | 4 (P3) | 5 (P2) |

| **Priority Interpretation (maps to 0–100 risk score):**

| Priority | Risk Score Range | Action Required | Color |
|----------|-----------------|----------------|-------|
| P1 — Immediate Action | 60 – 100 | Engineering review within 1 week, management report | Red (#ef4444) |
| P2 — High Priority | 40 – 59.99 | Schedule within 1 month, include in reliability review | Amber (#f59e0b) |
| P3 — Scheduled | 20 – 39.99 | Add to maintenance plan, monitor quarterly | Yellow (#eab308) |
| P4 — Routine | 0 – 19.99 | Continue current PM, review annually | Green (#10b981) |

### E.7 Conditional Formatting Rules

These thresholds are illustrative project thresholds for portfolio demonstration
and require site validation before operational use.

| Element | Condition | Color | Font/Background |
|---------|-----------|-------|-----------------|
| Risk Score value (card) | >= 60 | White on Red | Bold, background = #ef4444 |
| Risk Score value (card) | 40 – 59.99 | Black on Amber | Bold, background = #f59e0b |
| Risk Score value (card) | 20 – 39.99 | Black on Yellow | Bold, background = #eab308 |
| Risk Score value (card) | < 20 | Black on Green | Bold, background = #10b981 |
| Table row (Priority) | P1 | White on #ef4444 | Entire row |
| Table row (Priority) | P2 | Black on #f59e0b | Entire row |
| Table row (Priority) | P3 | Black on #eab308 | Entire row |
| Table row (Priority) | P4 | Black on #10b981 | Entire row |
| KPI trend arrow | Increase in good metric | Green (#10b981) | ▲ |
| KPI trend arrow | Decrease in good metric | Red (#ef4444) | ▼ |
| Availability Estimate bar | >= 97% | #10b981 | Bar fill |
| Availability Estimate bar | 95-97% | #f59e0b | Bar fill |
| Availability Estimate bar | < 95% | #ef4444 | Bar fill |
| PM Compliance bar | >= 90% | #10b981 | Bar fill |
| PM Compliance bar | 80-90% | #f59e0b | Bar fill |
| PM Compliance bar | < 80% | #ef4444 | Bar fill |

### E.8 Critical Warnings (Must Be Displayed on Dashboard)

1. **"This risk matrix is an ILLUSTRATIVE prioritization tool. It is NOT a formal safety
   risk assessment. Do not use for safety-critical decisions without authorised
   engineering review."**
2. **"Risk scores combine multiple factors with assumed weightings. Adjust weights
   based on site-specific priorities."**
3. **"All maintenance priority decisions must follow site procedures and be approved
   by an authorised engineer."**
4. **"Bad actor identification is based on historical data. A high-risk score does not
   predict the next failure — it flags assets that need investigation."**

---

## F. Professional Visual Design

### F.1 Page Dimensions

| Setting | Value | Rationale |
|---------|-------|-----------|
| Page type | Default | Standard Power BI page |
| Width | 1280 px (16:9) | Standard widescreen, fits most laptop screens |
| Height | 720 px | Matches 16:9, no scrolling needed if well laid out |
| Page background | #FAFAFA (near-white) | Professional, reduces visual fatigue |
| Wallpaper | None — use clean canvas | Avoids decorative backgrounds that distract from data |

### F.2 Grid and Spacing System

| Element | Value |
|---------|-------|
| Grid snap | ON (to 1px grid) |
| Page margin | 16px all sides |
| Card spacing | 8px between elements |
| Section padding | 16px within grouped elements |
| Alignment | All charts in same row have matching heights |
| Width unit | Use thirds (33% / 33% / 33%) or halves (50% / 50%) for visual balance |

### F.3 Typography Hierarchy

| Level | Font | Size | Weight | Color | Usage |
|-------|------|------|--------|-------|-------|
| Page Title | Segoe UI (or DIN Pro if available) | 18pt | Bold | #1A1A2E | Top-left page name |
| Section Heading | Segoe UI | 12pt | Semibold | #333333 | Above each visual group |
| KPI Value | Segoe UI | 28pt | Bold | #1A1A2E | Card main number |
| KPI Label | Segoe UI | 10pt | Regular | #666666 | Below KPI value |
| KPI Subtitle | Segoe UI | 9pt | Regular | #999999 | Period or comparison text |
| Visual Title | Segoe UI | 11pt | Semibold | #333333 | Above each chart |
| Axis Labels | Segoe UI | 9pt | Regular | #666666 | Chart axes |
| Data Labels | Segoe UI | 9pt | Regular | #666666 | On-chart values |
| Table Text | Segoe UI | 10pt | Regular | #333333 | Table cell content |
| Slicer Title | Segoe UI | 10pt | Semibold | #333333 | Above each slicer |
| Footer/Disclaimer | Segoe UI | 8pt | Regular Italic | #999999 | Bottom of page |

### F.4 Card Structure (KPI Cards)

```
┌──────────────────────────────────┐
│  KPI Label (10pt, #666)         │
│  VALUE (28pt, Bold, #1A1A2E)   │
│  ▲ 12.3% vs prev period        │
│  Units / Period (9pt, #999)     │
└──────────────────────────────────┘
```

- Card background: White (#FFFFFF)
- Card border: None — use subtle shadow effect
- Card corner radius: 4px
- Card width: ~200px (4 per row fits 1280px page)
- Card height: ~100px
- Icon: Optional small icon left of KPI label (use Power BI icons)

### F.5 Heading Structure

| Element | Example |
|---------|---------|
| Page Title | "Executive Reliability Overview" |
| Section | "KEY PERFORMANCE INDICATORS" (uppercase, smaller) |
| Visual Title | "Monthly Downtime Trend — Last 12 Months" |
| Visual Subtitle | "Includes all unplanned downtime events" |

### F.6 Colour Usage by Meaning

| Color | Hex | Usage |
|-------|-----|-------|
| Primary (Dark Navy) | #1A1A2E | Page titles, headers, KPI values |
| Secondary (Steel Blue) | #3B82F6 | Default chart series, bars, lines |
| Success (Green) | #10B981 | Good: High availability, on-time PM, low MTTR |
| Warning (Amber) | #F59E0B | Caution: Medium risk, borderline KPI |
| Danger (Red) | #EF4444 | Action needed: P1 risk, overdue, high downtime |
| Info (Blue) | #0EA5E9 | Informational: neutral categories |
| Background (Off-white) | #FAFAFA | Page background |
| Card Background | #FFFFFF | White cards for KPI values |
| Grid Lines | #E5E7EB | Subtle chart grid |
| Text Dark | #1A1A2E | Titles, main values |
| Text Medium | #666666 | Labels, axis text |
| Text Light | #999999 | Subtitles, disclaimers, footnotes |

**Color rules:**
- NEVER use red/green together for accessibility without also using text labels
- NEVER use pure black (#000000) — it creates excessive contrast
- NEVER use more than 4 distinct series colors on one chart
- ALWAYS use a color legend for stacked/combo charts
- ALWAYS verify red-green combinations are distinguishable in grayscale

### F.7 Chart Title Conventions

| Convention | Example |
|------------|---------|
| Title = {Metric} by {Dimension} — {Time Period} | "Downtime by Equipment Category — Last 12 Months" |
| Subtitle = {Data source note} | "Source: Azure PdM failure events" |
| Dynamic title uses DAX: | `= "Failure Count by Asset — " & SELECTEDVALUE(dim_Date[YearMonthLabel], "All Periods")` |
| No titles on tables | Tables use a section heading above |
| Consistent phrase structure | "Verb + Noun by Dimension" |

### F.8 Dynamic Subtitles (DAX)

```dax
Measure_DynamicTitle_EquipmentPage =
VAR SelectedCategory = SELECTEDVALUE(dim_Asset[EquipmentCategory], "All Equipment")
VAR SelectedAsset = SELECTEDVALUE(dim_Asset[AssetName], "")
VAR Period = SELECTEDVALUE(dim_Date[YearMonthLabel], "All Periods")
RETURN
    SelectedAsset & " — " & SelectedCategory & " | " & Period
```

Use this as the dynamic title for the Equipment Performance page.

### F.9 Data Labels

| Chart Type | Data Labels | Position | Format |
|------------|-------------|----------|--------|
| KPI Card | Always | Center of card | Large, bold |
| Bar/Column chart | On bars (end) | Outside end | "123 hrs" |
| Line chart | On last data point only | Top | Bold last value |
| Pareto chart | On bars + cumulative line | Bar: inside, Line: above | "% of total" |
| Pie/Donut | Inside, category + % | Inside | "Bearing, 34%" |
| Table | Not needed — displayed as text | N/A | N/A |
| Scatter plot | Hover tooltip only | N/A | N/A |

### F.10 Background and Border Treatment

| Element | Treatment |
|---------|-----------|
| Page background | #FAFAFA, no image |
| Visual background | Transparent (inherits page) |
| Visual border | None (clean modern look) |
| Visual shadow | Light (Power BI visual effects > Shadow preset) |
| KPI card background | White (#FFFFFF) |
| KPI card shadow | Light, 4px offset |
| Table grid | Subtle horizontal lines only (#E5E7EB) |
| Table header | #1A1A2E background, white text |
| Section divider | 1px line, #E5E7EB |

---

## G. Power Query Plan

### G.1 Folder Structure in Power BI

After loading, name your queries as follows:

```
Queries [4 folders]:
  ├── Parameters/
  │   ├── pv_DataPath         -- Text, path to processed data folder
  │   └── pv_CurrentDate      -- Date, default = DateTime.Date(DateTime.LocalNow())
  │
  ├── Dimensions/
  │   ├── dim_Date             -- Created in DAX, NOT Power Query
  │   ├── dim_Asset            -- From asset_register.csv
  │   ├── dim_FailureMode      -- From failure mode CSV
  │   └── dim_MaintenanceAction-- From action lookup CSV
  │
  ├── Facts/
  │   ├── fact_Failure          -- From downtime_log.csv
  │   ├── fact_Maintenance      -- From maintenance records.csv
  │   └── fact_PM_Compliance    -- From PM schedule.csv
  │
  └── Reference/
      └── ref_DataQualityLog    -- Transformation log for audit trail
```

### G.2 Transformation Steps by Query

---

**dim_Asset — Transformation Steps:**

| # | Step | M Code (conceptual) | Rationale |
|---|------|--------------------|-----------|
| 1 | Source | `Csv.Document(File.Contents(DataPath & "/asset_register.csv"))` | Load CSV |
| 2 | Promote Headers | `Table.PromoteHeaders` | First row = column names |
| 3 | Change Type | `Table.TransformColumnTypes` | AssetID=Text, AssetName=Text, etc. |
| 4 | Replace Nulls (CriticalityRating) | `Table.ReplaceValue(null, "C", Replacer.ReplaceValue, {"CriticalityRating"})` | Default to C if unrated |
| 5 | Trim Whitespace | `Table.TransformColumns(..., Text.Trim)` | Remove leading/trailing spaces |
| 6 | Add Data Quality Flag | Custom column: if AssetID is null or AssetName is null → "Suspect" | Track invalid records |
| 7 | Remove Duplicates | `Table.Distinct({"AssetID"})` | One row per asset |
| 8 | Set Data Type | AssetID=Text, EquipmentCategory=Text, etc. | Final type setting |

---

**fact_Failure — Transformation Steps:**

| # | Step | M Code (conceptual) | Rationale |
|---|------|--------------------|-----------|
| 1 | Source | CSV load | Load downtime_log.csv |
| 2 | Promote Headers | Standard | |
| 3 | Validate EventID | Filter where EventID ≠ null | EventID is the primary key — cannot be null |
| 4 | Validate Dates | Filter where DowntimeStart < DowntimeEnd | Ensure logical date order |
| 5 | Validate DowntimeHours | Filter where DowntimeHours >= 0 | Remove impossible negative values |
| 6 | Flag Negative Hours | Custom: if DowntimeHours < 0 then "Suspect" else "Valid" | Track suspect records |
| 7 | Standardize FailureCause | `Text.Proper`, trim whitespace | Consistent capitalisation |
| 8 | Replace Empty Causes | Replace "" with "Unknown" | Handle missing data |
| 9 | Map Failure Consequence | If DowntimeHours > 168 → "Critical", > 48 → "High", > 12 → "Medium", else "Low" | Automated consequence mapping |
| 10 | Add IsRepeatFailure flag | See calculated column (C.5) — this is better as a calculated column in DAX | DAX handles row context better |
| 11 | Set Data Types | See schema in C.3.5 | |
| 12 | Data Quality Summary | Count of suspect records logged to ref_DataQualityLog | Audit trail |

---

**fact_PM_Compliance — Transformation Steps:**

| # | Step | Rationale |
|---|-------|-----------|
| 1 | Source + Headers + Types | Standard |
| 2 | Validate PMDueDate | Must be a valid date |
| 3 | Calculate CompletionStatus | If PMCompletedDate is not null → "Completed", else "Open" |
| 4 | Calculate ScheduleStatus | "On Time" (completed on/before due), "Completed Late" (completed after due), "Overdue" (not completed, past due), "Upcoming" (due in future) |
| 5 | Add DaysOverdue custom column | `if [ScheduleStatus] = "Overdue" then Duration.Days(Date.From(pv_CurrentDate) - [PMDueDate]) else null`; set type to Whole Number |
| 6 | Filter Future PMs | Include only PMs with due date <= today + 30 days (for upcoming view) |
| 7 | Data Type Setting | Match schema in C.3.7 |

---

**General Data Quality Steps (applied to ALL fact and dimension queries):**

| # | Step | Rationale |
|---|-------|-----------|
| 1 | Remove duplicate rows | Based on primary key |
| 2 | Standardise NULL handling | Replace "" with null, replace null with explicit "Unknown" for text fields |
| 3 | Standardise date format | Ensure all dates are Power BI Date type (no DateTime for date-only columns) |
| 4 | Standardise text casing | `Text.Proper` for names, `Text.Upper` for asset IDs |
| 5 | Remove leading/trailing whitespace | `Text.Trim` on all text columns |
| 6 | Validate numerical ranges | Flag negative downtime, >365-day repair duration as "Suspect" |

### G.3 Data Quality Summary Table

Create a reference query `ref_DataQualityLog` that tracks:

| Column | Description |
|--------|-------------|
| QueryName | Which query was being transformed |
| StepName | Which step flagged the issue |
| RecordCount | Number of records processed |
| SuspectCount | Number of suspect records flagged |
| SuspectPct | Percentage of suspect records |
| Timestamp | When transformation ran |

This table is not used in the dashboard visual — it exists for audit and debugging.
You can add it as a hidden page in Power BI for developer use.

---

## H. Build Sequence

### Stage 0: Backup v0.1

**Duration:** 15 minutes

| Step | Action | Verification |
|------|--------|-------------|
| 0.1 | Copy entire `lng-reliability-dashboard/` to `lng-reliability-dashboard-backup/` | Confirm backup folder exists |
| 0.2 | Copy the v0.1 Excel workbook to backup folder | Confirm Excel file in backup |
| 0.3 | In Git: `git add . && git commit -m "v0.1 complete — pre Power BI v0.2 upgrade"` | Git log shows commit |
| 0.4 | Create Git branch: `git checkout -b v0.2-powerbi` | `git branch` shows v0.2-powerbi |

### Stage 1: Inspect Existing Data

**Duration:** 30 minutes

| Step | Action | Verification |
|------|--------|-------------|
| 1.1 | Open the v0.1 Excel workbook | Check all 11 sheets exist |
| 1.2 | Note column names for every sheet | Write down exact column headers |
| 1.3 | Note data types: dates, numbers, text | Check for any currency or percentage columns |
| 1.4 | Check for nulls, blanks, obvious errors | Scan 10-20 rows per sheet |
| 1.5 | Note any calculated fields in Excel | These become measures or calculated columns |
| 1.6 | Confirm processed CSVs exist in data/processed/ | `ls data/processed/*.csv` |

### Stage 2: Create Clean CSV Files for Power BI

**Duration:** 1–2 hours  
**Location:** This can be done in Power Query or by running the v0.1 cleaning notebooks

| Step | Action |
|------|--------|
| 2.1 | Run v0.1 cleaning notebooks (01 → 02) to generate processed CSVs |
| 2.2 | Validate: open each processed CSV and check |
| 2.3 | Confirm: asset_register.csv, downtime_log.csv, maintenance_log.csv, pm_schedule.csv exist |
| 2.4 | Create a lookup CSV for dim_FailureMode with the values from C.3.3 |
| 2.5 | Create a lookup CSV for dim_MaintenanceAction with the values from C.3.4 |

**Output:** Clean CSV files in `data/processed/` ready for Power BI import.

### Stage 3: Save PBIX and Verify CSVs

**Duration:** 30 minutes

| Step | Action | Verification |
|------|--------|-------------|
| 3.1 | Open Power BI Desktop | Blank canvas |
| 3.2 | File -> Save As -> `lng_reliability_dashboard_v0.2.pbix` | File exists before data import begins |
| 3.3 | Verify required CSVs exist in `data/processed/`: `asset_register.csv`, `downtime_log.csv`, `maintenance_log.csv`, `pm_schedule.csv` | Do not proceed if any required file is missing |
| 3.4 | Note optional lookup CSVs if present: `failure_modes_lookup.csv`, `maintenance_actions_lookup.csv` | Optional files are listed before import |

**Important:** Do not assume seven CSVs exist. The three fact files and asset
register are required; lookup files are optional and should only be imported if
they exist.

### Stage 4: Import Tables, Create Date Table, and Build Relationships

**Duration:** 1 hour

| Step | Action | Verification |
|------|--------|-------------|
| 4.1 | Import and clean `asset_register.csv` first; rename query to `dim_Asset` | Asset dimension appears in Fields pane |
| 4.2 | Import and clean all available fact tables: `fact_Failure`, `fact_Maintenance`, `fact_PM_Compliance` | Three fact tables appear with row counts |
| 4.3 | Import optional lookup tables only if the CSVs exist: `dim_FailureMode`, `dim_MaintenanceAction` | Optional dimensions appear if available |
| 4.4 | Create `dim_Date` using DAX with fixed project date bounds | Date table appears in Fields pane |
| 4.5 | Mark `dim_Date[Date]` as the date table | Date table icon appears |
| 4.6 | Build relationships from Section C.4 | Six mandatory relationships are 1:* and single-direction; two lookup relationships are added only if lookup tables are loaded |
| 4.7 | Save the .pbix file | File saved |

**DAX for Date Table:**
```dax
dim_Date =
VAR MinDate = DATE(2020, 1, 1)
VAR MaxDate = DATE(2026, 12, 31)
RETURN
    ADDCOLUMNS(
        CALENDAR(MinDate, MaxDate),
        "Year", YEAR([Date]),
        "Month", MONTH([Date]),
        "MonthName", FORMAT([Date], "mmmm"),
        "Quarter", QUARTER([Date]),
        "QuarterLabel", "Q" & FORMAT([Date], "Q"),
        "YearMonth", FORMAT([Date], "YYYY-MM"),
        "YearMonthLabel", FORMAT([Date], "mmm YYYY"),
        "MonthSort", MONTH([Date])
    )
```

Do not create date relationships until `dim_Date` exists.

### Stage 5: Create Measures Table and Add Calculated Columns

**Duration:** 30 minutes

| Step | Action | DAX |
|------|--------|-----|
| 5.1 | Create a Measures table: Modelling -> New Table | `Measures = ROW("Placeholder", "Measures go here")` |
| 5.2 | Hide `Measures[Placeholder]` in report view | Keeps the Measures table tidy |
| 5.3 | fact_Failure: DowntimeHours column | Already in CSV, but verify it is numeric |
| 5.4 | fact_Failure: RepairHours (if not in data) | `= fact_Failure[DowntimeHours] * 0.8` |
| 5.5 | fact_Failure: IsRepeatFailure | See C.5 |
| 5.6 | Verify all columns show correct values | Spot-check 5 rows per column |

### Stage 6: Create and Test All Measures

**Duration:** 2 hours (the longest single stage)

| Step | Action |
|------|--------|
| 6.1 | Create Measure_TotalDowntimeHours |
| 6.2 | Create Measure_FailureCount |
| 6.3 | Create Measure_TotalRepairHours |
| 6.4 | Create Measure_AvgRepairTime |
| 6.5 | Create Measure_MTTR |
| 6.6 | Create Measure_MTBF_Estimate |
| 6.7 | Create Measure_Availability_Estimate |
| 6.8 | Create Measure_PMCompliance |
| 6.9 | Create Measure_RepeatFailureCount |
| 6.10 | Create Measure_CorrectiveToPreventiveRatio |
| 6.11 | Create Measure_MaintenanceCost |
| 6.12 | Create Measure_CostPerDowntimeHour |
| 6.13 | Create Measure_RiskScore + supporting normalisation |
| 6.14 | Create Measure_HighRiskAssetCount and P2-P4 count measures |
| 6.15 | Create Measure_BadActorScore and Measure_BadActorRanking |
| 6.16 | Create Measure_PreviousPeriodComparison |
| 6.17 | Create Measure_PercentageChange |
| 6.18 | Create Measure_DynamicTitle_... for each page |

**Verification for each measure:** Place it in a card or table visual and check
for a valid numeric value or a valid BLANK() where the denominator or source data
is unavailable. A DAX error is a failure; a justified BLANK() is not.

### Stage 7: Build Each Dashboard Page

**Duration:** 4–6 hours total (break into sub-stages)

**Sub-stage 7.1: Page Design Template (apply to all pages)**
- Set page dimensions to 1280 x 720 px
- Set page background to #FAFAFA
- Add 16px margin guides
- Create a header banner (32px height, #1A1A2E background, white page title text)
- Create navigation button row (7 buttons, uniform size)
- Add company/project logo top-left (or text header)

**Sub-stage 7.2: Page 1 — Executive Overview**
| Step | Action |
|------|--------|
| 7.2a | Create 4 KPI cards in a row (MTBF Estimate, MTTR, Availability Estimate, Total Downtime) |
| 7.2b | Add Monthly Downtime Trend (line + column clustered) |
| 7.2c | Add Availability Estimate by Equipment Category (horizontal bar) |
| 7.2d | Add Top-5 Bad Actors (bar chart) |
| 7.2e | Add KPI Comparison multi-row card |
| 7.2f | Add compact P1-P4 priority summary cards |
| 7.2g | Add slicer: Year-Month hierarchy |
| 7.2h | Add slicer: Equipment Category |

**Sub-stage 7.3: Page 2 — Equipment Performance**
| Step | Action |
|------|--------|
| 7.3a | KPI row: Failure Count, Total Downtime, MTTR, Availability Estimate |
| 7.3b | Scatter plot: MTBF Estimate vs Availability Estimate (bubble = failure count) |
| 7.3c | Stacked bar: Failure Mode by Category |
| 7.3d | Line chart: Monthly Failure Frequency |
| 7.3e | Equipment Detail Table |
| 7.3f | Slicers: Category, Asset, Date Range |

**Sub-stage 7.4: Page 3 — Downtime & Bad Actors**
| Step | Action |
|------|--------|
| 7.4a | KPI row: Total Downtime, Downtime Cost, Repeat Failure Count, C/P Ratio |
| 7.4b | Downtime Pareto chart |
| 7.4c | Bad Actor horizontal bar (top 10) |
| 7.4d | Failure Frequency heatmap |
| 7.4e | Repeat Failure Trend line |
| 7.4f | Slicers: Category, Time Period, Failure Mode |

**Sub-stage 7.5: Page 4 — Failure Modes & Root Causes**
| Step | Action |
|------|--------|
| 7.5a | KPI row: Most Frequent Failure Mode, Total Count, Mean Downtime, Worst Month |
| 7.5b | Failure Mode Pareto |
| 7.5c | Root Cause Treemap |
| 7.5d | Failure Mode by Category (stacked bar 100%) |
| 7.5e | Failure Trend Over Time |
| 7.5f | Asset Failure Timeline scatter |
| 7.5g | Slicers: Failure Mode, Category, Root Cause |

**Sub-stage 7.6: Page 5 — PM Performance**
| Step | Action |
|------|--------|
| 7.6a | KPI row: PM Compliance, PMs Overdue, PMs Completed, Corrective Actions |
| 7.6b | PM Compliance by Category (bar with illustrative 90% project threshold line) |
| 7.6c | PM Completion Trend (line + column) |
| 7.6d | PM vs Corrective correlation scatter |
| 7.6e | Overdue PM Table |
| 7.6f | Slicers: Category, PM Status, Date Range |

**Sub-stage 7.7: Page 6 — Maintenance Risk & Priority**
| Step | Action |
|------|--------|
| 7.7a | KPI row: P1 count, P2 count, P3 count, P4 count |
| 7.7b | 5x5 Risk Matrix scatter plot with background quadrants |
| 7.7c | Risk Score by Equipment bar chart |
| 7.7d | Risk Category Donut |
| 7.7e | Priority Recommendation Table |
| 7.7f | Slicers: Risk Category, Equipment Category, Criticality |

**Sub-stage 7.8: Page 7 — Engineering Recommendations**
| Step | Action |
|------|--------|
| 7.8a | KPI row: High-Risk Assets P1, Needs Review P2, Needs Monitoring P3, Low-Risk Assets P4 |
| 7.8b | Recommendation Distribution Summary using P1-P4 cards or a text panel |
| 7.8c | Priority Summary panel without measure-based chart axes or legends |
| 7.8d | Engineering Interpretation panel and Recommended Action panel |
| 7.8e | Asset Recommendation Table with Asset Name, Equipment Category, Risk Score, Priority Level, Total Downtime, Repeat Failure Count, Suggested Action |
| 7.8f | Slicers: Priority and Equipment Category |
| 7.8g | Add the required risk-derived recommendation disclaimer |

### Stage 8: Add Drill-Through and Tooltips

**Duration:** 1–2 hours

| Step | Action | Verification |
|------|--------|-------------|
| 8.1 | Create Asset Detail drill-through page | Right-click asset → "See details" |
| 8.2 | Set drill-through fields: AssetID (add dim_Asset[AssetID] to drill-through filter pane) | Drill-through filter shows in page settings |
| 8.3 | Add dynamic DAX title: `= SELECTEDVALUE(dim_Asset[AssetName]) & " — Reliability Profile"` | Title changes per asset |
| 8.4 | Add Back button: Insert → Button → Back (select "Back" action type) | Button navigates to source page |
| 8.5 | Create Failure Mode Detail drill-through page | Similar to 8.1-8.4 |
| 8.6 | Create Asset Tooltip page (300x200, mini layout) | |
| 8.7 | Assign tooltip page: select chart → Format → Tooltip → Page → Asset Tooltip | Hover shows tooltip |
| 8.8 | Create KPI Definition Tooltip page | |
| 8.9 | Assign KPI tooltip to card info icons | |

### Stage 9: Add Navigation

**Duration:** 30 minutes

| Step | Action |
|------|--------|
| 9.1 | Create navigation button row on Page 1 (7 buttons) |
| 9.2 | Button type: Blank (custom) |
| 9.3 | Button text: Overview, Equipment, Downtime, Failures, PM, Risk, Recommendations |
| 9.4 | Action: Page navigation → target page |
| 9.5 | Format: #1A1A2E background, white text, 10pt Semibold, 4px radius |
| 9.6 | Copy button row to all 7 pages (edit → copy, then paste on each page) |
| 9.7 | Highlight active page button (different shade or underline) — optional advanced technique using bookmarks |

### Stage 10: Apply Conditional Formatting

**Duration:** 1 hour

| Step | Action |
|------|--------|
| 10.1 | Apply conditional formatting to Risk Score card: Format → Conditional formatting → Background color → Rules |
| 10.2 | Apply to PM Compliance card |
| 10.3 | Apply to Availability Estimate card |
| 10.4 | Apply to Table: Priority column → conditional formatting by field value |
| 10.5 | Apply to Risk Matrix: Likelihood x Consequence → background shading (use play axis or gradient) |
| 10.6 | Apply to KPI trend arrows: Format → Conditional formatting → Font color → Rules |
| 10.7 | Apply to all bar charts: Series color = rules based on measure value |

### Stage 11: Validate Results

**Duration:** 1 hour

| # | Validation Check | How to Perform | Pass Criteria |
|---|-----------------|----------------|---------------|
| 11.1 | All measures evaluate correctly | Add each measure to a card or table visual | Valid numeric result, or valid BLANK() where no denominator/source data exists; no DAX errors |
| 11.2 | Cross-filtering works | Click a bar in one visual | Other visuals update |
| 11.3 | Drill-through navigates correctly | Right-click asset → drill-through | Correct asset detail page |
| 11.4 | Tooltips appear on hover | Hover over each visual type | Tooltip content is accurate |
| 11.5 | Navigation buttons work | Click each button | Correct page loads |
| 11.6 | Slicers filter correctly | Select a slicer value | All visuals update |
| 11.7 | Date table marked correctly | Model view → Date table | Checkmark icon |
| 11.8 | Required relationships single-direction | Model view | Six mandatory relationships exist; optional lookup relationships exist only when lookup tables are loaded; no bidirectionals |
| 11.9 | Page dimensions consistent | Check each page properties | All 1280x720 |
| 11.10 | Conditional formatting looks right | Visual inspection | No ugly overlaps |
| 11.11 | Disclaimers present on risk page | Visual inspection | Text visible |
| 11.12 | KPI definitions correct (spot-check 3) | Calculate manually in Excel | DAX result matches Excel |

### Stage 12: Capture Portfolio Screenshots

**Duration:** 30 minutes

| # | Screenshot | Page | Purpose |
|---|------------|------|---------|
| 1 | Executive Overview (full page) | Page 1 | Primary LinkedIn/GitHub image |
| 2 | Equipment Performance with data visible | Page 2 | Shows depth |
| 3 | Downtime Pareto | Page 3 | Shows engineering thinking |
| 4 | Failure Mode Breakdown | Page 4 | Shows failure analysis capability |
| 5 | PM Compliance | Page 5 | Shows maintenance awareness |
| 6 | Risk Matrix | Page 6 | Shows risk management skills |
| 7 | Engineering Recommendations | Page 7 | Shows risk-derived engineering recommendations |
| 8 | Asset Detail drill-through | Drill-through | Shows technical depth |

**Screenshot technique:**
1. Set slicers to meaningful default state (last 12 months)
2. Press Ctrl+Shift+S (Power BI screenshot)
3. Save as PNG in `screenshots/` folder with descriptive names
4. Min file sizes: compress PNGs (use tinypng.com or equivalent)

### Stage 13: Update GitHub Documentation

**Duration:** 1 hour

| # | File | Change |
|---|------|--------|
| 1 | README.md | Add "View Interactive Power BI Dashboard" section with screenshots and link to .pbix |
| 2 | docs/architecture_plan.md | Add v0.2 Power BI section with page descriptions |
| 3 | docs/assumptions_and_limitations.md | Add Power BI v0.2 specific assumptions |
| 4 | screenshots/README.md | Describe each screenshot |
| 5 | .gitignore | Add *.pbix if >100MB (optional, Power BI files may exceed GitHub free limit) |
| 6 | docs/data_inventory.md | Update with Power BI table names |

**Note on .pbix file size:** Power BI files can exceed 50MB quickly. If yours is large:
- Option A: Host on Google Drive / OneDrive and link in README
- Option B: Include a .pbit (template) file instead, which excludes the data
- Option C: Put .pbix in GitHub Releases (not the main repo)

---

## I. Acceptance Criteria

### I.1 Functional Criteria

| # | Criteria | How to Verify | Pass/Fail |
|---|----------|---------------|-----------|
| F1 | All 7 report pages exist with correct names | Navigation pane shows all 7 pages | |
| F2 | The model contains mandatory tables dim_Date, dim_Asset, fact_Failure, fact_Maintenance, fact_PM_Compliance; optional dim_FailureMode and dim_MaintenanceAction are present only if their lookup CSVs were loaded | Model view inspection | |
| F3 | Date table dim_Date is marked as Date Table | Date table icon in Model view | |
| F4 | Six mandatory relationships are 1:* single direction; two lookup relationships are conditional | Model view inspection | |
| F5 | All measures from Section D return valid numeric values or valid BLANK() where data is unavailable | Card/table visual spot-check | |
| F6 | Risk Score measure uses the 0-100 scale per asset | Table visual spot-check | |
| F7 | Bad Actor Ranking ranks assets 1..N | Table visual spot-check | |
| F8 | Drill-through from Equipment page → Asset Detail works | Right-click → drill-through | |
| F9 | Drill-through from Failures page → Failure Detail works | Right-click → drill-through | |
| F10 | Navigation buttons on all pages are functional | Click each | |
| F11 | Slicers on all pages filter data correctly | Select a category, visual updates | |
| F12 | At least one dynamic DAX title is used | Title text changes with filter | |

### I.2 Design Criteria

| # | Criteria | How to Verify | Pass/Fail |
|---|----------|---------------|-----------|
| D1 | Page dimensions are 1280x720 | Page properties | |
| D2 | Consistent header with page title on every page | Visual inspection | |
| D3 | KPI cards use consistent 4-card-per-row layout | Visual inspection | |
| D4 | Colour meanings are consistent (Red=bad, Green=good) | Check all pages | |
| D5 | No pure black (#000000) text | Check font colours | |
| D6 | No decorative-only visuals (gauge, word cloud) | Visual inspection | |
| D7 | Background is #FAFAFA or near-white | Page properties | |
| D8 | Risk page has safety warning disclaimer | Text visible | |
| D9 | All chart titles include time period context | Read each title | |

### I.3 Data Quality Criteria

| # | Criteria | How to Verify | Pass/Fail |
|---|----------|---------------|-----------|
| Q1 | All dates are Date type, not DateTime where date-only | Column data types | |
| Q2 | No null primary keys (EventID, WorkOrderID, etc.) | Column profile in Power Query | |
| Q3 | DowntimeHours ≥ 0 for all records | Column distribution check | |
| Q4 | Equipment names are standardised (no duplicates) | dim_Asset distinct count | |
| Q5 | Failure modes are standardised if dim_FailureMode is loaded (no "bearng" vs "bearing") | dim_FailureMode distinct list, if available | |
| Q6 | Data quality suspect records are flagged | ref_DataQualityLog exists | |

### I.4 Portfolio Criteria

| # | Criteria | Pass/Fail |
|---|----------|-----------|
| P1 | At least 6 portfolio-quality screenshots saved in screenshots/ | |
| P2 | README.md updated with Power BI section | |
| P3 | Disclaimer about public data remains prominent in README | |
| P4 | Git branch v0.2-powerbi exists and is pushed | |
| P5 | KPI definitions are documented (either in architecture plan or Power BI measure descriptions) | |

---

## J. Portfolio Value

### J.1 Mechanical Engineering Understanding

This dashboard demonstrates mechanical engineering knowledge through:

| Feature | What It Proves to an Employer |
|---------|-------------------------------|
| Equipment categories mapped to LNG operations | You understand LNG plant equipment taxonomy — compressors, turbines, pumps, heat exchangers |
| Failure mode taxonomy (bearing, seal, overheating) | You know the common failure modes of rotating equipment |
| MTBF Estimate/MTTR/Availability Estimate computation | You understand reliability fundamentals and the limits of estimated operating-time metrics |
| Risk-based prioritisation | You think in terms of consequence and likelihood — core to mechanical integrity engineering |
| Asset criticality classification (A/B/C) | You understand that not all assets have equal operational importance |

### J.2 Reliability Engineering Thinking

| Feature | What It Proves |
|---------|----------------|
| Bad actor identification | You can use data to identify which assets need engineering attention — not guesswork |
| Repeat failure tracking | You understand that a failure that recurs is a failure of root cause analysis |
| Pareto analysis (80/20 rule) | You know that reliability improvements come from focusing on the vital few, not the trivial many |
| PM compliance vs corrective ratio | You understand that the PM program's effectiveness can be measured — not just its completion rate |
| Rolling trend analysis | You track whether reliability is improving or deteriorating over time |
| Clear labelling of estimates vs facts | You have intellectual honesty — critical in safety-critical industries |

### J.3 Maintenance Decision Support

| Feature | What It Proves |
|---------|----------------|
| Risk matrix (5x5 secondary visual) | You can communicate likelihood-consequence context without confusing it with the primary 0-100 ranking |
| Risk-derived engineering recommendations | You understand that analysis should produce reviewable engineering recommendations, not unauthorised work instructions |
| Drill-through to asset detail | You can guide maintenance teams from dashboard-level insight to asset-specific action |
| Equipment performance scatter (MTBF Estimate vs Availability Estimate) | You can identify equipment categories that need different maintenance strategies |
| PM vs corrective correlation | You can evaluate whether the PM program is actually effective |

### J.4 Power BI Competence

| Skill | Demonstrated By |
|-------|-----------------|
| Data modelling | Star schema design with 7 analytical tables plus a Measures table, 6 mandatory relationships, and 2 conditional lookup relationships |
| DAX measures | 16+ measures using CALCULATE, FILTER, DIVIDE, RANKX, DATESBETWEEN |
| Power Query | 6+ transformation steps per query, data quality tracking |
| Visual design | Professional grid layout, consistent typography, intentional colour usage |
| Interactivity | Cross-filtering, drill-through, tooltips, navigation buttons |
| Conditional formatting | Rule-based formatting on KPIs, tables, charts |
| Dynamic titles | DAX-driven titles that respond to filter context |
| Data quality | Suspect flagging, audit trail, validation rules |

### J.5 AI-Augmented Engineering Workflow

| Feature | What It Proves |
|---------|----------------|
| LLM-generated engineering recommendations (carried from v0.1) | You use AI responsibly — with caveats, review requirements, and source disclosure |
| Architecture plan co-created with AI | You know how to delegate to AI while maintaining engineering oversight |
| Code/AI collaboration methodology | You designed a build sequence where AI can assist (DAX generation, Power Query steps) without replacing engineering judgment |

### J.6 Oil & Gas Career Relevance

| Employer Priority | How This Dashboard Addresses It |
|-------------------|---------------------------------|
| Process safety culture | Risk matrix with disclaimers, safety consequence tracking, safety warning on risk page |
| Asset integrity | Equipment criticality, failure mode analysis, mechanical integrity data |
| Operations technical support | Drill-through from KPIs to asset detail — supports operational decision-making |
| Data-driven maintenance | Bad actor identification, PM compliance tracking, C/P ratio |
| Reliability improvement | MTBF Estimate/MTTR/Availability Estimate trends, period-over-period comparison |
| Professional communication | Clear visual hierarchy, documented assumptions, honest data sourcing |
| Graduate potential | Built from scratch using public data — shows initiative and ability to learn independently |

---

## First Action & Pre-Work Checklist

### Your First Action in Power BI

**"Before opening Power BI, collect the following information from your existing v0.1 dashboard."**

### Pre-Work Checklist: What to Collect From v0.1

Before making any changes, gather these items:

| # | Item to Collect | Location in v0.1 | Completed? |
|---|----------------|-------------------|------------|
| 1 | Screenshot of every Excel sheet with column headers visible | Excel workbook → each sheet | ☐ |
| 2 | Screenshot of the asset register (all rows) | Excel → Asset Register sheet | ☐ |
| 3 | Screenshot of downtime log sample (first 20 rows) | Excel → Downtime Log sheet | ☐ |
| 4 | Screenshot of failure summary table | Notebook 03 or Excel → Failure Summary | ☐ |
| 5 | Note: what does the "Consequence" column contain? (Text? Numbers? 1-5?) | Excel → any sheet with consequence data | ☐ |
| 6 | Note: exact MTBF, MTTR, Availability values from v0.1 (3 numbers) | Excel → Reliability KPIs sheet | ☐ |
| 7 | Note: list of ALL failure modes in the data (e.g., Bearing, Seal, etc.) | Any sheet with failure mode column | ☐ |
| 8 | Note: list of ALL equipment categories (e.g., Compressor, Pump, etc.) | Asset Register sheet | ☐ |
| 9 | Note: date range of data (earliest to latest failure date) | Downtime Log sheet → sort by date | ☐ |
| 10 | Note: does the data have cost fields? Yes/No + column names | Any sheet with $ or cost data | ☐ |
| 11 | Note: does the data have PM schedule data? Yes/No | Look for PM completion dates | ☐ |
| 12 | Note: any data quality issues you spotted (nulls, duplicates, typos) | Visual scan of each sheet | ☐ |
| 13 | Confirm the processed CSV files are the final cleaned version | Check data/processed/*.csv | ☐ |
| 14 | Confirm the LLM recommendations text is saved (for Engineering Recommendations page) | Excel → AI Recommendations sheet | ☐ |

### Minimum Viable First Power BI Session

When you sit down to build v0.2, do these things **in this order**:

1. Save the PBIX file.
2. Verify the required CSV files exist.
3. Import and clean `dim_Asset`.
4. Import and clean all available fact tables.
5. Import optional lookup tables.
6. Create and mark `dim_Date`.
7. Build relationships.
8. Create the `Measures` table with `Measures = ROW("Placeholder", "Measures go here")` and hide `Measures[Placeholder]`.
9. Create calculated columns only where required.
10. Create and test DAX measures.
11. Build Page 1.
12. Continue with remaining pages.
---

*End of v0.2 Architecture & Upgrade Plan*
*Review this document alongside your v0.1 Excel workbook before making changes.*
