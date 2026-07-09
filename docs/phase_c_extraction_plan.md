# Phase C: Data Extraction & Inspection Plan

**Target:** Extract all 4 ZIP files, inspect contents, understand structure, and prepare for cleaning.

**Skill Level:** Beginner — every step uses Windows File Explorer or simple commands you can run in Git Bash.

**Duration:** 1–2 hours for a beginner working carefully.

---

## 1. WHICH DATASET TO INSPECT FIRST — AND WHY

Open the datasets in this exact order:

| Order | Dataset | Why This First |
|-------|---------|----------------|
| **1st** | **Azure PdM** (31 MB ZIP) | Smallest. Easiest to understand. 5 clean CSV tables with clear column names. You will get a "quick win" and learn the inspection pattern here before tackling larger files. |
| **2nd** | **PHMSA LNG** (449 KB ZIP) | Tiny (only ~51 rows). Directly relevant to LNG facilities. Uses tab-separated format — you'll learn how PHMSA structures data. |
| **3rd** | **PHMSA Gas Transmission** (2.2 MB ZIP) | Medium size (~2,025 rows). Same format as LNG data but much richer. This is the "main" reliability dataset for pipeline risk analysis. |
| **4th** | **MetroPT-3** (209 MB ZIP) | Largest. 1.5 million rows of sensor data. Inspect LAST because it requires resampling strategy before you can work with it comfortably. |

**Golden rule:** If Excel crashes or hangs, that dataset is too big for Excel — skip to Python inspection for that file.

---

## 2. WHAT'S INSIDE EACH ZIP

### 2.1 Azure Predictive Maintenance (`azure_predictive_maintenance_dataset.zip` — 31 MB)

| File Inside ZIP | Rows | Columns | Description |
|-----------------|------|---------|-------------|
| `PdM_telemetry.csv` | 876,100 | 6 | Hourly sensor readings: datetime, machineID, volt, rotate, pressure, vibration |
| `PdM_errors.csv` | 3,919 | 3 | Error events: datetime, machineID, errorID (error1–error5) |
| `PdM_failures.csv` | 761 | 3 | Failure events: datetime, machineID, failure (comp1–comp4) |
| `PdM_maint.csv` | 3,286 | 3 | Maintenance actions: datetime, machineID, comp (comp1–comp4 = component replaced) |
| `PdM_machines.csv` | 100 | 3 | Machine catalog: machineID, model (model1–model4), age (years) |

**Key insight:** These 5 tables JOIN together on `machineID` and `datetime`. This is a relational dataset — like a mini database. The telemetry table is ~80 MB when extracted.

### 2.2 PHMSA LNG Incidents (`phmsa_lng_incident_data_2011_present.zip` — 449 KB)

| File Inside ZIP | Rows | Columns | Description |
|-----------------|------|---------|-------------|
| `incident_liquefied_natural_gas_jan2011_present.txt` | ~51 | 211 | Tab-separated. One row per LNG facility incident (2011–present). Contains cause codes, costs, facility details, narrative. |
| `Liquefied Natrual Gas Incident PHMSA F7100.3 Rev 9-2023 Data fields.pdf` | — | — | PDF codebook explaining all 211 column names |

**Key insight:** The file is `.txt` but uses TAB characters between columns — NOT commas. You cannot open this directly in Excel without importing properly.

### 2.3 PHMSA Gas Transmission Incidents (`phmsa_gas_transmission_incident_data_2010_present.zip` — 2.2 MB)

| File Inside ZIP | Rows | Columns | Description |
|-----------------|------|---------|-------------|
| `incident_gas_transmission_gathering_jan2010_present.txt` | ~2,025 | 624 | Tab-separated. One row per gas transmission incident (2010–present). Very rich: pipe specs, corrosion data, inspection history, excavation details, costs. |
| `Gas Transmission and Gathering Incident PHMSA F7100.2 Rev 9-2023 Data fields.pdf` | — | — | PDF codebook explaining all 624 column names |

**Key insight:** 624 columns means most columns are empty for any given incident. You will select only ~10–15 relevant columns during cleaning. Do NOT try to keep all 624.

### 2.4 MetroPT-3 Compressor (`metropt+3+dataset.zip` — 209 MB)

