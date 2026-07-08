# Assumptions and Limitations

This document is the **honesty file** for the project. It exists so that:

1. The candidate can speak to this project with integrity in interviews
2. Reviewers understand exactly what is real vs. adapted
3. Future contributors know the boundaries of the data

---

## Core Assumptions

### A1: Equipment Category Mapping

**What we did:** Mapped public dataset equipment to LNG equipment categories.
**Why it's reasonable:** The sensor types, failure modes, and maintenance patterns are
similar between industrial air compressors and LNG refrigerant compressors.
**What we didn't do:** Claim these are real LNG compressors or real LNG operating data.

### A2: Operating Hours

**What we assumed:** 24/7 continuous operation (standard for LNG baseload plants).
**Why it's reasonable:** LNG plants operate >360 days/year with planned shutdowns every
2–4 years.
**What we didn't do:** Account for actual planned shutdown windows — the public datasets
don't distinguish planned vs. unplanned downtime.

### A3: Failure Mode Mapping

**What we did:** Interpreted Azure PdM error codes and MetroPT-3 fault labels as
common LNG equipment failure modes.
**Why it's reasonable:** Bearing failures, seal leaks, overheating, and vibration are
universal rotating equipment failure modes.
**What we didn't do:** Validate failure mode labels against actual LNG equipment failure
data.

### A4: MTBF and Availability Estimation

**What we did:** Computed MTBF and Availability from available timestamps.
**Why it's labeled "estimate":** Public datasets lack precise operating hour counters
and don't distinguish planned vs. unplanned downtime. True MTBF requires accurate
operating hours and true failure-event definitions.
**What we didn't do:** Present these as auditable reliability metrics. They are
illustrative.

### A5: Mechanical Integrity Data

**What we did:** Created illustrative inspection data (wall thickness, corrosion rate,
next inspection date) for the asset register.
**Why this is honest:** The table structure and decision logic (satisfactory/monitor/action)
is realistic, but the numbers are adapted, not from real equipment.
**What we didn't do:** Claim these come from real UT thickness measurements.

### A6: AI Engineering Recommendations

**What we did:** Fed top failure modes + context to an LLM (Claude Sonnet 4 via OpenRouter)
and asked for engineering commentary.
**Why this is honest:** The LLM output is clearly labeled as AI-generated with a review
caveat. The LLM has general engineering knowledge but no access to real LNG data.
**What we didn't do:** Present AI output as expert engineering analysis.

---

## Known Limitations

### L1: MetroPT-3 is an Air Compressor, Not a Refrigerant Compressor

| Aspect | Air Compressor | LNG Refrigerant Compressor |
|--------|---------------|---------------------------|
| Working fluid | Air (ideal gas) | Propane/MR (real gas, phase change) |
| Operating pressure | ~8–10 bar | 1–40+ bar |
| Operating temperature | Ambient to ~100°C | -40°C to +120°C |
| Speed | Fixed or VSD | Typically gas turbine or motor driven |
| Seal type | Labyrinth | Dry gas or oil film seals |

**Impact:** Absolute sensor values (temperature, pressure) will differ from real LNG
compressor values. The trend patterns and anomaly detection methodology are still valid.

### L2: PHMSA Data is U.S. Regulatory Data, Not PNG

**Impact:** Geographic, regulatory, and operational context differs. However, the root
cause categories (corrosion, equipment failure, excavation damage, operational error)
are universal pipeline risks.

### L3: Small Asset Sample Size

**Impact:** With 20–30 mapped assets and ~1 year of data (Azure PdM), statistical
conclusions about failure rates have limited confidence. Presented as illustrative,
not statistically validated.

### L4: No Process Data Integration

**Impact:** A real Operations Technical engineer works with process data (flow rates,
compositions, pressures, temperatures across the entire plant). This project has no
process simulation and no heat-and-material balance context. This is a V2 addition
candidate.

### L5: No CMMS Integration

**Impact:** Real maintenance planning uses a CMMS (Computerized Maintenance Management
System) like SAP PM or Maximo. This project simulates work order logic in Python but
does not integrate with any CMMS.

---

## What This Project is NOT

1. **NOT** a real LNG plant reliability analysis
2. **NOT** based on ExxonMobil, PNG LNG, or any operator's confidential data
3. **NOT** a substitute for professional engineering judgment
4. **NOT** a production-grade software application
5. **NOT** affiliated with or endorsed by ExxonMobil Corporation or any LNG operator

## What This Project IS

1. **IS** a portfolio demonstration of reliability engineering thinking
2. **IS** built entirely from publicly available datasets
3. **IS** an honest, transparent learning exercise
4. **IS** a demonstration of Python data analysis and engineering communication skills
5. **IS** designed to show readiness for a graduate engineer role in operations technical

---

## Interview Talking Points

If asked about this project in an interview:

**Q: "Is this real LNG plant data?"**
> "No. It uses publicly available industrial datasets — PHMSA pipeline incident data,
> MetroPT-3 compressor sensor data, and Microsoft Azure predictive maintenance data —
> adapted into LNG-style equipment categories. All data sources and adaptations are
> documented in the repository."

**Q: "How accurate are the reliability KPIs?"**
> "They're order-of-magnitude estimates. Without true operating hour data and confirmed
> failure-event definitions, MTBF and Availability are illustrative. I've labeled them
> as 'estimates' throughout. The value is in the methodology, not the absolute numbers."

**Q: "Why did you build this?"**
> "I wanted to demonstrate the kind of reliability engineering thinking expected in an
> operations technical role — asset hierarchies, condition monitoring, risk-based
> maintenance prioritization, and KPI computation — using real industrial datasets
> adapted to an LNG context. I built it while my graduate application was being processed
> to show initiative and technical capability."

---

*This document should be updated whenever a new assumption is made or a new limitation
is discovered. Honesty compounds; deception collapses.*