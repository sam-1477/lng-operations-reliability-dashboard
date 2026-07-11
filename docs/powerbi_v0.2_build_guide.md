# LNG Operations Technical Reliability Dashboard
## Power BI v0.2 — Beginner Build Guide

**Version:** 1.0  
**Prerequisite:** Read `docs/powerbi_v0.2_architecture_plan.md` first  
**Skill Level:** Power BI beginner (no DAX experience assumed)  
**Estimated Build Time:** 12–18 hours  

---

## How to Use This Guide

Each page has 16 numbered steps. Do them **in order**. Every step is written so a
first-time Power BI user can follow it.

**Before you start:** Complete the pre-work checklist at the end of the architecture
plan. You need your v0.1 Excel workbook open and your processed CSV files ready.

---

## Phase 0: Project Setup (Do This First)

Follow this exact setup order. Do not create a measure before its referenced
fact or dimension table exists, and do not build date relationships before
`dim_Date` exists.

1. Save the PBIX file.
2. Verify the required CSV files exist.
3. Import and clean `dim_Asset`.
4. Import and clean all available fact tables.
5. Import optional lookup tables.
6. Create and mark `dim_Date`.
7. Build relationships.
8. Create the `Measures` table.
9. Create calculated columns only where required.
10. Create and test DAX measures.
11. Build Page 1.
12. Continue with remaining pages.

### 0.1 Save the Power BI Desktop File

1. Open Power BI Desktop (the free version from Microsoft Store)
2. Click **File -> Save As**
3. Navigate to your project folder: `D:\ai-portfolio-projects\lng-reliability-dashboard\`
4. File name: `lng_reliability_dashboard_v0.2.pbix`
5. Click **Save**

### 0.2 Verify Source CSV Files Exist

Before importing anything, confirm the required CSV files exist in your
`data/processed/` folder:

- `asset_register.csv`
- `downtime_log.csv` (or `fact_Failure.csv`)
- `maintenance_log.csv` (or `fact_Maintenance.csv`)
- `pm_schedule.csv` (or `fact_PM_Compliance.csv`)

Optional lookup CSV files, if available:

- `failure_modes_lookup.csv` (for `dim_FailureMode`)
- `maintenance_actions_lookup.csv` (for `dim_MaintenanceAction`)

If a required file is missing, run the v0.1 data-cleaning notebooks first to
generate it. **Do not assume seven CSVs exist.** Import optional lookup files only
when they are present.

### 0.3 Import and Clean dim_Asset

Import the asset register first. It is the primary dimension used by every fact
table.

1. Click **Home -> Get Data -> Text/CSV**
2. Navigate to your processed data folder (for example, `data/processed/`)
3. Select `asset_register.csv` and click **Open**
4. A preview window appears; check the data looks correct
5. Click **Transform Data** (not Load)
6. In Power Query Editor, apply the transformations below
7. When done, click **Home -> Close & Apply**

#### dim_Asset (asset_register.csv)

| Step | What to Do | Where |
|------|-----------|-------|
| 1 | Click **Use First Row as Headers** | Home tab |
| 2 | Click column header **AssetID** → Check it shows "Text" data type | Transform tab |
| 3 | Check all columns have correct types (Text for names, Whole Number for operating hours) | Transform → Data Type |
| 4 | Click **Remove Rows → Remove Duplicates** | Home tab |
| 5 | Right-click AssetID column → **Remove Duplicates** (again, per-column) | Right-click menu |
| 6 | On the **Query Settings** pane (right), rename the query from the file name to `dim_Asset` | Properties → Name |

**If you see any null values in CriticalityRating:**
1. Select the CriticalityRating column
2. Click **Transform → Replace Values**
3. Replace `null` with `"C"`

### 0.4 Import and Clean All Available Fact Tables

Import the three available fact tables after dim_Asset.

#### fact_Failure (downtime_log.csv) — Most Important Table

| Step | What to Do | Where |
|------|-----------|-------|
| 1 | Use First Row as Headers | Home |
| 2 | Select **EventID** column → Set type to **Whole Number** | Transform → Data Type |
| 3 | Select **AssetID** column → Set type to **Text** | |
| 4 | Select **FailureDate** column → Set type to **Date** (NOT DateTime) | |
| 5 | Select **DowntimeStart**, **DowntimeEnd** → Set type to **Date/Time** | |
| 6 | Select **DowntimeHours**, **RepairHours** → Set type to **Decimal Number** | |
| 7 | Select **RepairCost** → Set type to **Decimal Number** | |
| 8 | Select **FailureModeID** → Set type to **Whole Number** | |
| 9 | Click **Remove Rows → Remove Duplicates** | Home |
| 10 | Right-click EventID → **Remove Duplicates** | Right-click |
| 11 | Click **Keep Rows → Keep Bottom Rows → enter 100** — this is just a quick check (undo after) | Home |
| 12 | Click **Undo** (to undo step 11) | Home → Undo |
| 13 | Rename to `fact_Failure` | Properties |

**Null check:** Click the DowntimeHours column dropdown → check "null" is not checked.
If it is, investigate the offending rows in your source CSV.

#### fact_Maintenance (maintenance_log.csv)

| Step | What to Do |
|------|-----------|
| 1 | Use First Row as Headers |
| 2 | Set data types: WorkOrderID=Whole Number, AssetID=Text, MaintenanceDate=Date, ActionID=Whole Number, MaintenanceType=Text, LaborHours=Decimal, PartsCost=Decimal, TotalCost=Decimal |
| 3 | Remove duplicates |
| 4 | Rename to `fact_Maintenance` |

#### fact_PM_Compliance (pm_schedule.csv)

| Step | What to Do |
|------|-----------|
| 1 | Use First Row as Headers |
| 2 | Set data types: PMRecordID=Whole Number, AssetID=Text, PMDueDate=Date, PMCompletedDate=Date (nullable), PMCategory=Text, PMFrequency=Text, CompletionStatus=Text, ScheduleStatus=Text, AssignedTeam=Text |
| 3 | Remove duplicates |
| 4 | Rename to `fact_PM_Compliance` |

#### Add DaysOverdue in Power Query

`DaysOverdue` is a row-level preparation field, so Power Query is preferred.
Create it before you use `fact_PM_Compliance[DaysOverdue]` in Page 5.

1. In Power Query Editor, select `fact_PM_Compliance`
2. Click **Add Column**
3. Click **Custom Column**
4. Name: `DaysOverdue`
5. Paste this formula:

```powerquery
if [ScheduleStatus] = "Overdue" then
    Duration.Days(Date.From(pv_CurrentDate) - [PMDueDate])
else
    null
```

6. Set data type to **Whole Number**

If you do not have a `pv_CurrentDate` parameter, create it as a Date parameter
that defaults to today's date for the current portfolio build.

**Optional DAX fallback:** Use this only if you cannot create the Power Query
column. Power Query is preferred because this is row-level preparation logic.

```dax
DaysOverdue =
IF(
    fact_PM_Compliance[ScheduleStatus] = "Overdue",
    DATEDIFF(
        fact_PM_Compliance[PMDueDate],
        TODAY(),
        DAY
    ),
    BLANK()
)
```

**Important:** If PMCompletedDate has blanks (nulls), that is normal — it means the
PM has not been completed yet. Do NOT replace nulls with a date.

### 0.5 Import Optional Lookup Tables

Import these only if the CSV files exist. If they are missing, continue with the
core model and add the lookup tables later.

#### dim_FailureMode (failure_modes_lookup.csv)

| Step | What to Do |
|------|-----------|
| 1 | Use First Row as Headers |
| 2 | Check data types (all Text except FailureModeID = Whole Number) |
| 3 | Rename query to `dim_FailureMode` |

#### dim_MaintenanceAction (maintenance_actions_lookup.csv)

| Step | What to Do |
|------|-----------|
| 1 | Use First Row as Headers |
| 2 | Check data types |
| 3 | Rename query to `dim_MaintenanceAction` |

### 0.6 Create and Mark dim_Date

Power BI needs a dedicated date table for time intelligence functions such as
period-over-period comparisons and rolling calculations.

1. Go to **Model View** (left sidebar, second icon)
2. Click **New Table**
3. Paste this formula into the formula bar:

```dax
dim_Date =
VAR MinDate = DATE(2020, 1, 1)
VAR MaxDate = DATE(2026, 12, 31)
RETURN
    ADDCOLUMNS(
        CALENDAR(MinDate, MaxDate),
        "Year", YEAR([Date]),
        "MonthNumber", MONTH([Date]),
        "MonthName", FORMAT([Date], "mmmm"),
        "Quarter", QUARTER([Date]),
        "QuarterLabel", "Q" & FORMAT([Date], "Q"),
        "YearMonth", FORMAT([Date], "YYYY-MM"),
        "YearMonthLabel", FORMAT([Date], "mmm YYYY"),
        "MonthSort", MONTH([Date])
    )
```

4. Press Enter. You should see a new table called `dim_Date` appear in the Fields pane.
5. Select `dim_Date`, go to **Table tools**, click **Mark as date table**, and choose `dim_Date[Date]`.

**Date range note:** This fixed date range is project-bound and suitable for the
current portfolio dataset. It is not a reusable production strategy. A production
model should derive date bounds from fact-table dates or use an approved wider
enterprise date range.

Do not build relationships to `dim_Date` until this table exists.

### 0.7 Build Relationships (Model View)

This is the most important step. Incorrect relationships = incorrect numbers.

1. Click **Model View** (left sidebar, second icon)
2. You will see boxes representing all your tables with fields listed inside

Now create the six mandatory relationships by dragging and dropping:

| # | Drag FROM | Drop ONTO | Ensures |
|---|-----------|-----------|---------|
| 1 | dim_Date[Date] | fact_Failure[FailureDate] | Date filtering works |
| 2 | dim_Asset[AssetID] | fact_Failure[AssetID] | Asset names appear in failure data |
| 3 | dim_Date[Date] | fact_Maintenance[MaintenanceDate] | Date filtering works for maintenance |
| 4 | dim_Asset[AssetID] | fact_Maintenance[AssetID] | Asset names in maintenance |
| 5 | dim_Date[Date] | fact_PM_Compliance[PMDueDate] | Date filtering for PM |
| 6 | dim_Asset[AssetID] | fact_PM_Compliance[AssetID] | Asset names in PM |

Create these two conditional relationships only if the optional lookup tables were loaded:

| # | Drag FROM | Drop ONTO | Condition |
|---|-----------|-----------|-----------|
| 7 | dim_FailureMode[FailureModeID] | fact_Failure[FailureModeID] | Only if `dim_FailureMode` is loaded |
| 8 | dim_MaintenanceAction[ActionID] | fact_Maintenance[ActionID] | Only if `dim_MaintenanceAction` is loaded |

**How to verify each relationship:**
1. After dragging, a line appears between the two tables with a "1" and "*" symbol
2. The "1" side = the dimension table (lookup)
3. The "*" side = the fact table (data)
4. If you see "*" on BOTH sides, you did something wrong — right-click the line and delete, then try again

**Common mistake:** If Power BI creates an "Auto-detect" relationship that you
did not intend (e.g., between dim_Date and fact_PM_Compliance on a different column),
right-click the unwanted line → **Delete**.

**Your final model should look like:**
- dim_Date in the center (connected to all three fact tables)
- dim_Asset connected to all three fact tables
- dim_FailureMode connected to fact_Failure only if loaded
- dim_MaintenanceAction connected to fact_Maintenance only if loaded
- EquipmentCategory and CategoryGroup are columns in dim_Asset (no separate lookup table needed)

### 0.8 Create the Measures Table

A dedicated table keeps all DAX measures organised in one place.

1. Go to **Modeling tab** -> **New Table**
2. Paste this exact formula:
   ```dax
   Measures = ROW("Placeholder", "Measures go here")
   ```
3. Press Enter
4. In the **Fields** pane, right-click `Measures[Placeholder]` -> **Hide in report view**
5. Create all new measures in the `Measures` table

### 0.9 Add Calculated Columns

Go to **Table View** (left sidebar, third icon). We need two calculated columns in
fact_Failure. Wait — check if your source CSV already has these columns. If yes,
skip the corresponding step.

#### IsRepeatFailure Column

1. Click on the fact_Failure table
2. Click **New Column** in the ribbon (Table tools tab)
3. Paste:
```dax
IsRepeatFailure =
VAR CurrentAsset = fact_Failure[AssetID]
VAR CurrentMode = fact_Failure[FailureModeID]
VAR CurrentDate = fact_Failure[FailureDate]
VAR PriorSameFailure =
    COUNTROWS(
        FILTER(
            fact_Failure,
            fact_Failure[AssetID] = CurrentAsset &&
            fact_Failure[FailureModeID] = CurrentMode &&
            fact_Failure[FailureDate] < CurrentDate &&
            fact_Failure[FailureDate] > CurrentDate - 90
        )
    )
