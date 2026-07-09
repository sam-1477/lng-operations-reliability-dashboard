# Azure Predictive Maintenance Data Profile

This report profiles the public Microsoft Azure Predictive Maintenance dataset files found locally. The data is used as a public industrial reliability dataset and may be adapted into LNG-style reliability categories in future project work.

No ExxonMobil, PNG LNG, confidential, proprietary, or licensee data is used in this profile.

## Source Files

| File | Status | Rows | Columns | Sample Output |
|---|---:|---:|---:|---|
| `PdM_machines.csv` | found | 100 | 3 | `samples/azure/PdM_machines_sample.csv` |
| `PdM_telemetry.csv` | found | 876100 | 6 | `samples/azure/PdM_telemetry_sample.csv` |
| `PdM_errors.csv` | found | 3919 | 3 | `samples/azure/PdM_errors_sample.csv` |
| `PdM_failures.csv` | found | 761 | 3 | `samples/azure/PdM_failures_sample.csv` |
| `PdM_maint.csv` | found | 3286 | 3 | `samples/azure/PdM_maint_sample.csv` |

## File Details

### PdM_machines.csv

- Source path: `data/raw/extracted/azure_pdm/PdM_machines.csv`
- Row count: 100
- Columns: machineID, model, age

First 5 rows:

```text
 machineID  model  age
         1 model3   18
         2 model4    7
         3 model3    8
         4 model3    7
         5 model3    2
```

### PdM_telemetry.csv

- Source path: `data/raw/extracted/azure_pdm/PdM_telemetry.csv`
- Row count: 876100
- Columns: datetime, machineID, volt, rotate, pressure, vibration

First 5 rows:

```text
           datetime  machineID       volt     rotate   pressure  vibration
2015-01-01 06:00:00          1 176.217853 418.504078 113.077935  45.087686
2015-01-01 07:00:00          1 162.879223 402.747490  95.460525  43.413973
2015-01-01 08:00:00          1 170.989902 527.349825  75.237905  34.178847
2015-01-01 09:00:00          1 162.462833 346.149335 109.248561  41.122144
2015-01-01 10:00:00          1 157.610021 435.376873 111.886648  25.990511
```

### PdM_errors.csv

- Source path: `data/raw/extracted/azure_pdm/PdM_errors.csv`
- Row count: 3919
- Columns: datetime, machineID, errorID

First 5 rows:

```text
           datetime  machineID errorID
2015-01-03 07:00:00          1  error1
2015-01-03 20:00:00          1  error3
2015-01-04 06:00:00          1  error5
2015-01-10 15:00:00          1  error4
2015-01-22 10:00:00          1  error4
```

### PdM_failures.csv

- Source path: `data/raw/extracted/azure_pdm/PdM_failures.csv`
- Row count: 761
- Columns: datetime, machineID, failure

First 5 rows:

```text
           datetime  machineID failure
2015-01-05 06:00:00          1   comp4
2015-03-06 06:00:00          1   comp1
2015-04-20 06:00:00          1   comp2
2015-06-19 06:00:00          1   comp4
2015-09-02 06:00:00          1   comp4
```

### PdM_maint.csv

- Source path: `data/raw/extracted/azure_pdm/PdM_maint.csv`
- Row count: 3286
- Columns: datetime, machineID, comp

First 5 rows:

```text
           datetime  machineID  comp
2014-06-01 06:00:00          1 comp2
2014-07-16 06:00:00          1 comp4
2014-07-31 06:00:00          1 comp3
2014-12-13 06:00:00          1 comp1
2015-01-05 06:00:00          1 comp4
```

## Notes

- Raw data remains local under `data/raw/` and is not modified by this script.
- Sample CSV files are capped at 100 rows each.
- The generated samples are for portfolio demonstration and repository review only.
