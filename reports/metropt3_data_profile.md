# MetroPT-3 Compressor Data Profile

This report profiles the public MetroPT-3 compressor dataset for portfolio demonstration. The dataset is adapted for LNG-style compressor surveillance and rotating equipment health monitoring.

This is a public compressor dataset. It is not ExxonMobil or PNG LNG operating data, and it does not contain confidential, proprietary, or licensee data.

## Main Compressor File

- File name: `MetroPT3_AirCompressor.csv`
- Source path: `data/raw/extracted/metropt3/MetroPT3_AirCompressor.csv`
- Row count: 1,516,948
- Column count: 17
- GitHub-safe sample: `samples/metropt3/metropt3_compressor_sample.csv`

## Column Names

The raw CSV contains a blank first column that is labeled `source_row_index` in this profile and sample.

```text
source_row_index, timestamp, TP2, TP3, H1, DV_pressure, Reservoirs, Oil_temperature, Motor_current, COMP, DV_eletric, Towers, MPG, LPS, Pressure_switch, Oil_level, Caudal_impulses
```

## First 5 Rows

```text
 source_row_index           timestamp    TP2   TP3    H1  DV_pressure  Reservoirs  Oil_temperature  Motor_current  COMP  DV_eletric  Towers  MPG  LPS  Pressure_switch  Oil_level  Caudal_impulses
                0 2020-02-01 00:00:00 -0.012 9.358 9.340       -0.024       9.358           53.600         0.0400   1.0         0.0     1.0  1.0  0.0              1.0        1.0              1.0
               10 2020-02-01 00:00:10 -0.014 9.348 9.332       -0.022       9.348           53.675         0.0400   1.0         0.0     1.0  1.0  0.0              1.0        1.0              1.0
               20 2020-02-01 00:00:19 -0.012 9.338 9.322       -0.022       9.338           53.600         0.0425   1.0         0.0     1.0  1.0  0.0              1.0        1.0              1.0
               30 2020-02-01 00:00:29 -0.012 9.328 9.312       -0.022       9.328           53.425         0.0400   1.0         0.0     1.0  1.0  0.0              1.0        1.0              1.0
               40 2020-02-01 00:00:39 -0.012 9.318 9.302       -0.022       9.318           53.475         0.0400   1.0         0.0     1.0  1.0  0.0              1.0        1.0              1.0
```

## Missing Value Summary

```text
          column  missing_count  missing_percent
source_row_index              0              0.0
       timestamp              0              0.0
             TP2              0              0.0
             TP3              0              0.0
              H1              0              0.0
     DV_pressure              0              0.0
      Reservoirs              0              0.0
 Oil_temperature              0              0.0
   Motor_current              0              0.0
            COMP              0              0.0
      DV_eletric              0              0.0
          Towers              0              0.0
             MPG              0              0.0
             LPS              0              0.0
 Pressure_switch              0              0.0
       Oil_level              0              0.0
 Caudal_impulses              0              0.0
```

## Basic Numeric Summary For Sensor Columns

The numeric summary is calculated in chunks to avoid loading the full 218 MB CSV into memory unnecessarily.

```text
         column   count    mean    std    min    max
            TP2 1516948  1.3678 3.2509 -0.032 10.676
            TP3 1516948  8.9846 0.6391  0.730 10.302
             H1 1516948  7.5682 3.3332 -0.036 10.288
    DV_pressure 1516948  0.0560 0.3824 -0.032  9.844
     Reservoirs 1516948  8.9852 0.6383  0.712 10.300
Oil_temperature 1516948 62.6442 6.5163 15.400 89.050
  Motor_current 1516948  2.0502 2.3021  0.020  9.295
           COMP 1516948  0.8370 0.3694  0.000  1.000
     DV_eletric 1516948  0.1606 0.3672  0.000  1.000
         Towers 1516948  0.9198 0.2715  0.000  1.000
            MPG 1516948  0.8327 0.3733  0.000  1.000
            LPS 1516948  0.0034 0.0584  0.000  1.000
Pressure_switch 1516948  0.9914 0.0921  0.000  1.000
      Oil_level 1516948  0.9042 0.2944  0.000  1.000
Caudal_impulses 1516948  0.9371 0.2428  0.000  1.000
```

## Useful Compressor Surveillance Columns

- `TP2`, `TP3`, `H1`, `DV_pressure`, and `Reservoirs` can support pressure trend and pressure alert views.
- `Oil_temperature` can support oil temperature monitoring and high-temperature alert counts.
- `Motor_current` can support compressor load and running-state surveillance.
- `COMP`, `DV_eletric`, `Towers`, `MPG`, `LPS`, `Pressure_switch`, `Oil_level`, and `Caudal_impulses` can support operating-status and signal-state checks.

## Notes

- Raw MetroPT-3 files remain local under `data/raw/`.
- This script writes only the Markdown profile and small sample CSV.
- The sample file is capped at 1,000 rows.
- The data is adapted for LNG-style compressor surveillance as a portfolio demonstration.