| File Inside ZIP | Rows | Columns | Description |
|-----------------|------|---------|-------------|
| `MetroPT3(AirCompressor).csv` | 1,516,948 | 17 | 1-second resolution sensor data from an industrial air compressor (Feb–May 2020). Columns: timestamp, TP2, TP3, H1, DV_pressure, Reservoirs, Oil_temperature, Motor_current, COMP, DV_eletric, Towers, MPG, LPS, Pressure_switch, Oil_level, Caudal_impulses |
| `Data Description_Metro.pdf` | — | — | PDF explaining sensor meanings and known fault periods |

**Key insight:** 1.5 million rows at 1-second resolution is ~17.5 days of continuous data. You will resample to 1-minute averages before doing anything — that shrinks it from 1.5M to ~25,000 rows. The extracted CSV is ~218 MB — Excel CANNOT open this.

---

## 3. EXACT FOLDER STRUCTURE FOR EXTRACTED FILES

Here is the exact folder structure to create. Paths shown from your project root (`~/projects/lng-reliability-dashboard`).

```
data/
├── raw/                                    # ALL RAW FILES (entire folder in .gitignore)
│   │
│   ├── phmsa_lng_incident_data_2011_present.zip    # Keep ZIP as record
│   ├── phmsa_gas_transmission_incident_data_2010_present.zip
│   ├── metropt+3+dataset.zip
│   ├── azure_predictive_maintenance_dataset.zip
│   │
│   ├── extracted/                          # NEW: extraction target
│   │   ├── phmsa_lng/
│   │   │   ├── incident_liquefied_natural_gas_jan2011_present.txt
│   │   │   └── phmsa_lng_codebook.pdf
│   │   │
│   │   ├── phmsa_gas_transmission/
│   │   │   ├── incident_gas_transmission_gathering_jan2010_present.txt
│   │   │   └── phmsa_gas_transmission_codebook.pdf
│   │   │
│   │   ├── metropt3/
│   │   │   ├── MetroPT3_AirCompressor.csv          # RENAMED: parentheses removed
│   │   │   └── metropt3_data_description.pdf
│   │   │
│   │   └── azure_pdm/
│   │       ├── PdM_telemetry.csv
│   │       ├── PdM_errors.csv
│   │       ├── PdM_failures.csv
│   │       ├── PdM_maint.csv
│   │       └── PdM_machines.csv
│   │
│   └── README.md                          # Already exists
│
├── processed/                              # Cleaned data (COMMITTED to GitHub)
│   ├── asset_register.csv
│   ├── downtime_log.csv
│   ├── failure_summary.csv
│   ├── compressor_health.csv
│   ├── pipeline_risk_scores.csv
│   └── reliability_kpis.csv
│
└── samples/                                # NEW: small GitHub-safe samples
    ├── phmsa_lng_sample_5rows.csv          # First 5 rows, key columns only
    ├── phmsa_gas_transmission_sample_5rows.csv
    ├── metropt3_sample_1hour.csv           # 1 hour of 1-minute resampled data
    └── azure_pdm_sample_machines.csv       # Full machines table (only 100 rows)
```