RETURN
    PriorSameFailure > 0
```
4. This will return TRUE if the same asset+mode happened within the prior 90 days.
5. Check the first few rows by clicking the column header — some should be TRUE, some FALSE.

#### RepairHours Column (If Not in Your Data)

If your downtime log does NOT have a separate RepairHours column:
1. Click on fact_Failure
2. Click **New Column**
3. Paste:
```dax
RepairHours = fact_Failure[DowntimeHours] * 0.80
```
4. This assumes active repair time is about 80% of total downtime (the rest is
   waiting for parts, crew, etc.). This is an assumption — document it.

### 0.10 Create and Test DAX Measures

This is the longest single step. Create each measure by:

1. Go to **Report View** (left sidebar, first icon — looks like a stacked bar chart)
2. Right-click the `Measures` table in the Fields pane
3. Click **New measure**
4. Paste the formula
5. Press Enter
6. The measure appears under the Measures table with a calculator icon

**VERY IMPORTANT:** After creating each measure, TEST IT immediately:

1. Click on a blank area of the report canvas
2. Click the **Table** visual (Visualizations pane)
3. Drag the measure to the table
4. You should see a valid number or a valid BLANK() where the denominator/source data is unavailable, not "#ERROR"
5. If you see "#ERROR", double-check the formula — look for:
   - Misspelled column names (e.g., "FailureData" instead of "FailureDate")
   - Missing closing parentheses
   - Wrong table names

**After testing, DELETE the temporary table visual.**

Create the measures in the order shown below. Do not create a measure before the measures it references already exist:

---

#### M1: TotalDowntimeHours

```dax
Measure_TotalDowntimeHours = SUM(fact_Failure[DowntimeHours])
```

**Test:** Place in a card visual. You should see a number like "1245.5".
**Format:** Select the measure → Measure tools tab → "0.0" format (one decimal).

---

#### M2: FailureCount

```dax
Measure_FailureCount = COUNTROWS(fact_Failure)
```

**Test:** Should show an integer like "87".
**Format:** Whole number.

---

#### M3: TotalRepairHours

```dax
Measure_TotalRepairHours = SUM(fact_Failure[RepairHours])
```

**Test:** Should be less than TotalDowntimeHours (roughly 80% of it).
**Format:** "0.0"

---

#### M4: AvgRepairTime

```dax
Measure_AvgRepairTime = DIVIDE([Measure_TotalRepairHours], [Measure_FailureCount], BLANK())
```

**Test:** Should be TotalRepairHours / FailureCount. If FailureCount=0, shows BLANK().
**Format:** "0.0"
**Note:** `DIVIDE(x, y, BLANK())` returns BLANK() if y=0. That is correct when the ratio is unavailable.

---

#### M5: MTTR

```dax
Measure_MTTR = [Measure_AvgRepairTime]
```

**Test:** Should show the same value as AvgRepairTime.
**Note:** Yes, this is the same measure. We create it separately so that if we later
change the MTTR definition (e.g., to exclude waiting time), we only change Measure_MTTR,
not every visual that uses AvgRepairTime.

---

#### M6: MTBF Estimate

```dax
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

**Test:** Should be EstimatedOperatingDays / FailureCount.
**Format:** "0.0" (days)

**What's happening in this formula:**
- `ALLSELECTED(dim_Asset[AssetID])` counts selected assets in the current report context
- `MIN(dim_Date[Date])` and `MAX(dim_Date[Date])` define the observation period
- `ObservationDays × SelectedAssetCount` produces selected-fleet observation days
- `0.95` adjusts for estimated operating availability and is an assumption
- `DIVIDE(..., ..., BLANK())` returns BLANK if no failures exist. BLANK is treated as missing data by Power BI and avoids distorting charts, filters, and rankings.

**Important:** This is an estimate. It assumes selected assets were available for
the full observation period. True MTBF requires actual operating hours.

---

#### M7: Availability Estimate

```dax
[Measure_Availability_Estimate] =
VAR MTBF_Days = [Measure_MTBF_Estimate]
VAR MTTR_Days = DIVIDE([Measure_MTTR], 24, BLANK())
RETURN
    DIVIDE(
        MTBF_Days,
        MTBF_Days + MTTR_Days,
        BLANK()
    )
```

**Test:** Should be a decimal between 0.88 and 0.99 for typical data, or BLANK() if MTBF/MTTR is unavailable. If you see
"1.00" something is wrong (MTTR is 0 or MTBF-estimate is huge).
**Format:** Select measure → Measure tools → Percentage with 1 decimal (99.5%).

---

#### M8: PMCompliance

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

**Test:** Should be a decimal like 0.85 (85%).
**Format:** Percentage, 1 decimal.
**If you get blank:** Check that fact_PM_Compliance has rows. Check ScheduleStatus
column has values like "On Time", "Overdue", "Upcoming".

---

#### M9: RepeatFailureCount

```dax
Measure_RepeatFailureCount =
CALCULATE(
    COUNTROWS(fact_Failure),
    fact_Failure[IsRepeatFailure] = TRUE
)
```

**Test:** Should be less than total FailureCount. If it equals FailureCount, every
failure was a repeat — which is unlikely.
**Format:** Whole number.

---

#### M10: CorrectiveToPreventiveRatio

```dax
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
```

**Test:** If Corrective=60 and Preventive=40, this shows 1.5. If Preventive=0, shows blank.
**Format:** "0.0"

---

#### M11: MaintenanceCost

```dax
Measure_MaintenanceCost = SUM(fact_Maintenance[TotalCost])
```

**Test:** Should show a number. If your data doesn't have cost fields, this will be 0
and that's OK — label it clearly.
**Format:** Currency ($) with 0 decimals if >$1000, 2 decimals if small.

---

#### M12: CostPerDowntimeHour

```dax
Measure_CostPerDowntimeHour =
DIVIDE([Measure_MaintenanceCost], [Measure_TotalDowntimeHours], BLANK())
```

**Test:** MaintenanceCost / TotalDowntimeHours. If downtime is unavailable or zero, shows BLANK().
**Format:** Currency ($), 2 decimals.

---

#### M13: RiskScore and PriorityLevel

Create the primary 0-100 risk score before any P1/P2/P3/P4 count measures.

```dax
[Measure_RiskScore] =
VAR DT_Score =
    DIVIDE(
        [Measure_TotalDowntimeHours],
        MAXX(ALLSELECTED(dim_Asset[AssetID]), CALCULATE([Measure_TotalDowntimeHours])),
        BLANK()
    ) * 30
VAR Freq_Score =
    DIVIDE(
        [Measure_FailureCount],
        MAXX(ALLSELECTED(dim_Asset[AssetID]), CALCULATE([Measure_FailureCount])),
        BLANK()
    ) * 25
VAR Cost_Score =
    DIVIDE(
        [Measure_MaintenanceCost],
        MAXX(ALLSELECTED(dim_Asset[AssetID]), CALCULATE([Measure_MaintenanceCost])),
        BLANK()
    ) * 15
VAR Cons_Score =
    IF(
        CALCULATE(
            COUNTROWS(fact_Failure),
            fact_Failure[FailureConsequence] IN {"High", "Critical"}
        ) > 0,
        20,
        IF(
            CALCULATE(
                COUNTROWS(fact_Failure),
                fact_Failure[FailureConsequence] = "Medium"
            ) > 0,
            14,
            IF(CALCULATE(COUNTROWS(fact_Failure)) > 0, 6, 0)
        )
    )
VAR Repeat_Score = IF([Measure_RepeatFailureCount] > 0, 10, 0)
RETURN
    DT_Score + Freq_Score + Cost_Score + Cons_Score + Repeat_Score
```

**Test:** Place in a table with `dim_Asset[AssetID]`. Scores should range 0-100.
**Warning:** This is an illustrative prioritisation tool, not a formal safety risk assessment.

```dax
Measure_PriorityLevel =
VAR Score = [Measure_RiskScore]
RETURN
    SWITCH(
        TRUE(),
        Score >= 60, "P1 - Immediate Action",
        Score >= 40, "P2 - High Priority",
        Score >= 20, "P3 - Scheduled",
        Score >= 0, "P4 - Routine",
        "Unrated"
    )
```

Primary risk thresholds:
- P1: 60-100
- P2: 40-59.99
- P3: 20-39.99
- P4: 0-19.99

---

#### M14: P1-P4 Risk Asset Counts

```dax
[Measure_HighRiskAssetCount] =
COUNTROWS(
    FILTER(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_RiskScore]) >= 60
    )
)
```

```dax
[Measure_P2AssetCount] =
COUNTROWS(
    FILTER(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_RiskScore]) >= 40 &&
        CALCULATE([Measure_RiskScore]) < 60
    )
)
```

```dax
[Measure_P3AssetCount] =
COUNTROWS(
    FILTER(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_RiskScore]) >= 20 &&
        CALCULATE([Measure_RiskScore]) < 40
    )
)
```

```dax
[Measure_P4AssetCount] =
COUNTROWS(
    FILTER(
        ALLSELECTED(dim_Asset[AssetID]),
        CALCULATE([Measure_RiskScore]) >= 0 &&
        CALCULATE([Measure_RiskScore]) < 20
    )
)
```

**Test:** Place each count in a card. Counts should be whole numbers >= 0.

---

#### M15: BadActorScore and BadActorRanking

**Create the supporting score first:**

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

**Then create the ranking:**

```dax
[Measure_BadActorRanking] =
RANKX(
    ALLSELECTED(dim_Asset[AssetID]),
    [Measure_BadActorScore],
    ,
    DESC,
    DENSE
)
```

**Test:** Place `Measure_BadActorRanking` in a table with AssetID. Asset with rank 1
should have the highest combined score.

---

#### M16: PreviousPeriodDowntime

```dax
Measure_PreviousPeriodDowntime =
CALCULATE(
    [Measure_TotalDowntimeHours],
    PREVIOUSMONTH(dim_Date[Date])
)
```

**Test:** If current month = July 2026, this shows June 2026 downtime, or BLANK()
if there is no prior-period data.

---

#### M17: PercentageChange (Downtime)

```dax
Measure_DowntimeChange =
VAR CurrentValue = [Measure_TotalDowntimeHours]
VAR PriorValue = [Measure_PreviousPeriodDowntime]
RETURN
    DIVIDE(CurrentValue - PriorValue, PriorValue, BLANK())
```