**Why the `samples/` folder:** Reviewers on GitHub cannot see your raw data (it's not committed). The sample files let them understand data structure without downloading 250 MB of ZIPs. They also prove you actually downloaded and inspected the data.

---

## 4. WHAT SMALL SAMPLE FILES TO CREATE FOR GITHUB

| Sample File | Content | Safe for GitHub? | Size |
|-------------|---------|------------------|------|
| `samples/phmsa_lng_sample_5rows.csv` | First 5 rows of LNG incidents, with only 15 key columns | Yes — tiny | ~3 KB |
| `samples/phmsa_gas_transmission_sample_5rows.csv` | First 5 rows of gas transmission incidents, only 15 key columns | Yes — tiny | ~3 KB |
| `samples/metropt3_sample_1hour.csv` | 60 rows (1-minute resampled, 1 hour of data), all 17 columns | Yes — tiny | ~5 KB |
| `samples/azure_pdm_sample_machines.csv` | Full machines table (100 rows public data) | Yes — tiny | ~2 KB |
| `samples/azure_pdm_sample_telemetry.csv` | First 100 rows of telemetry (1 machine, ~4 days) | Yes — tiny | ~8 KB |
| `samples/README.md` | Explains what each sample is and links to original source | Yes | ~1 KB |

**Never commit:**
- Any ZIP file
- Any extracted TXT/CSV from `data/raw/extracted/`
- The full MetroPT-3 CSV (218 MB)
- The full Azure telemetry CSV (80 MB)

---

## 5. INSPECTION STEPS (WHAT TO DO WITH EACH DATASET)

### Step 1: AZURE PdM (Quick Win — Do This First)

**In Excel:**
1. Open `data/raw/extracted/azure_pdm/PdM_machines.csv` — only 100 rows, opens instantly
2. Look at the columns: `machineID`, `model`, `age`
3. Open `data/raw/extracted/azure_pdm/PdM_failures.csv` — small, 761 rows
4. Notice failures reference `comp1` through `comp4` — these are component types
5. Open `data/raw/extracted/azure_pdm/PdM_errors.csv` — 3,919 rows
6. Open `data/raw/extracted/azure_pdm/PdM_maint.csv` — 3,286 rows

**Skip in Excel, inspect with Python:**
- `PdM_telemetry.csv` — 876,100 rows will crash Excel. Use Python.

**Questions to answer:**
- How many unique machines are there? (Answer: 100)
- What are the 4 component types in failures/maint? (comp1, comp2, comp3, comp4)
- What date range does the data cover? (2015 full year)

### Step 2: PHMSA LNG (Small, Directly LNG-Relevant)

**In Excel (using Import, NOT double-click):**
1. Open Excel
2. Data tab → From Text/CSV → select `incident_liquefied_natural_gas_jan2011_present.txt`
3. Set delimiter to **Tab** (NOT comma)
4. File origin: 65001 (Unicode UTF-8)
5. You will see ~51 rows and 211 columns — overwhelming. Scroll right slowly.

**Key columns to locate (use Find / Ctrl+F):**
- `REPORT_RECEIVED_DATE` — when the incident was reported
- `NAME` — operator company name
- `FACILITY_NAME` — LNG facility name
- `CAUSE` — root cause category (e.g., INCORRECT OPERATION, EQUIPMENT FAILURE, MATERIAL FAILURE)
- `CAUSE_DETAILS` — more specific cause description
- `COMMODITY_RELEASED_TYPE` — what was released (NATURAL GAS, REFRIGERANT GAS, etc.)
- `UNINTENTIONAL_RELEASE` — volume released unintentionally
- `FATALITY_IND` — were there fatalities?
- `INJURY_IND` — were there injuries?
- `EST_COST_OPER_PAID` — operator cost
- `EST_COST_PROP_DAMAGE` — property damage cost
- `PRPTY` — total cost
- `NARRATIVE` — rich text narrative of what happened (very useful for LLM analysis)

**Questions to answer:**
- What are the most common CAUSE values? (Read a few rows)
- What date range does the data cover? (Look at REPORT_RECEIVED_DATE)
- What LNG facility types appear? (BASE LOAD, PEAK SHAVE, SATELLITE)

### Step 3: PHMSA Gas Transmission (Richer, Medium Size)

**Same import method as LNG data:**
1. Excel → Data tab → From Text/CSV
2. Select `incident_gas_transmission_gathering_jan2010_present.txt`
3. Delimiter: **Tab**, File origin: 65001
4. ~2,025 rows, 624 columns — even more overwhelming

**Key columns (same pattern + a few extras):**
- Same date, name, cause columns as LNG data
- `PIPE_DIAMETER` — pipe size in inches
- `PIPE_WALL_THICKNESS` — wall thickness
- `INSTALLATION_YEAR` — when pipe was installed (some from 1930s!)
- `LOCATION_TYPE` — CLASS 1 through CLASS 4 location
- `ONSHORE_STATE_ABBREVIATION` — U.S. state (not relevant for PNG, but shows geography)
- `CAUSE` and `CAUSE_DETAILS` — same structure as LNG
- `NARRATIVE` — detailed incident description

**Questions to answer:**
- What installation years appear? (Range: 1930 to present — this is aging infrastructure data)
- What are the most common CAUSE codes?
- How many incidents involve pipe from before 1970?

### Step 4: MetroPT-3 (Large — Inspect in Python)

**Do NOT open in Excel.** It will freeze your laptop.

**Instead, use the MetroPT-3 inspection script or a quick Python peek:**
- 1,516,948 rows × 17 columns
- Timestamp every 10 seconds from Feb–May 2020
- Sensor columns: pressure, temperature, vibration, motor current, RPM-related

**Quick peek in Git Bash (cheat command):**
```bash
head -20 data/raw/extracted/metropt3/MetroPT3_AirCompressor.csv
```

**Questions to answer:**
- What are the 17 column names?
- What date range does it cover? (Feb 1 – May 31, 2020)
- What is the sampling interval? (10 seconds = 0.1 Hz, not 1 Hz as initially estimated)

---

## 6. RELIABILITY DASHBOARD TABLES TO PRODUCE FIRST

The architecture plan already defines 6 processed tables. Here is the recommended production ORDER with reasoning:

| Priority | Table | Source Dataset | Why First |
|----------|-------|----------------|-----------|
| **1st** | `asset_register.csv` | All 3 (mapped) | Foundation — every other table references asset_id. Build the asset taxonomy FIRST. |
| **2nd** | `downtime_log.csv` | Azure PdM (failures + maint) | Direct downtime events — required for all KPI calculations. |
| **3rd** | `failure_summary.csv` | Azure PdM (failures + errors) | Aggregated from downtime_log — shows failure patterns. |
| **4th** | `pipeline_risk_scores.csv` | PHMSA Gas Transmission | Independent of asset/downtime pipeline. Can be built in parallel. |
| **5th** | `compressor_health.csv` | MetroPT-3 (resampled) | Largest processing task — do after you're comfortable with pandas. |
| **6th** | `reliability_kpis.csv` | All above (computed) | Final aggregation — requires all other tables first. |

**Chart-ready output from these tables:**
- Downtime hours by equipment category (bar chart)
- Pareto of failure causes
- Compressor vibration trend with threshold bands
- Pipeline root cause distribution
- Maintenance priority matrix (likelihood × consequence)
- MTTR / MTBF / Availability summary cards

---

## 7. WHAT CAN BE DONE IN EXCEL BEFORE PYTHON

You can do a LOT of learning and inspection in Excel before writing a single line of Python. This is a legitimate engineering workflow — use the right tool for the job.

| Task | Tool | Notes |
|------|------|-------|
| Open and visually inspect small CSVs | Excel | Azure PdM machines, failures, errors, maint |
| Import tab-separated PHMSA files | Excel Data → From Text/CSV | Set delimiter to Tab |
| Browse column names in PHMSA codebook PDFs | Any PDF reader | Understand what each field means |
| Filter PHMSA data to see cause distribution | Excel AutoFilter | Click CAUSE column → filter |
| Count LNG facility types | Excel PivotTable | Rows: FACILITY_TYPE_BASE_LOAD_IND |
| Write the initial asset_register.csv | Excel | Create a blank CSV with columns: asset_id, asset_name, lng_category, subsystem, criticality, source_dataset. Fill in rows yourself based on the architecture plan's mapping table (Appendix A). |
| Take screenshots of data structure | Snipping Tool | Save to `screenshots/` for portfolio |
| Read PHMSA incident narratives | Excel (scroll to NARRATIVE column) | Rich text descriptions — great for understanding root causes |

**What MUST be done in Python (Excel cannot handle):**
- Reading MetroPT-3 (1.5M rows — too large)
- Reading Azure telemetry (876K rows — too large)
- Merging/joining tables across datasets
- Resampling time-series data
- Computing reliability KPIs (MTTR, MTBF, Availability)
- Generating formatted matplotlib/seaborn charts

---

## 8. RISKS WITH LARGE FILES AND HOW TO AVOID GITHUB PROBLEMS

### Risk 1: Accidentally committing raw data to GitHub

**Problem:** `git add .` without a good `.gitignore` will try to stage 250 MB of ZIP files and extracted CSVs. GitHub rejects pushes > 100 MB per file, and your repo becomes bloated.

**Prevention (already in place):**
Your `.gitignore` already has:
```
data/raw/*.zip
data/raw/*.csv
data/raw/*.xlsx
data/raw/extracted/
data/raw/**/extracted/
data/raw/**/*.csv
```

**Before every commit, run:**
```bash
git status
```
Make sure no files under `data/raw/` or `data/raw/extracted/` appear in "Changes to be committed."

### Risk 2: Excel crashing on large files

**Problem:** MetroPT-3 (1.5M rows) and Azure telemetry (876K rows) exceed Excel's ~1,048,576 row limit or will hang your laptop.

**Prevention:**
- Never double-click these files
- Use Python (pandas) for any file > 50 MB
- Use the `head` command in Git Bash for a quick peek:
  ```bash
  head -20 data/raw/extracted/metropt3/MetroPT3_AirCompressor.csv
  ```

### Risk 3: Running out of disk space

**Problem:** Extracting all ZIPs takes ~250 MB. MetroPT-3 CSV alone is 218 MB. If your laptop is low on disk, this matters.

**Mitigation:**
- Keep ZIPs (they're compressed) — only extract when actively working
- After extracting MetroPT-3, the ZIP + extracted CSV together = ~427 MB
- You can delete the extracted CSV after producing the processed `compressor_health.csv` (which is only ~2 MB resampled)

### Risk 4: MetroPT-3 parentheses in filename

**Problem:** The filename `MetroPT3(AirCompressor).csv` contains parentheses which cause issues in shell commands (bash interprets them as subshell syntax).

**Mitigation:**
- Rename during extraction to `MetroPT3_AirCompressor.csv`
- Always quote filenames with special chars: `"MetroPT3(AirCompressor).csv"`

### Risk 5: PHMSA files are tab-separated, not CSV

**Problem:** Double-clicking a `.txt` tab-separated file opens it in Notepad (messy) or Excel (wrong parsing).

**Mitigation:**
- Always use Excel's Data → From Text/CSV import with Tab delimiter
- OR copy to `.tsv` extension (tab-separated values) for clarity
- Python `pd.read_csv(file, sep='\t')` handles this correctly

---

## 9. YOUR NEXT 5 EXACT ACTIONS

Do these in order. Each action takes 5–15 minutes.

### Action 1: CREATE THE EXTRACTION FOLDERS

Open Git Bash at your project root and run:

```bash
mkdir -p data/raw/extracted/phmsa_lng
mkdir -p data/raw/extracted/phmsa_gas_transmission
mkdir -p data/raw/extracted/metropt3
mkdir -p data/raw/extracted/azure_pdm
mkdir -p samples
```

**Verify:** Open File Explorer, navigate to `C:\Users\22301295SATA\projects\lng-reliability-dashboard\data\raw\extracted\` — you should see 4 empty subfolders.

### Action 2: EXTRACT ALL 4 ZIP FILES

Run these 4 commands in Git Bash (one at a time):

```bash
# Extract Azure PdM (easiest)
unzip "data/raw/azure_predictive_maintenance_dataset.zip" -d "data/raw/extracted/azure_pdm/"

# Extract PHMSA LNG
unzip "data/raw/phmsa_lng_incident_data_2011_present.zip" -d "data/raw/extracted/phmsa_lng/"
mv "data/raw/extracted/phmsa_lng/Liquefied Natrual Gas Incident PHMSA F7100.3 Rev 9-2023 Data fields.pdf" "data/raw/extracted/phmsa_lng/phmsa_lng_codebook.pdf"

# Extract PHMSA Gas Transmission
unzip "data/raw/phmsa_gas_transmission_incident_data_2010_present.zip" -d "data/raw/extracted/phmsa_gas_transmission/"
mv "data/raw/extracted/phmsa_gas_transmission/Gas Transmission and Gathering Incident PHMSA F7100.2 Rev 9-2023 Data fields.pdf" "data/raw/extracted/phmsa_gas_transmission/phmsa_gas_transmission_codebook.pdf"

# Extract MetroPT-3 (largest — takes ~30 seconds)
unzip "data/raw/metropt+3+dataset.zip" -d "data/raw/extracted/metropt3/"
mv "data/raw/extracted/metropt3/MetroPT3(AirCompressor).csv" "data/raw/extracted/metropt3/MetroPT3_AirCompressor.csv"
mv "data/raw/extracted/metropt3/Data Description_Metro.pdf" "data/raw/extracted/metropt3/metropt3_data_description.pdf"
```

**Verify:** Run `ls data/raw/extracted/*/` — each folder should contain files.

### Action 3: OPEN Azure PdM IN EXCEL (FIRST INSPECTION)

1. Open Windows File Explorer
2. Navigate to `data\raw\extracted\azure_pdm\`
3. **Double-click `PdM_machines.csv`** — opens in Excel instantly (100 rows)
4. Observe: 3 columns, 100 machines, ages range ~0–20 years
5. **Double-click `PdM_failures.csv`** — 761 rows of failure events
6. **Double-click `PdM_errors.csv`** — 3,919 rows of error events
7. **Double-click `PdM_maint.csv`** — 3,286 rows of maintenance actions
8. **DO NOT double-click `PdM_telemetry.csv`** — it will hang Excel (876K rows)

**Deliverable:** Take a screenshot of `PdM_machines.csv` open in Excel, save to `screenshots/azure_pdm_machines_preview.png`.

### Action 4: IMPORT PHMSA LNG DATA PROPERLY INTO EXCEL

1. Open Excel (blank workbook)
2. Click **Data** tab in the ribbon
3. Click **From Text/CSV** (left side of Data ribbon)
4. Navigate to `data\raw\extracted\phmsa_lng\`
5. Select `incident_liquefied_natural_gas_jan2011_present.txt`
6. In the preview window:
   - Set **Delimiter** to **Tab** (NOT comma)
   - Set **File Origin** to `65001: Unicode (UTF-8)`
7. Click **Load**
8. You should see ~51 rows and 211 columns
9. Scroll to find the `CAUSE`, `NARRATIVE`, and `FACILITY_NAME` columns
10. Read 2–3 narrative descriptions to understand what incidents look like

**Deliverable:** Take a screenshot of the Excel window showing the CAUSE and FACILITY_NAME columns. Save to `screenshots/phmsa_lng_inspection.png`.

### Action 5: VERIFY GIT IGNORE IS WORKING

Before you continue working, verify that Git will NOT try to commit your raw data:

```bash
git status
```

You should see:
- `data/raw/extracted/` does NOT appear in the output (it's gitignored)
- `data/raw/*.zip` does NOT appear (they're gitignored)
- If you see any raw files listed, STOP and tell me — we need to fix `.gitignore`

Then create the samples folder README:

```bash
echo "# Data Samples

These are small extracts from the public datasets used in this project.
Full datasets are NOT committed to GitHub — see docs/data_sources.md for download instructions.

| Sample | Source Dataset | Rows | Description |
|--------|---------------|------|-------------|
| phmsa_lng_sample_5rows.csv | PHMSA LNG Incidents | 5 | First 5 incidents with key columns |
| phmsa_gas_transmission_sample_5rows.csv | PHMSA Gas Transmission | 5 | First 5 incidents with key columns |
| metropt3_sample_1hour.csv | MetroPT-3 | 60 | 1 hour of 1-minute resampled sensor data |
| azure_pdm_sample_machines.csv | Azure PdM | 100 | Full machine catalog |
| azure_pdm_sample_telemetry.csv | Azure PdM | 100 | First 100 telemetry readings |" > samples/README.md
```

---

## SUMMARY: PHASE C CHECKLIST

- [ ] Action 1: Created 4 extraction subfolders
- [ ] Action 2: Extracted all 4 ZIPs, renamed files with special chars
- [ ] Action 3: Opened Azure PdM CSVs in Excel (first look)
- [ ] Action 4: Imported PHMSA LNG data properly with Tab delimiter
- [ ] Action 5: Verified `git status` shows raw data is ignored
- [ ] Screenshots saved to `screenshots/` folder
- [ ] `samples/README.md` created

**After completing these 5 actions, you are ready for Phase D (Python cleaning).**
Come back to Hermes and say: "Phase C complete. Ready for Python data cleaning."

---

## KEY LESSONS LEARNED DURING INSPECTION

1. **PHMSA data is tab-separated, not comma-separated.** Always use `sep='\t'` in pandas.
2. **PHMSA files have hundreds of columns.** For the dashboard, you only need ~15. Selecting the right 15 is the core data-cleaning judgment.
3. **MetroPT-3 sampling is every 10 seconds, not 1 second.** That means 1,516,948 rows = ~17.5 days of data at 0.1 Hz.
4. **Azure PdM is a 5-table relational dataset.** You MUST join on `machineID` and `datetime` to connect failures to telemetry and maintenance.
5. **The narrative field in PHMSA data is gold.** It contains detailed engineering descriptions of what failed and why. This is what the LLM (09_ai_recommendations.ipynb) will analyze.
6. **Not all data is LNG-relevant.** PHMSA Gas Transmission covers all U.S. gas pipelines. You will filter to incidents with relevant cause types and pipe characteristics.

---

*Plan created: July 2026. This is your Phase C workbook — follow it step by step, check off each box, and ask Hermes for help at any point.*