**Test:** If current month=100 hrs and previous month=80 hrs, shows 0.25 (25% increase).
If no prior period exists, shows BLANK().
**Format:** Percentage, 1 decimal.
**Watch out:** Positive = MORE downtime = WORSE. This is a "bad increase" metric.

---
## Phase 1: Executive Reliability Overview (Page 1)

**This is the first page you build.** It is the landing page that a Maintenance Manager
opens first. Get this right before moving on.

### 1.1 Page Setup

1. Click the **+** icon at the bottom to add a new page
2. Right-click the page tab → **Rename** → type: `Executive Overview`
3. Right-click → **Hide Page** — NO, do NOT hide this (it's the landing page)
4. With the page selected, go to the **Format** pane (paint roller icon)
5. Expand **Page Size**
6. Set: Width = `1280`, Height = `720`
7. Expand **Page Background**
8. Color: `#FAFAFA`
9. Expand **Filter Pane** → turn OFF
10. Expand **Visual Header** → turn ON icons, turn OFF the ... menu if too busy

### 1.2 Create the Navigation Bar (Copy to All Pages Later)

1. Click **Insert → Buttons → Blank**
2. Resize to about 120x32 pixels
3. In the Format pane:
   - **Button text:** `Overview` (11pt Segoe UI, White, Semibold)
   - **Button fill:** #1A1A2E
   - **Border radius:** 4px
   - **Action → Type:** Page navigation → select "Executive Overview"
4. Copy the button (Ctrl+C) and paste 6 more copies
5. Place them in a row at the top, change labels to:
   Equipment, Downtime, Failures, PM, Risk, Recommendations
6. Set each button's action to navigate to the correct page

**Tip:** Hold Alt while dragging to align buttons to the grid.

**We will add this bar to other pages later (copy/paste).** For now, just create
it on this page.

### 1.3 KPI Cards (Top Row — 4 Cards)

Each card is a **Card** visual (not Multi-Row Card). Create them side by side.

**Card 1: MTBF Estimate**

| Setting | Value |
|---------|-------|
| Visual type | Card (Visualizations pane, first icon) |
| Field | Measure_MTBF_Estimate |
| Dropdown arrow | Not needed (card shows the value) |
| Format → Callout value → Font | 28pt, Bold, #1A1A2E |
| Format → Category label → Text | "MTBF Estimate (Days)" — but we'll set this differently |

**Better approach — use a text box above:** Instead of relying on the card's built-in
label, insert a Text Box above the card with the label. This gives you more control.

1. Click **Insert → Text Box**
2. Type: `MTBF Estimate`
3. Font: 10pt, Segoe UI, #666666
4. Place it directly above where your card will go

**For ALL four cards, repeat this pattern:**

| Card | Measure | Label | Unit below |
|------|---------|-------|-------------|
| Card 1 | Measure_MTBF_Estimate | MTBF Estimate | Days |
| Card 2 | Measure_MTTR | MTTR | Hours |
| Card 3 | Measure_Availability_Estimate | Availability Estimate | % |
| Card 4 | Measure_TotalDowntimeHours | Total Downtime | Hours |

**Card formatting (apply to all 4 cards):**

1. Select the card
2. Format pane:
   - **Visual → Card → Callout value:** Font = 28pt, Color = #1A1A2E
   - **Visual → Card → Category label:** Turn OFF (we use text boxes instead)
   - **General → Effects → Visual border:** Turn ON, Color = #E5E7EB, Radius = 4px
   - **General → Effects → Shadow:** Preset = Small

**Conditional formatting for card colour:**

1. Select MTBF Estimate card
2. Format pane → Visual → Card → Callout value
3. Click the fx (conditional formatting) button next to Color
4. Format style: Rules
5. Based on field: Measure_MTBF_Estimate
6. Rules:
   - If value >= 90 → Green (#10B981)
   - If value >= 30 → Amber (#F59E0B)
   - If value < 30 → Red (#EF4444)

Repeat for MTTR (thresholds reversed: >=24=Red, >=8=Amber, <8=Green),
Availability Estimate (>=0.97=Green, >=0.95=Amber, <0.95=Red).

**Common mistake:** Do NOT use the "Background color" fx on cards — use "Font color"
on the callout value. Background coloring on cards looks unprofessional.

### 1.4 Monthly Downtime Trend (Center-Left Visual)

**What this answers:** "Is downtime getting better or worse over time?"

| Setting | Value |
|---------|-------|
| Visual type | Line and Clustered Column Chart |
| Shared axis | dim_Date[YearMonth] (as a hierarchy or text field) |
| Column values | Measure_TotalDowntimeHours — Sum |
| Line values | Measure_FailureCount — Sum |
| Sort | dim_Date[YearMonth] ascending by YearMonth (not alphabetically) |

**Steps:**

1. Click the **Line and Clustered Column Chart** visual
2. Drag `dim_Date[YearMonth]` to **Shared axis**
3. Drag `Measure_TotalDowntimeHours` to **Column y-axis**
4. Drag `Measure_FailureCount` to **Line y-axis**

**Formatting:**

| Element | Setting |
|---------|---------|
| X-axis → Type | Categorical (not Continuous) |
| X-axis → Labels | 45° rotation if too many months |
| Column color | #3B82F6 (Steel Blue) |
| Line color | #EF4444 (Red) |
| Line width | 2px |
| Data labels | Turn OFF on column, Turn ON on line (last point only) |
| Visual → Title | "Monthly Downtime & Failure Trend" |
| General → Effects → Shadow | Small |

**Sorting fix:** YearMonth like "2026-07" sorts alphabetically.
Make sure your YearMonth uses "YYYY-MM" format so January comes before February.

**Common mistake:** If the chart shows years as multiple bars (2026, 2026, 2026),
your YearMonth field is a hierarchy, not a flat field. Use `dim_Date[YearMonth]`
(the text field, not the Date hierarchy). If your dim_Date has a YearMonth hierarchy,
expand it and select the YearMonth text field specifically.

### 1.5 Availability Estimate by Equipment Category (Right Visual)

**What this answers:** "Which equipment types are least reliable?"

| Setting | Value |
|---------|-------|
| Visual type | Clustered Bar Chart (horizontal bars) |
| Axis | dim_Asset[EquipmentCategory] |
| Values | Measure_Availability_Estimate — Do Not Summarize (it's already a measure) |
| Sort | By Measure_Availability_Estimate ascending (worst first) |

**Steps:**

1. Click **Clustered Bar Chart**
2. Drag `dim_Asset[EquipmentCategory]` to **Y-axis**
3. Drag `Measure_Availability_Estimate` to **X-axis**
4. Click the **...** on the chart → Sort axis → Measure_Availability_Estimate → Sort ascending

**Formatting:**

| Element | Setting |
|---------|---------|
| Each bar color | Use conditional formatting: Rules based on Availability Estimate |
| Rule 1: >= 0.97 | #10B981 (Green) |
| Rule 2: >= 0.95 | #F59E0B (Amber) |
| Rule 3: < 0.95 | #EF4444 (Red) |
| Data labels | ON, positioned "Outside end" |
| Data label format | Percentage, 1 decimal |
| Title | "Availability Estimate by Equipment Category" |
| Title font | 11pt Semibold |
| X-axis → Type | Continuous |

**Tooltip:** We'll add custom tooltips later. For now, the default tooltip (showing
Equipment Category + Availability Estimate) is acceptable.

### 1.6 Top-5 Bad Actors (Bottom Left Visual)

**What this answers:** "Which specific assets are costing us the most downtime?"

| Setting | Value |
|---------|-------|
| Visual type | Clustered Bar Chart (horizontal) |
| Y-axis | dim_Asset[AssetName] |
| X-axis | Measure_TotalDowntimeHours |
| Filter | Top N: Show Top 5 by Measure_TotalDowntimeHours |

**Steps:**

1. Click **Clustered Bar Chart**
2. Drag `dim_Asset[AssetName]` to Y-axis
3. Drag `Measure_TotalDowntimeHours` to X-axis
4. In the **Filters pane** (right side, not Visualizations):
   - Drag `dim_Asset[AssetName]` to **Filters on this visual**
   - Click the dropdown → **Filter type:** Top N
   - **Show items:** Top → **5**
   - **By value:** Measure_TotalDowntimeHours
   - Click **Apply filter**

**Formatting:**

| Setting | Value |
|---------|-------|
| Bar color | Single color = #EF4444 (Red — highlight bad actors) |
| Data labels | On, positioned "Outside end", format "0.0 hrs" |
| Title | "Top-5 Bad Actors — Highest Downtime" |
| Subtitle (text box below) | "Assets causing greatest operational loss" |
| X-axis | Unit = hours |

### 1.7 KPI Comparison (Bottom Right)

**What this answers:** "Are we improving or deteriorating compared to last period?"

| Setting | Value |
|---------|-------|
| Visual type | Table |
| Columns | Measure_KPI (we'll create this), Measure Value, Previous Period, Change % |

Instead of a table, use a **Multi-Row Card** visual:

1. Click the **Multi-Row Card** visual
2. Drag the following measures to the **Fields** well (they appear as rows):
   - Measure_MTBF_Estimate
   - Measure_MTTR
   - Measure_Availability_Estimate
   - Measure_PMCompliance

**Formatting:**

| Element | Setting |
|---------|---------|
| Category label | ON, 9pt, #666666 |
| Callout value | 14pt, Bold, #1A1A2E |
| Show all labels | ON |
| Spacing | Comfortable |
| Title | "KPI Summary" |

### 1.8 Compact Priority Summary (Small Visual, Bottom Right Area)

**What this answers:** "How many assets are in each risk-priority band?"

Do not use a DAX measure as a donut legend. A DAX measure cannot be used as a
standard categorical legend or axis. Use four compact cards instead.

| Card | Measure | Label | Color |
|------|---------|-------|-------|
| 1 | Measure_HighRiskAssetCount | P1 | #EF4444 |
| 2 | Measure_P2AssetCount | P2 | #F59E0B |
| 3 | Measure_P3AssetCount | P3 | #EAB308 |
| 4 | Measure_P4AssetCount | P4 | #10B981 |

**Steps:**

1. Add four small Card visuals in a row
2. Add one P1-P4 count measure to each card
3. Add a text box title: `Priority Summary`
4. Add small text labels under the cards: `P1`, `P2`, `P3`, `P4`
5. Use the color rules above for each card's callout value or border

### 1.9 Slicers

| Slicer | Type | Field | Orientation |
|--------|------|-------|-------------|
| Date | Dropdown | dim_Date[YearMonth] (single select, default=latest) | Horizontal |
| Category | Dropdown | dim_Asset[EquipmentCategory] (multi-select) | Horizontal |

**Steps for date slicer:**

1. Click **Slicer** visual
2. Drag `dim_Date[YearMonth]` to **Field**
3. Format → Slicer settings → Style = "Dropdown"
4. Format → Slicer header = ON, "Time Period", 10pt

**Steps for category slicer:**

1. Click **Slicer** visual
2. Drag `dim_Asset[EquipmentCategory]` to **Field**
3. Style = "Dropdown"
4. Select multiple = ON (check the box in Slicer settings)

**Set default values:** Click the dropdown and select the most recent month
for the date slicer. No selection for category slicer (shows all).

### 1.10 Disclaimers

At the bottom of the page, add a Text Box:

```
Data source: Public datasets (PHMSA, MetroPT-3, Azure PdM) adapted to LNG context.
KPIs marked "estimate" are based on assumed operating hours — see documentation.
```

Font: 8pt, Italic, #999999, Segoe UI.

### 1.11 Validation Test

| Test | Expected Result |
|------|----------------|
| Slicer selects month | All visuals update |
| Cross-filter: click bad actor bar | Other visuals filter to that asset |
| KPI values seem reasonable | MTBF Estimate 30-300 days, MTTR 2-48 hrs, Availability Estimate 88-99% |
| Priority donut has 4 segments | No blank "Unknown" segment |

### 1.12 Screenshot to Capture

After the page is complete and formatted:
1. Set slicers to: Last 6 months, All equipment
2. Press **Ctrl + Shift + S** (Power BI screenshot)
3. Save to: `screenshots/page1_executive_overview.png`

---

## Phase 2: Equipment Performance (Page 2)

### 2.1 Page Setup

1. Click + to add new page
2. Rename: "Equipment Performance"
3. Size: 1280x720
4. Background: #FAFAFA
5. Copy the navigation bar from Page 1 and paste it here
6. Update the "Equipment" button to look active (different shade — optional for now)

### 2.2 KPI Cards

Four cards, same as Page 1 but with different measures:

| Card | Measure | Label |
|------|---------|-------|
| 1 | Measure_FailureCount | Failure Count |
| 2 | Measure_TotalDowntimeHours | Total Downtime |
| 3 | Measure_MTTR | MTTR |
| 4 | Measure_Availability_Estimate | Availability Estimate |

Apply the same formatting from Section 1.3.

### 2.3 Scatter Plot: MTBF Estimate vs Availability Estimate

**What this answers:** "Which equipment categories combine low reliability (MTBF Estimate)
with poor restoration (Availability Estimate)?"

| Setting | Value |
|---------|-------|
| Visual type | Scatter Chart |
| Values | dim_Asset[EquipmentCategory] |
| X-axis | Measure_MTBF_Estimate |
| Y-axis | Measure_Availability_Estimate |
| Size | Measure_FailureCount |
| Legend | dim_Asset[EquipmentCategory] (or leave blank for category bubbles) |

**Steps:**

1. Click **Scatter Chart**
2. Drag `dim_Asset[EquipmentCategory]` to **Values** (creates one bubble per category)
3. Drag `Measure_MTBF_Estimate` to **X-axis**
4. Drag `Measure_Availability_Estimate` to **Y-axis**
5. Drag `Measure_FailureCount` to **Size**

**Formatting:**

| Element | Setting |
|---------|---------|
| X-axis range | 0 to max MTBF Estimate (automatically set) |
| Y-axis range | 0.80 to 1.00 (manually set min to 0.80 for meaningful spread) |
| Data labels | ON: Category name next to each bubble |
| Title | "Equipment Performance — MTBF Estimate vs Availability Estimate" |
| Subtitle | "Bubble size = failure count. Top-right = best performance" |

**How to read this chart:**
- **Top-right** = high MTBF Estimate + high Availability Estimate = best performing
- **Bottom-left** = low MTBF Estimate + low Availability Estimate = worst performing
- **Biggest bubble** = most failures (warrants investigation)

### 2.4 Failure Mode Distribution (Top Right)

**What this answers:** "What types of failures affect each equipment category?"

| Setting | Value |
|---------|-------|
| Visual type | Stacked Bar Chart (100%) |
| Axis | dim_Asset[EquipmentCategory] |
| Legend | dim_FailureMode[FailureMode] |
| Values | Count of fact_Failure[EventID] — Count |

**Steps:**

1. Click **Stacked Bar Chart** (100% version — find it in the visual gallery)
2. Drag `dim_Asset[EquipmentCategory]` to **Axis**
3. Drag `dim_FailureMode[FailureMode]` to **Legend**
4. Drag `fact_Failure[EventID]` to **Values** → change aggregation to **Count**

**Formatting:**

| Element | Setting |
|---------|---------|
| Title | "Failure Mode Distribution by Equipment" |
| Data labels | ON: Percent of total |
| Legend | Right side, 9pt |
| Colors | Assign manually for consistency: Bearing=#EF4444, Seal=#F59E0B, Overheating=#EAB308, Vibration=#3B82F6, Electrical=#8B5CF6, Other=#9CA3AF |

### 2.5 Monthly Failure Frequency (Bottom Right)

**What this answers:** "Are failures becoming more or less frequent?"

| Setting | Value |
|---------|-------|
| Visual type | Line Chart |
| Axis | dim_Date[YearMonth] |
| Values | Measure_FailureCount |
| Legend | dim_Asset[EquipmentCategory] — if you want lines per category |

**Steps:**

1. Click **Line Chart**
2. Drag `dim_Date[YearMonth]` to **Axis**
3. Drag `Measure_FailureCount` to **Values**
4. Drag `dim_Asset[EquipmentCategory]` to **Legend** (optional — shows one line per category)
5. Without legend: single line showing total failures per month

**Formatting:**

| Element | Setting |
|---------|---------|
| Title | "Failure Frequency Trend" |
| Line color (single line) | #3B82F6 |
| Line width | 2px |
| Data labels | Last point only, bold |
| Y-axis label | "Failure Count" |
| X-axis | Show for last 12 periods only (use filter) |

### 2.6 Equipment Detail Table (Bottom)

**What this answers:** "Give me the raw data so I can find specific assets."

| Setting | Value |
|---------|-------|
| Visual type | Table |
| Columns (in order) | See below |

Drag these fields to **Columns** in this exact order:

1. `dim_Asset[AssetName]` — Text
2. `dim_Asset[EquipmentCategory]` — Text
3. `Measure_FailureCount` — Sum (auto)
4. `Measure_TotalDowntimeHours` — Sum
5. `Measure_MTTR` — Auto
6. `Measure_MTBF_Estimate` — Auto
7. `Measure_Availability_Estimate` — Auto

**Table formatting:**

| Element | Setting |
|---------|---------|
| Header font | 10pt, Bold, White, Background = #1A1A2E |
| Row font | 9pt, Segoe UI |
| Alternating rows | ON: alternating grey #F9FAFB |
| Grid | Horizontal lines only, #E5E7EB |
| Column widths | Adjust so all columns fit without horizontal scroll |
| Title | "Asset Reliability Detail" |
| Values → Units | Availability Estimate = %, MTBF Estimate = "days", MTTR = "hrs" |

**Conditional formatting on Availability Estimate column:**

1. Select the table → **Format** pane → **Conditional formatting**
2. Find **Availability Estimate** in the list
3. Turn ON **Background color**
4. Format style: Rules
5. Rules:
   - >= 0.97 → Green (#10B981, white text)
   - >= 0.95 → Amber (#F59E0B, black text)
   - < 0.95 → Red (#EF4444, white text)
6. Turn ON **Font color** → same rules (white on green/red, black on amber)

### 2.7 Slicers

| Slicer | Type | Field |
|--------|------|-------|
| Equipment Category | Dropdown | dim_Asset[EquipmentCategory] |
| Asset | Dropdown | dim_Asset[AssetName] — changes based on category selection |
| Date Range | Between (slider) | dim_Date[Date] |

**Steps for dependent slicers:**

1. Create slicer for Equipment Category (dropdown, multi-select)
2. Create slicer for Asset (dropdown, single select)
3. Click the Asset slicer → Format pane → **Edit interactions** (or just the slicer
   settings) → Under **Visual interactions**, check that the Equipment Category slicer
   filters the Asset slicer (this is the default behavior when both use the same
   dimension table — Power BI does this automatically)

**Date range slicer:**

1. Click **Slicer** → select "Between" style
2. Drag `dim_Date[Date]` to Field
3. Format → Slicer settings → Style = "Between"
4. On the slicer, drag the handles to select your date range
5. Default: Last 12 months

### 2.8 Visual Filters

| Visual | Filter | Value |
|--------|--------|-------|
| Monthly Failure Trend | dim_Date[YearMonth] | Last 12 months (Top N filter, Bottom 12) |
| Scatter Plot | No filter | All data |

### 2.9 Validation Test

| Test | Expected |
|------|----------|
| Select a category in slicer | Table filters to that category |
| Click a bubble in scatter | Other visuals filter to that category |
| Table shows multiple rows | At least 5-10 assets visible |
| Availability Estimate colors look correct | Green/Amber/Red visible |

### 2.10 Screenshot

Save: `screenshots/page2_equipment_performance.png`

---

## Phase 3: Downtime and Bad Actors (Page 3)

### 3.1 Page Setup

Add new page → Rename: "Downtime and Bad Actors" → 1280x720 → #FAFAFA → Paste nav bar.

### 3.2 KPI Cards

| Card | Measure | Label |
|------|---------|-------|
| 1 | Measure_TotalDowntimeHours | Total Downtime |
| 2 | Measure_MaintenanceCost | Downtime Cost (estimated) |
| 3 | Measure_RepeatFailureCount | Repeat Failures |
| 4 | Measure_CorrectiveToPreventiveRatio | C/P Ratio |

### 3.3 Downtime Pareto Chart (Top Left)

**What this answers:** "Which 20% of assets cause 80% of our downtime?"

| Setting | Value |
|---------|-------|
| Visual type | Pareto Line (this is a combination line + column chart) |
| Category | dim_Asset[AssetName] |
| Value | Measure_TotalDowntimeHours |

**Steps for creating a Pareto in Power BI:**

Power BI does not have a built-in Pareto chart. Create it manually:

1. Add a **Line and Clustered Column Chart**
2. Drag `dim_Asset[AssetName]` to **Shared axis**
3. Drag `Measure_TotalDowntimeHours` to **Column y-axis**
4. Create a new measure for cumulative percentage:

```dax
Measure_DowntimeParetoPct =
VAR AllAssets = ALLSELECTED(dim_Asset)
VAR CurrentAssetDowntime = [Measure_TotalDowntimeHours]
VAR TotalDowntimeAll = CALCULATE([Measure_TotalDowntimeHours], AllAssets)
VAR CumulativeDowntime =
    CALCULATE(
        [Measure_TotalDowntimeHours],
        AllAssets,
        FILTER(
            AllAssets,
            [Measure_TotalDowntimeHours] >= CurrentAssetDowntime ||
            ([Measure_TotalDowntimeHours] = CurrentAssetDowntime &&
             dim_Asset[AssetName] <= MAX(dim_Asset[AssetName]))
        )
    )
RETURN
    DIVIDE(CumulativeDowntime, TotalDowntimeAll, BLANK())
```

5. Drag `Measure_DowntimeParetoPct` to **Line y-axis**
6. Format the line y-axis as Percentage

**Alternative approach (easier for beginners):**

Use a standard **Clustered Column Chart** sorted by downtime descending, and add a
text box annotation saying "Top 3 assets cause X% of downtime" using a measure:

```dax
Measure_Top3Pct =
VAR Top3Downtime =
    CALCULATE(
        [Measure_TotalDowntimeHours],
        TOPN(3, ALL(dim_Asset), [Measure_TotalDowntimeHours], DESC)
    )
VAR TotalDowntime = CALCULATE([Measure_TotalDowntimeHours], ALL(dim_Asset))
RETURN
    DIVIDE(Top3Downtime, TotalDowntime, BLANK())
```

This measure tells you the percentage without needing a complex Pareto chart.
Place it in a Card visual below the bar chart.

**For the bar chart:**

| Setting | Value |
|---------|-------|
| Visual type | Clustered Column Chart |
| Axis | dim_Asset[AssetName] |
| Value | Measure_TotalDowntimeHours |
| Sort | By Measure_TotalDowntimeHours descending |
| Filter | Top N = 10 |

### 3.4 Bad Actor Horizontal Bar (Top Right)

**What this answers:** "Which assets rank worst on our combined bad-actor score?"

| Setting | Value |
|---------|-------|
| Visual type | Clustered Bar Chart |
| Y-axis | dim_Asset[AssetName] |
| X-axis | Measure_BadActorScore |
| Sort | Measure_BadActorScore descending |

**Color by risk:** Use conditional formatting:

1. Select the bars → Format → Visual → Bars
2. Click the fx button next to **Color**
3. Format style = Rules
4. Based on field = Measure_BadActorScore
5. Rules: >= 60 = #EF4444, >= 30 = #F59E0B, < 30 = #10B981

### 3.5 Failure Frequency Heatmap (Bottom Left)

**What this answers:** "Which combinations of asset + failure mode happen most often?"

| Setting | Value |
|---------|-------|
| Visual type | Matrix |
| Rows | dim_Asset[AssetName] |
| Columns | dim_FailureMode[FailureMode] |
| Values | Count of fact_Failure[EventID] — Count (not Sum) |

**Steps:**

1. Click **Matrix** visual
2. Drag `dim_Asset[AssetName]` to **Rows**
3. Drag `dim_FailureMode[FailureMode]` to **Columns**
4. Drag `fact_Failure[EventID]` to **Values** → Change to **Count**

**Formatting:**

| Element | Setting |
|---------|---------|
| Row headers | Bold, background alternating |
| Column headers | Bold, white text on #1A1A2E |
| Conditional formatting → Background color | Color scale: White (low) → #EF4444 (high) |
| Title | "Failure Frequency — Asset x Failure Mode" |

**How to read this:** A cell with dark red = that asset + failure mode happens
frequently. Investigate why.

### 3.6 Repeat Failure Trend (Bottom Right)

**What this answers:** "Are repeat failures becoming more common?"

| Setting | Value |
|---------|-------|
| Visual type | Line Chart |
| Axis | dim_Date[YearMonth] |
| Values | Measure_RepeatFailureCount |

**Formatting:**

| Element | Setting |
|---------|---------|
| Line color | #EF4444 |
| Line width | 2px |
| Data labels | Last point only |
| Title | "Repeat Failure Trend — Failures Recurring Within 90 Days" |

### 3.7 Slicers

| Slicer | Type | Field |
|--------|------|-------|
| Equipment Category | Dropdown | dim_Asset[EquipmentCategory] |
| Failure Mode | Dropdown | dim_FailureMode[FailureMode] (multi-select) |
| Time Period | Relative (pre-made) | dim_Date — use "Last 6 months" or "Last 12 months" |

**Quick relative date slicer:**

1. Click **Slicer**
2. Drag `dim_Date[Date]` to Field
3. Format → Slicer settings → Style = "Relative Date"
4. Set: "Show items when the value is: in the last 12 calendar months"

### 3.8 Validation Test

| Test | Expected |
|------|----------|
| Downtime Pareto bars sorted descending | Yes |
| Bad actor scores show clear ranking | Yes |
| Heatmap has colored cells | At least some cells are red |
| Repeat failures < total failures | Yes |

### 3.9 Screenshot

Save: `screenshots/page3_downtime_bad_actors.png`

---

## Phase 4: Failure Modes and Root Causes (Page 4)

### 4.1 Page Setup

Add new page → Rename: "Failure Modes and Root Causes" → 1280x720 → #FAFAFA → Paste nav bar.

### 4.2 KPI Cards

| Card | Measure | Label |
|------|---------|-------|
| 1 | Measure_FailureCount (with a twist — show mode) | Most Frequent Failure Mode |
| 2 | Measure_FailureCount | Total Failure Count |
| 3 | Measure_AvgRepairTime | Mean Downtime per Failure |
| 4 | Measure_TotalRepairHours | Total Repair Hours |

**For Card 1 (Most Frequent Failure Mode text):**

The measure returns text instead of a number:

```dax
Measure_MostFrequentFailureMode =
VAR TopMode =
    TOPN(
        1,
        ALL(dim_FailureMode[FailureMode]),
        CALCULATE(COUNTROWS(fact_Failure))
    )
RETURN
    MAXX(TopMode, dim_FailureMode[FailureMode])
```

Place this in a Card visual. The card will show the failure mode name as text.

### 4.3 Failure Mode Pareto (Top Left)

**What this answers:** "Which failure modes cause the most disruptions?"

| Setting | Value |
|---------|-------|
| Visual type | Clustered Column Chart |
| Axis | dim_FailureMode[FailureMode] |
| Values | Count of fact_Failure[EventID] — Count |
| Sort | By Count descending |

**Formatting:** Bar color = #3B82F6. Title = "Failure Mode Pareto — Ranked by Frequency".

### 4.4 Root Cause Distribution (Top Right)

**What this answers:** "What root causes are driving our failures?"

| Setting | Value |
|---------|-------|
| Visual type | Pie Chart (or Treemap for many categories) |
| Legend | dim_FailureMode[FailureMechanism] (if you have this column) OR dim_FailureMode[FailureClass] |
| Values | Count of fact_Failure[EventID] |

**Recommendation:** Use a **Treemap** if you have many root cause categories.
It shows size relationships more effectively than a pie.

| Setting | Value |
|---------|-------|
| Visual type | Treemap |
| Category | dim_FailureMode[FailureMechanism] |
| Values | Count of fact_Failure[EventID] |
| Detail | dim_FailureMode[FailureMode] (optional sub-categories) |

### 4.5 Failure Mode by Equipment (Middle Left)

**What this answers:** "Do different equipment types suffer from different failure modes?"

| Setting | Value |
|---------|-------|
| Visual type | 100% Stacked Bar Chart |
| Axis | dim_FailureMode[FailureMode] |
| Legend | dim_Asset[EquipmentCategory] |
| Values | Count of fact_Failure[EventID] |

### 4.6 Failure Trend Over Time (Middle Right)

**What this answers:** "Are failure patterns changing?"

| Setting | Value |
|---------|-------|
| Visual type | Line Chart |
| Axis | dim_Date[YearMonth] |
| Values | Measure_FailureCount |
| Legend | dim_FailureMode[FailureMode] |

**Formatting:**

| Element | Setting |
|---------|---------|
| Title | "Failure Trend by Failure Mode" |
| Legend position | Bottom |
| Line styles | Solid lines, assign each mode a distinct colour |
| Y-axis minimum | 0 (to avoid exaggerating trends) |

### 4.7 Slicers

| Slicer | Type | Field |
|--------|------|-------|
| Failure Mode | Dropdown | dim_FailureMode[FailureMode] |
| Equipment Category | Dropdown | dim_Asset[EquipmentCategory] |
| Year | Dropdown | dim_Date[Year] |

### 4.8 Validation Test

| Test | Expected |
|------|----------|
| Pareto shows "Bearing" at top (if data supports) | Most frequent mode first |
| Treemap shows clear size hierarchy | Yes |
| Trend shows monthly pattern | At least some variation |

### 4.9 Screenshot

Save: `screenshots/page4_failure_modes.png`

---

## Phase 5: PM Performance (Page 5)

### 5.1 Page Setup

Add new page → Rename: "PM Performance" → 1280x720 → #FAFAFA → Paste nav bar.

### 5.2 KPI Cards

| Card | Measure | Label |
|------|---------|-------|
| 1 | Measure_PMCompliance | PM Compliance |
| 2 | Measure_OverduePMs | PMs Overdue |
| 3 | Measure_CompletedPMs | PMs Completed |
| 4 | Measure_CorrectiveToPreventiveRatio | C/P Ratio |

**For Card 2 (Overdue PMs):**

```dax
Measure_OverduePMs =
CALCULATE(
    COUNTROWS(fact_PM_Compliance),
    fact_PM_Compliance[ScheduleStatus] = "Overdue"
)
```

**For Card 3 (Completed PMs):**

```dax
Measure_CompletedPMs =
CALCULATE(
    COUNTROWS(fact_PM_Compliance),
    fact_PM_Compliance[CompletionStatus] = "Completed"
)
```

### 5.3 PM Compliance by Category (Left)

**What this answers:** "Which equipment categories are falling behind on PMs?"

| Setting | Value |
|---------|-------|
| Visual type | Clustered Bar Chart |
| Y-axis | dim_Asset[EquipmentCategory] |
| X-axis | Measure_PMCompliance |
| Sort | Ascending by compliance (worst first) |

**Add an illustrative project threshold line:**

Power BI doesn't have built-in reference lines on bar charts for free version.
Alternative: Add a text box annotation: "Illustrative project threshold: 90%".

### 5.4 PM Completion Trend (Top Right)

**What this answers:** "Are we completing more or fewer PMs each month?"

| Setting | Value |
|---------|-------|
| Visual type | Line and Clustered Column Chart |
| Shared axis | dim_Date[YearMonth] |
| Column values | COUNTROWS(fact_PM_Compliance) — Count (scheduled) |
| Line values | Measure_CompletedPMs — Sum (actually Count) |

**For the line:**
```dax
Measure_MonthlyPMsCompleted =
CALCULATE(
    COUNTROWS(fact_PM_Compliance),
    fact_PM_Compliance[CompletionStatus] = "Completed"
)
```

Drag this to the Line y-axis.

### 5.5 PM vs Corrective Correlation (Bottom Left)

**What this answers:** "Does higher PM compliance actually reduce corrective work?"

| Setting | Value |
|---------|-------|
| Visual type | Scatter Chart |
| Values | dim_Date[YearMonthLabel] |
| X-axis | Measure_PMCompliance (for each month) |
| Y-axis | Measure_CorrectiveToPreventiveRatio |

**Theory:** If PM is effective, months with higher compliance should have lower
C/P ratios. The scatter plot will show whether this correlation exists in your data.

**Formatting:**

| Element | Setting |
|---------|---------|
| Data labels | ON: show YearMonthLabel |
| Trend line | ON: add a linear trend line (Format pane → Analytics → Trend line) |
| X-axis minimum | 0.50 (50%) |
| Title | "PM Compliance vs Corrective Ratio — Is PM Effective?" |

### 5.6 Overdue PM Table (Bottom Right)

**What this answers:** "Which specific PM tasks are overdue?"

| Setting | Value |
|---------|-------|
| Visual type | Table |
| Columns (in order): | |
| | dim_Asset[AssetName] |
| | fact_PM_Compliance[PMCategory] |
| | fact_PM_Compliance[PMDueDate] |
| | fact_PM_Compliance[DaysOverdue] |
| | dim_Asset[EquipmentCategory] |

**Filters:**

1. Drag `fact_PM_Compliance[DaysOverdue]` to **Filters on this visual**
2. Filter type: "Greater than" → Value: 0
3. Click **Apply filter**

This shows only overdue PMs.

**Conditional formatting on DaysOverdue:**
- Red background (#EF4444) if > 30 days
- Amber (#F59E0B) if 15-30 days
- Yellow (#EAB308) if 1-14 days

### 5.7 Slicers

| Slicer | Type | Field |
|--------|------|-------|
| Equipment Category | Dropdown | dim_Asset[EquipmentCategory] |
| PM Status | Dropdown | fact_PM_Compliance[ScheduleStatus] |
| Date Range | Between | dim_Date[Date] |

### 5.8 Validation Test

| Test | Expected |
|------|----------|
| PM Compliance < 100% | Yes (some are overdue) |
| Overdue table shows rows with DaysOverdue > 0 | Yes |
| Scatter chart shows some spread | Not all points in one cluster |

### 5.9 Screenshot

Save: `screenshots/page5_pm_performance.png`

---

## Phase 6: Maintenance Risk and Priority (Page 6)

### 6.1 Page Setup

Add new page → Rename: "Risk and Priority" → 1280x720 → #FAFAFA → Paste nav bar.

**Important:** Add a prominent disclaimer at the top of this page:

1. Insert a **Text Box** at the top
2. Type: "⚠ This is an illustrative risk prioritization tool. NOT a formal safety
   risk assessment. All decisions require authorized engineering review."
3. Font: 9pt, Italic, #EF4444, Segoe UI
4. Background: #FEF2F2 (light red), Border: 1px solid #EF4444
5. Width: Full page width

### 6.2 KPI Cards

| Card | Measure | Label |
|------|---------|-------|
| 1 | Measure_HighRiskAssetCount | High-Risk Assets P1 |
| 2 | Measure_P2AssetCount | Needs Review P2 |
| 3 | Measure_P3AssetCount | Needs Monitoring P3 |
| 4 | Measure_P4AssetCount | Low-Risk Assets P4 |

Use the P1-P4 measures created in Phase 0.10. The primary risk score is always
on a 0-100 scale:

- P1: 60-100
- P2: 40-59.99
- P3: 20-39.99
- P4: 0-19.99

### 6.3 5x5 Risk Matrix (Left Side, Large)

**What this answers:** "Where does each asset sit on a likelihood-consequence grid?"

This 5x5 matrix is a secondary visual aid using 1-5 likelihood and 1-5 consequence
ratings. It is not the primary ranking measure. The primary ranking measure is
`Measure_RiskScore` on the 0-100 scale.

Power BI does not have a built-in 5x5 risk matrix visual. Here are two approaches.

**Approach A: Scatter Plot (Recommended for Beginners)**

| Setting | Value |
|---------|-------|
| Visual type | Scatter Chart |
| Details | dim_Asset[AssetName] |
| X-axis | Likelihood Score (1-5) |
| Y-axis | Consequence Score (1-5) |

**Likelihood Score based on failure frequency:**

```dax
Measure_LikelihoodScore =
VAR Freq = DIVIDE([Measure_FailureCount], 12, BLANK()) -- Approximate per month
RETURN
    SWITCH(TRUE(),
        Freq > 6, 5,
        Freq >= 3, 4,
        Freq >= 1, 3,
        Freq >= 0.33, 2,
        Freq > 0, 1,
        1
    )
```

**Consequence Score based on downtime:**

```dax
Measure_ConsequenceScore_5x5 =
VAR AvgDowntime = [Measure_AvgRepairTime]
RETURN
    SWITCH(TRUE(),
        AvgDowntime > 168, 5,   -- > 7 days
        AvgDowntime > 48, 4,    -- 2-7 days
        AvgDowntime > 12, 3,    -- 12-48 hours
        AvgDowntime > 2, 2,     -- 2-12 hours
        1                       -- < 2 hours or unavailable
    )
```

**Scatter formatting:**

| Element | Setting |
|---------|---------|
| X-axis range | 0.5 to 5.5 |
| Y-axis range | 0.5 to 5.5 |
| Category label | dim_Asset[AssetName] |
| Color | Single neutral color, or conditional color rules based on Measure_RiskScore if available |
| Title | "Secondary 5x5 Matrix - Likelihood vs Consequence" |

The quadrant labels are visual interpretation only. They must not override the
primary 0-100 risk priority.

**Approach B: Table with Conditional Formatting (Easier)**

If the scatter plot is too complex, use a Table with these columns:

| Visual type | Table |
|-------------|-------|
| Columns | AssetName, LikelihoodScore, ConsequenceScore, RiskScore, PriorityLevel |

Then apply conditional formatting to highlight P1 rows in red.

### 6.4 Risk Score by Equipment (Top Right)

**What this answers:** "Which equipment categories have the highest cumulative risk?"

| Setting | Value |
|---------|-------|
| Visual type | Clustered Column Chart |
| Axis | dim_Asset[EquipmentCategory] |
| Values | AVERAGE of Measure_RiskScore |

**Formatting:** Sort descending by average risk score.

### 6.5 Priority Recommendation Table (Bottom)

**What this answers:** "Which assets need engineering attention?"

| Setting | Value |
|---------|-------|
| Visual type | Table |
| Columns: | |
| | dim_Asset[AssetName] |
| | Measure_RiskScore |
| | Measure_PriorityLevel |
| | Measure_FailureCount |
| | Measure_TotalDowntimeHours |

**Conditional formatting on the Priority Level column:**
- P1 -> Red background
- P2 -> Amber
- P3 -> Yellow
- P4 -> Green

### 6.6 Slicers

| Slicer | Type | Field |
|--------|------|-------|
| Equipment Category | Dropdown | dim_Asset[EquipmentCategory] |
| Asset Criticality | Dropdown | dim_Asset[CriticalityRating] |

For priority filtering, use visual-level measure filters or the P1-P4 KPI cards.
Do not create a calculated column that references a measure.
### 6.7 Validation Test

| Test | Expected |
|------|----------|
| Risk scores are between 0 and 100 | Check min and max |
| At least 1 asset is P1 or P2 | Priority has spread |
| Disclaimer text is visible | Yes |

### 6.8 Screenshot

Save: `screenshots/page6_risk_matrix.png`

---

## Phase 7: Engineering Recommendations (Page 7)

### 7.1 Page Setup

Add new page -> Rename: "Engineering Recommendations" -> 1280x720 -> #FAFAFA -> Paste nav bar.

**What this page achieves:** It converts the primary 0-100 risk score into a
risk-derived recommendation list for engineering review. It is not a formal
action register.

Add this visible disclaimer near the top of the page:

```text
This is a risk-derived recommendation list. It is not a formal action register. All recommendations require engineering review and site-authorised work orders before execution.
```

### 7.2 KPI Cards

| Card | Measure | Label |
|------|---------|-------|
| 1 | Measure_HighRiskAssetCount | High-Risk Assets P1 |
| 2 | Measure_P2AssetCount | Needs Review P2 |
| 3 | Measure_P3AssetCount | Needs Monitoring P3 |
| 4 | Measure_P4AssetCount | Low-Risk Assets P4 |

These cards reuse the P1-P4 measures created in Phase 0.10. They count assets by
risk priority, not work-order status.

### 7.3 Recommendation Distribution Summary

**What this answers:** "How many assets fall into each recommendation band?"

Do not use a DAX measure as a chart axis or legend. A DAX measure cannot be used
as a standard categorical axis or legend. Use a beginner-safe summary panel or
four compact cards.

| Card | Measure | Label | Color |
|------|---------|-------|-------|
| 1 | Measure_HighRiskAssetCount | P1 Immediate Review | #EF4444 |
| 2 | Measure_P2AssetCount | P2 Needs Review | #F59E0B |
| 3 | Measure_P3AssetCount | P3 Needs Monitoring | #EAB308 |
| 4 | Measure_P4AssetCount | P4 Low Risk | #10B981 |

### 7.4 Priority Summary Panel

Create a text measure and place it in a Card visual:

```dax
Measure_PrioritySummaryText =
"Recommendation Distribution" & UNICHAR(10) &
"P1 High-Risk Assets: " & FORMAT([Measure_HighRiskAssetCount], "0") & UNICHAR(10) &
"P2 Needs Review: " & FORMAT([Measure_P2AssetCount], "0") & UNICHAR(10) &
"P3 Needs Monitoring: " & FORMAT([Measure_P3AssetCount], "0") & UNICHAR(10) &
"P4 Low-Risk Assets: " & FORMAT([Measure_P4AssetCount], "0")
```

This replaces any chart that would otherwise need a measure as a categorical axis
or legend.

### 7.5 Engineering Interpretation Panel

Create a text measure and place it in a Card visual.

```dax
Measure_InterpretationText =
VAR TopAsset =
    MAXX(
        TOPN(1, ALLSELECTED(dim_Asset), [Measure_TotalDowntimeHours], DESC),
        dim_Asset[AssetName]
    )
VAR TopDowntime =
    FORMAT(
        MAXX(
            TOPN(1, ALLSELECTED(dim_Asset), [Measure_TotalDowntimeHours], DESC),
            [Measure_TotalDowntimeHours]
        ),
        "0.0"
    )
RETURN
    "Engineering Interpretation" & UNICHAR(10) &
    "Primary bad actor: " & TopAsset & " (" & TopDowntime & " hrs downtime)" & UNICHAR(10) &
    "PM compliance: " & FORMAT([Measure_PMCompliance], "0%") & UNICHAR(10) &
    "Availability Estimate: " & FORMAT([Measure_Availability_Estimate], "0.0%") & UNICHAR(10) &
    "Repeat failures: " & FORMAT([Measure_RepeatFailureCount], "0")
```

Format this panel with a white or very light background, 4px border radius, and a
blue accent line.

### 7.6 Recommended Action Panel

Create a second text measure and place it in a Card visual.

```dax
Measure_RecommendedActionPanel =
VAR P1Count = [Measure_HighRiskAssetCount]
VAR P2Count = [Measure_P2AssetCount]
RETURN
    "Recommended Action" & UNICHAR(10) &
    IF(
        P1Count > 0,
        "Review P1 assets first and validate failure evidence before any work order is raised.",
        "No P1 assets in the current filter context. Review P2 assets for planned investigation."
    ) & UNICHAR(10) &
    "P2 assets needing review: " & FORMAT(P2Count, "0")
```

Format this panel with a green accent line. Do not present the text as approved
work instructions.

### 7.7 Asset Recommendation Table

**What this answers:** "Which assets need engineering review, and why?"

| Setting | Value |
|---------|-------|
| Visual type | Table |
| Columns: | |
| | dim_Asset[AssetName] |
| | dim_Asset[EquipmentCategory] |
| | Measure_RiskScore |
| | Measure_PriorityLevel |
| | Measure_TotalDowntimeHours |
| | Measure_RepeatFailureCount |
| | Measure_RecommendedAction |

Create the Suggested Action measure:

```dax
Measure_RecommendedAction =
VAR Score = [Measure_RiskScore]
VAR Asset = SELECTEDVALUE(dim_Asset[AssetName])
RETURN
    SWITCH(
        TRUE(),
        Score >= 60, "Immediate engineering review required for " & Asset,
        Score >= 40, "Schedule detailed failure investigation within 30 days",
        Score >= 20, "Review PM scope and frequency",
        Score >= 0, "Continue current maintenance strategy",
        "Insufficient data for recommendation"
    )
```

Rename the measure in the table visual to **Suggested Action**.

### 7.8 Conditional Formatting

Apply background color rules to the Priority Level and Suggested Action columns:
- P1 / Immediate engineering review -> #EF4444 (white text)
- P2 / detailed failure investigation -> #F59E0B (black text)
- P3 / PM scope review -> #EAB308 (black text)
- P4 / continue current strategy -> #10B981 (white text)

### 7.9 Slicers

| Slicer | Type | Field |
|--------|------|-------|
| Equipment Category | Dropdown | dim_Asset[EquipmentCategory] |
| Asset Criticality | Dropdown | dim_Asset[CriticalityRating] |

Use table filters for P1-P4 priority if needed. Avoid disconnected slicers unless
you are comfortable applying visual-level measure filters.

### 7.10 Validation Test

| Test | Expected |
|------|----------|
| Page title reads "Engineering Recommendations" | Yes |
| P1-P4 KPI cards show asset counts | Whole numbers >= 0 |
| Disclaimer is visible | Yes |
| Asset Recommendation Table includes Asset Name, Equipment Category, Risk Score, Priority Level, Total Downtime, Repeat Failure Count, Suggested Action | Yes |
| Suggested Action column shows risk-derived recommendations | Not all "Insufficient data" |

### 7.11 Screenshot

Save: `screenshots/page7_engineering_recommendations.png`

---
## Phase 8: Drill-Through Pages

### 8.1 Asset Detail Drill-Through Page

**Purpose:** Show complete reliability profile for a single asset.

**Steps:**

1. Add a new page → Rename: "Asset Detail"
2. **Important:** In the Format pane → **Drill Through** section:
   - Turn ON "Drill through from" 
   - Add `dim_Asset[AssetID]` as the drill-through field
   - Turn ON "Keep all filters"
   - The drill-through filter pane will appear on the right side
3. Hide the page (right-click → Hide Page) — this is a drill-through target, not a navigable page
4. Add a **Back button**: Insert → Buttons → Back → Action = Back

**Page content:**

| Location | Visual | Content |
|----------|--------|---------|
| Top-left | Text (DAX-driven) | Dynamic title: "Asset: [Asset Name] — Reliability Profile" |
| Top row | Card x4 | Failure Count, Total Downtime, MTTR, MTBF Estimate |
| Mid-left | Table | Failure history: Date, Mode, Duration, Cost |
| Mid-right | Gauge or Card | Overall Risk Score with color |
| Bottom | Text box | Engineering Interpretation (dynamic DAX text) |

**Dynamic title DAX:**

```dax
AssetDetail_Title =
VAR SelectedAsset = SELECTEDVALUE(dim_Asset[AssetName], "No asset selected")
VAR SelectedCategory = SELECTEDVALUE(dim_Asset[EquipmentCategory], "")
RETURN
    SelectedAsset & " — " & SelectedCategory & " — Reliability Profile"
```

Place this in a Card visual as the page header.

**Failure history table:**

| Visual type | Table |
|-------------|-------|
| Columns | fact_Failure[FailureDate], dim_FailureMode[FailureMode], fact_Failure[DowntimeHours], fact_Failure[RepairCost] |

### 8.2 Failure Mode Detail Drill-Through Page

**Purpose:** Show all assets affected by a specific failure mode.

**Steps:**

1. Add new page → Rename: "Failure Mode Detail"
2. Format pane → Drill Through → Add `dim_FailureMode[FailureModeID]`
3. Hide page

**Page content:**

| Location | Visual | Content |
|----------|--------|---------|
| Top | Text (DAX title) | "Failure Mode: [Name] — All Affected Assets" |
| Row | Card x3 | Total Occurrences, Assets Affected, Avg Downtime |
| Left | Table | Asset, Count, Total Downtime, MTTR |
| Right | Bar chart | Affected assets ranked by occurrence count |
| Bottom | Treemap | Root cause distribution |

---

## Phase 9: Tooltip Pages

### 9.1 Asset Tooltip Page

**Purpose:** Show asset mini-profile on hover in table/chart visuals.

**Steps:**

1. Add new page → Rename: "Asset Tooltip"
2. Format pane → **Page Information** → **Tooltip** → Turn ON
3. Type: Report tooltip
4. Set **Page Size** to: Tooltip (320x240 default — set to 300x200 manually)
5. Page background: #FFFFFF (white — tooltips should be clean)

**Add visuals to the tooltip page:**

| Visual | Content | Position |
|--------|---------|----------|
| Text (DAX) | Asset name (dynamic from drill-through context) | Top |
| Card (small) | Measure_FailureCount | Left |
| Card (small) | Measure_MTTR | Center |
| Card (small) | Measure_BadActorRanking | Right |
| Card (small) | Measure_RiskScore | Bottom left |
| Card (small) | Measure_PMCompliance | Bottom right |

**DAX for asset name in tooltip:**

```dax
Tooltip_AssetName =
SELECTEDVALUE(dim_Asset[AssetName], "Hover over an asset")
```

**DAX for tooltip subtitle:**

```dax
Tooltip_Subtitle =
VAR Cat = SELECTEDVALUE(dim_Asset[EquipmentCategory], "")
VAR Crit = SELECTEDVALUE(dim_Asset[CriticalityRating], "")
RETURN
    Cat & " | Criticality: " & Crit
```

**How to assign the tooltip:**

1. Go to the visual you want the tooltip on (e.g., the Bad Actor bar chart on Page 3)
2. Format pane → **Visual → Tooltips**
3. Turn ON **Report page**
4. Select **Asset Tooltip** from the dropdown

**Repeat for:** All bar charts and tables on Pages 2, 3, 4, 6 where asset names appear.

### 9.2 KPI Definition Tooltip Page

**Purpose:** Show KPI formula and interpretation on hover.

**Steps:**

1. Add new page → Rename: "KPI Definitions"
2. Turn ON as tooltip page
3. Page size: 320x250

**Add a dynamic measure that shows the KPI name + formula + interpretation:**

```dax
Tooltip_KPI_Definition =
VAR MeasureName = SELECTEDMEASURENAME()
RETURN
    SWITCH(TRUE(),
        MeasureName = "Measure_MTBF_Estimate", "Mean Time Between Failures" & UNICHAR(10) &
            "Formula: Operating Days / Failure Count" & UNICHAR(10) &
            "Illustrative project threshold: >90 days",
        MeasureName = "Measure_MTTR", "Mean Time To Repair" & UNICHAR(10) &
            "Formula: Total Repair Hours / Failure Count" & UNICHAR(10) &
            "Illustrative project threshold: <8 hours per event",
        MeasureName = "Measure_Availability_Estimate", "Operational Availability" & UNICHAR(10) &
            "Formula: MTBF Estimate / (MTBF Estimate + MTTR)" & UNICHAR(10) &
            "Illustrative project threshold: >97%",
        "Hover over a KPI card for definitions"
    )
```

**Note:** `SELECTEDMEASURENAME()` has limited support in tooltip pages. An
easier approach: place this in a Text Box on the tooltip page with generic KPI
definitions that do not change per hover.

**Simpler tooltip — static text:**

Create a measure that always shows the same KPI reference:

```dax
Tooltip_KPI_Static =
"Reliability KPIs calculated from adapted public data." & UNICHAR(10) &
"See docs/assumptions_and_limitations.md for methodology." & UNICHAR(10) &
UNICHAR(10) &
"MTBF Estimate and Availability Estimate are not auditable metrics."
```

---

## Phase 10: Final Polish and Validation

### 10.1 Sync Slicers Across Pages

If you want slicers on multiple pages to stay synchronized:

1. On the **View** tab, turn ON **Sync slicers**
2. A pane appears showing each slicer and which pages it applies to
3. For each slicer, check the boxes for pages where it should sync
4. Important: On pages where the slicer should NOT appear, leave the "Visible" box unchecked

**Simpler option for beginners:** Do not synchronize slicers. Each slicer affects
only its own page. This avoids confusing cross-page filtering behavior.

### 10.2 Edit Visual Interactions

By default, clicking any visual filters all other visuals. This is usually correct,
but sometimes you want to disable it.

1. Select a slicer visual
2. Click **Format → Edit interactions** (Format tab)
3. Icons appear above every other visual:
   - 🎯 Filter icon = this slicer filters this visual (default, usually correct)
   - 🚫 No effect = slicer does NOT affect this visual
4. For date slicers, you want ALL visuals to be filtered
5. For equipment category slicers, you want ALL visuals to be filtered
6. Click **Edit interactions** again to turn off edit mode

**Common mistake to avoid:** Do NOT disable interactions on KPI cards. KPIs must
update when slicer selections change. Disabling interactions makes KPIs show
"total" values regardless of slicers.

### 10.3 Check Filters That May Produce Misleading Totals

**The #1 beginner mistake:** A KPI card showing a number that looks correct but
is actually showing ALL data (ignoring slicer context).

**Check every visual on every page:**

1. Select the visual
2. Look at the **Filters pane** (right side)
3. Check if there are any "Visual level filters" that should not be there
4. Check if the visual is being accidentally filtered by an unrelated slicer

**Specific checks:**

| Check | Why This Matters |
|-------|-----------------|
| MTBF Estimate card on Page 1 should update when date slicer changes | It uses dim_Date through relationships |
| Any card using ALL() or ALLEXCEPT() in DAX | These override slicers — verify this is intentional |
| Drill-through target page filters | Should show only the selected asset |
| Tooltip page values | Should change based on hovered item |

**Test:**
1. Select a specific month in the date slicer
2. Note the Total Downtime value
3. Select a different month
4. The value should change

If the value does NOT change, your measure is ignoring filter context. Check
whether your DAX uses ALL() or ALLSELECTED() in a way that bypasses the slicer.

### 10.4 Page-Navigation Button Consistency

Check that all navigation buttons on all 7 pages are consistent:

| Property | Standard |
|----------|----------|
| Width | 120px |
| Height | 32px |
| Font | 10pt, Segoe UI |
| Text color | White |
| Background (inactive) | #1A1A2E |
| Background (active) | #3B82F6 (or leave all the same) |
| Border radius | 4px |
| Padding between buttons | 8px |
| Alignment | Top of page, 16px from left/right edges |

**To highlight the active page (advanced):**

1. Create a bookmark for each page (View → Bookmarks → Add)
2. Set button formatting per bookmark state
3. This is optional for V0.2 — uniform buttons are fine

### 10.5 Final Validation Walkthrough

Go through every page in order and verify:

| # | Check | Pass? |
|---|-------|-------|
| 1 | Page 1: KPI cards show numbers or valid BLANK() for unavailable estimates (no #ERROR) | ☐ |
| 2 | Page 1: Trend chart has lines visible | ☐ |
| 3 | Page 1: When you click a bad actor bar, other visuals filter | ☐ |
| 4 | Page 2: Scatter plot shows bubbles of different sizes | ☐ |
| 5 | Page 2: Table shows availability with color coding | ☐ |
| 6 | Page 3: Pareto bars sorted high to low | ☐ |
| 7 | Page 3: Heatmap has colored cells | ☐ |
| 8 | Page 4: Treemap shows root cause hierarchy | ☐ |
| 9 | Page 5: PM Compliance shows as % | ☐ |
| 10 | Page 5: Overdue table has overdue days | ☐ |
| 11 | Page 6: Risk scores between 0-100 | ☐ |
| 12 | Page 6: Disclaimer text visible | ☐ |
| 13 | Page 7: Interpretation card shows dynamic text | ☐ |
| 14 | Page 7: Suggested Action column shows recommendations | ☐ |
| 15 | Asset Detail: Drill-through works from Page 2 table | ☐ |
| 16 | Asset Detail: Shows correct asset name | ☐ |
| 17 | Asset Tooltip: Appears on hover on Page 3 bars | ☐ |
| 18 | Navigation: All 7 buttons navigate to correct pages | ☐ |
| 19 | Filters: Date slicer updates all visuals | ☐ |
| 20 | No #ERROR values anywhere; BLANK() is acceptable where source data or denominators are unavailable | ☐ |

---

## Checklist A: Complete Page-Build Checklist

Use this to track your progress through all phases.

| # | Phase | Component | Done? |
|---|-------|-----------|-------|
| 0.1 | Setup | Save .pbix file | ☐ |
| 0.2 | Setup | Verify required CSV files exist | ☐ |
| 0.3 | Setup | Import and clean dim_Asset | ☐ |
| 0.4 | Setup | Import and clean all available fact tables | ☐ |
| 0.5 | Setup | Import optional lookup tables if present | ☐ |
| 0.6 | Setup | Create and mark dim_Date in DAX | ☐ |
| 0.7 | Setup | Build 6 mandatory relationships, plus 2 conditional lookup relationships if lookup tables are loaded | ☐ |
| 0.8 | Setup | Create Measures table | ☐ |
| 0.9 | Setup | Add required calculated columns | ☐ |
| 0.10 | Setup | Create and test DAX measures, including risk and bad actor measures | ☐ |
| 1.1 | Page 1 | Page setup (1280x720, #FAFAFA) | ☐ |
| 1.2 | Page 1 | Navigation buttons (7 buttons) | ☐ |
| 1.3 | Page 1 | KPI cards (4 cards) | ☐ |
| 1.4 | Page 1 | Monthly Downtime Trend chart | ☐ |
| 1.5 | Page 1 | Availability Estimate by Category bar chart | ☐ |
| 1.6 | Page 1 | Top-5 Bad Actors bar chart | ☐ |
| 1.7 | Page 1 | KPI Comparison multi-row card | ☐ |
| 1.8 | Page 1 | Compact P1-P4 priority summary | ☐ |
| 1.9 | Page 1 | Slicers (Date + Category) | ☐ |
| 1.10 | Page 1 | Disclaimers text | ☐ |
| 2.1 | Page 2 | Page setup + nav bar | ☐ |
| 2.2 | Page 2 | KPI cards | ☐ |
| 2.3 | Page 2 | Scatter plot (MTBF Estimate vs Availability Estimate) | ☐ |
| 2.4 | Page 2 | Failure Mode Distribution (100% stacked bar) | ☐ |
| 2.5 | Page 2 | Monthly Failure Frequency (line chart) | ☐ |
| 2.6 | Page 2 | Equipment Detail Table | ☐ |
| 2.7 | Page 2 | Slicers + visual filters | ☐ |
| 3.1 | Page 3 | Page setup + nav bar | ☐ |
| 3.2 | Page 3 | KPI cards | ☐ |
| 3.3 | Page 3 | Downtime Pareto (bar + TopN filter) | ☐ |
| 3.4 | Page 3 | Bad Actor horizontal bar | ☐ |
| 3.5 | Page 3 | Failure Frequency heatmap (matrix) | ☐ |
| 3.6 | Page 3 | Repeat Failure Trend | ☐ |
| 3.7 | Page 3 | Slicers (Category, Failure Mode, Time) | ☐ |
| 4.1 | Page 4 | Page setup + nav bar | ☐ |
| 4.2 | Page 4 | KPI cards (including Most Frequent text) | ☐ |
| 4.3 | Page 4 | Failure Mode Pareto | ☐ |
| 4.4 | Page 4 | Root Cause Treemap | ☐ |
| 4.5 | Page 4 | Failure Mode by Equipment (stacked bar) | ☐ |
| 4.6 | Page 4 | Failure Trend by Mode (line chart) | ☐ |
| 4.7 | Page 4 | Slicers (Mode, Category, Year) | ☐ |
| 5.1 | Page 5 | Page setup + nav bar | ☐ |
| 5.2 | Page 5 | KPI cards + Overdue/Completed measures | ☐ |
| 5.3 | Page 5 | PM Compliance by Category bar chart | ☐ |
| 5.4 | Page 5 | PM Completion Trend (line + column) | ☐ |
| 5.5 | Page 5 | PM vs Corrective scatter plot | ☐ |
| 5.6 | Page 5 | Overdue PM Table | ☐ |
| 5.7 | Page 5 | Slicers | ☐ |
| 6.1 | Page 6 | Page setup + nav bar | ☐ |
| 6.2 | Page 6 | KPI cards (P1-P4 counts) | ☐ |
| 6.3 | Page 6 | Risk Matrix (scatter or table) | ☐ |
| 6.4 | Page 6 | Risk Score by Equipment bar chart | ☐ |
| 6.5 | Page 6 | Priority Recommendation Table | ☐ |
| 6.6 | Page 6 | Slicers + disclaimer text | ☐ |
| 7.1 | Page 7 | Page setup + nav bar | ☐ |
| 7.2 | Page 7 | KPI cards | ☐ |
| 7.3 | Page 7 | Recommendation Distribution Summary | ☐ |
| 7.4 | Page 7 | Priority Summary Panel | ☐ |
| 7.5 | Page 7 | Engineering Interpretation card (panel design) | ☐ |
| 7.6 | Page 7 | Recommended Action card (panel design) | ☐ |
| 7.7 | Page 7 | Asset Recommendation Table | ☐ |
| 7.8 | Page 7 | Conditional formatting on Suggested Action column | ☐ |
| 7.9 | Page 7 | Slicers | ☐ |
| 8.1 | Drill | Asset Detail drill-through page | ☐ |
| 8.2 | Drill | Failure Mode Detail drill-through page | ☐ |
| 9.1 | Tooltip | Asset Tooltip page (300x200) | ☐ |
| 9.2 | Tooltip | KPI Definitions tooltip page | ☐ |
| 10.1 | Polish | Sync slicers (or decide not to) | ☐ |
| 10.2 | Polish | Visual interactions verified | ☐ |
| 10.3 | Polish | Filter context verified | ☐ |
| 10.4 | Polish | Navigation buttons consistent | ☐ |
| 10.5 | Polish | Final validation walkthrough | ☐ |
| 12 | Docs | 7 screenshots saved to screenshots/ | ☐ |

---

## Checklist B: DAX Validation Checklist

| # | Measure | Test | Expected Value | Actual |
|---|---------|------|----------------|--------|
| 1 | Measure_TotalDowntimeHours | Card visual | Positive number (e.g., 1245.5) | ☐ |
| 2 | Measure_FailureCount | Card visual | Integer > 0 (e.g., 87) | ☐ |
| 3 | Measure_TotalRepairHours | Card visual | ~80% of TotalDowntimeHours | ☐ |
| 4 | Measure_AvgRepairTime | Card visual | TotalRepair / FailureCount, or BLANK() if no failures | ☐ |
| 5 | Measure_MTTR | Card visual | Same as AvgRepairTime | ☐ |
| 6 | Measure_MTBF_Estimate | Card visual | Numeric estimate, or BLANK() if no failures/observation denominator | ☐ |
| 7 | Measure_Availability_Estimate | Card visual | 0.0 - 1.0, or BLANK() if MTBF/MTTR unavailable | ☐ |
| 8 | Measure_PMCompliance | Card visual | 0.0 - 1.0, or BLANK() if no valid scheduled PMs | ☐ |
| 9 | Measure_RepeatFailureCount | Card visual | < FailureCount | ☐ |
| 10 | Measure_CorrectiveToPreventiveRatio | Card visual | Number, or BLANK() if no preventive work exists | ☐ |
| 11 | Measure_MaintenanceCost | Card visual | Number or 0 when zero cost is valid | ☐ |
| 12 | Measure_CostPerDowntimeHour | Card visual | Cost / Downtime, or BLANK() if downtime/cost data unavailable | ☐ |
| 13 | Measure_RiskScore | Table with assets | 0-100 range, varies per asset | ☐ |
| 14 | Measure_PriorityLevel | Table with assets | P1/P2/P3/P4 | ☐ |
| 15 | Measure_BadActorRanking | Table with assets | 1 = worst actor | ☐ |
| 16 | Measure_HighRiskAssetCount | Card visual | Integer >= 0 | ☐ |
| 17 | Measure_DowntimeChange | Card visual | % positive/negative, or BLANK() if no prior period exists | ☐ |
| 18 | Measure_LikelihoodScore | Table with assets | 1-5 | ☐ |
| 19 | Measure_ConsequenceScore_5x5 | Table with assets | 1-5 | ☐ |

**DAX Troubleshooting Reference:**

| Error | Most Likely Cause | Fix |
|-------|------------------|-----|
| "#ERROR" in card | Measure references a nonexistent column | Check spelling of all column names |
| Blank card | May be valid missing data, or filter context eliminates all rows | Check denominator/source data first, then relationships |
| "Cannot find table" | Table name is wrong | Check exact table name in Fields pane |
| "Circular dependency" | Measure A references Measure B that references A | Trace the chain, break the circle |
| Wrong number (way too large) | Measure is summing ALL data, ignoring filters | Check for ALL() in CALCULATE that should not be there |
| Wrong number (way too small) | Measure is being filtered by unrelated slicer | Check visual interactions |
| Division by zero error | DIVIDE denominator = 0 | Use DIVIDE(numerator, denominator, BLANK()) for unavailable ratios |
| Time intelligence blank | dim_Date not marked as date table | Mark as date table (Step 0.6) |

---

## Checklist C: Data-Quality Checklist

| # | Check | How to Verify | Pass? |
|---|-------|---------------|-------|
| 1 | No null primary keys | Table view → EventID column — any blanks? | ☐ |
| 2 | DowntimeHours >= 0 | Column distribution → check min value | ☐ |
| 3 | Failure dates in chronological order | Table view → sort by FailureDate ascending | ☐ |
| 4 | No duplicate EventIDs | Column profile → distinct vs unique count match | ☐ |
| 5 | Asset names are standardised | Table view → check for "CMP-001" vs "Compressor 1" | ☐ |
| 6 | Failure modes are standardised | Table view → check "Bearing" vs "bearing" vs "Bearings" | ☐ |
| 7 | Equipment categories match dim table | Related table check in Model view | ☐ |
| 8 | PM completion dates not in the future | MAX(PMCompletedDate) < TODAY() + 1 | ☐ |
| 9 | Fact table row counts make sense | fact_Failure = 50-500 rows (depending on data) | ☐ |
| 10 | Six mandatory relationships are 1:* single direction; optional lookup relationships are present only if lookup tables are loaded | Model view inspection | ☐ |

---

## Checklist D: Visual-Consistency Checklist

| # | Check | Standard | Pass? |
|---|-------|----------|-------|
| 1 | Page dimensions | All 1280x720 | ☐ |
| 2 | Page background | All #FAFAFA | ☐ |
| 3 | KPI card layout | 4 cards per row, uniform width | ☐ |
| 4 | KPI card font | 28pt Bold #1A1A2E | ☐ |
| 5 | KPI label font | 10pt #666666 (text boxes) | ☐ |
| 6 | Visual titles | 11pt Semibold, include time context | ☐ |
| 7 | Navigation buttons | All 7 visible on every page | ☐ |
| 8 | No pure black (#000000) text | Check all font colors | ☐ |
| 9 | Color meanings consistent | Green=good, Red=bad everywhere | ☐ |
| 10 | Red/green distinction with text | Not color-only — verify labels present | ☐ |
| 11 | Visual shadows | Small preset, consistent | ☐ |
| 12 | Table headers | #1A1A2E background, white text | ☐ |
| 13 | Drill-through pages hidden | Hidden (right-click → Hide) | ☐ |
| 14 | Tooltip pages set as tooltip type | Format → Page Info → Tooltip = ON | ☐ |
| 15 | Disclaimer on Risk page | Red-bordered text box | ☐ |
| 16 | Data labels on charts | Consistent position (outside end) | ☐ |
| 17 | No decorative-only visuals | No gauge, radar, word cloud | ☐ |
| 18 | Grid alignment | Visuals snap to 1px grid, edges aligned | ☐ |

---

## Your First Actions in Power BI

### The Exact First Page to Build

**Build Page 1 (Executive Overview) first.** Here's why:
- It uses the most basic measures (total downtime, failure count)
- It gives you immediate feedback that relationships and filters work
- It's the landing page — getting this right builds confidence
- Bad actor and Pareto (Pages 2-3) depend on measures you prove on Page 1

### The Exact First Actions

Open Power BI Desktop. In this exact order:

1. **File -> Save As** -> `lng_reliability_dashboard_v0.2.pbix`
2. Verify the required CSV files exist in `data/processed/`
3. Import and clean `asset_register.csv`; rename the query to `dim_Asset`
4. Import and clean all available fact tables: `fact_Failure`, `fact_Maintenance`, `fact_PM_Compliance`
5. Import optional lookup tables only if present: `dim_FailureMode`, `dim_MaintenanceAction`
6. Create and mark `dim_Date`
7. Build relationships in Model view
8. Create the `Measures` table with `Measures = ROW("Placeholder", "Measures go here")` and hide `Measures[Placeholder]`
9. Create calculated columns only where required
10. Create and test DAX measures
11. Build Page 1 (Executive Overview)
12. Continue with remaining pages

**Never create a measure before its referenced table exists.**

---

*End of Beginner Build Guide*
*Built for Power BI Desktop (free version, November 2023+)*
