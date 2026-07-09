# MetroPT-3 Compressor Surveillance Plan

## Dataset Representation

MetroPT-3 is a public compressor dataset containing operating measurements and
status signals from an air compressor system. In this portfolio demonstration,
the dataset is adapted for LNG-style compressor surveillance and rotating
equipment health monitoring.

This is not ExxonMobil or PNG LNG operating data. It does not contain
confidential, proprietary, or licensee data.

## Useful Compressor Surveillance Columns

The following columns appear useful for compressor process surveillance:

| Column | Potential Surveillance Use |
|---|---|
| `timestamp` | Time-series trending and dashboard filtering |
| `TP2` | Pressure behavior around one compressor measurement point |
| `TP3` | Pressure behavior around another compressor measurement point |
| `H1` | Additional pressure or system state indicator |
| `DV_pressure` | Discharge valve pressure behavior |
| `Reservoirs` | Reservoir pressure trend |
| `Oil_temperature` | Lubrication or thermal condition monitoring |
| `Motor_current` | Compressor electrical load and running-state indicator |
| `COMP` | Compressor operating signal |
| `DV_eletric` | Discharge valve electrical signal |
| `Towers` | System state or operating-mode signal |
| `MPG` | Operating status signal |
| `LPS` | Low-pressure switch signal |
| `Pressure_switch` | Pressure switch status |
| `Oil_level` | Oil level status signal |
| `Caudal_impulses` | Flow or pulse-style operating signal |

## LNG-Style Monitoring Link

For the LNG Operations Technical Reliability Dashboard, MetroPT-3 can represent
a public compressor dataset adapted for LNG-style compressor surveillance. The
sensor values can be used to demonstrate how an LNG technical support team might
monitor compressor operating stability, load, oil temperature, pressure trends,
and signal changes.

This mapping is for portfolio demonstration only. The compressor is not an LNG
plant compressor, and the values should not be treated as real LNG operating
limits.

## Candidate Dashboard Metrics

The following metrics can be built later from the profiled MetroPT-3 data:

- Average motor current
- Average oil temperature
- Pressure trend for `TP2`, `TP3`, `H1`, `DV_pressure`, and `Reservoirs`
- High-temperature alert count
- High-pressure alert count
- Compressor operating status
- Sensor anomaly flags
- Running versus idle time estimate
- Oil-level status count
- Low-pressure switch activation count
- Pressure switch status count

## Possible Simple Logic For Later Scripts

Beginner-friendly dashboard logic can start with transparent thresholds:

- Flag high oil temperature when `Oil_temperature` is above a selected public
  dataset threshold.
- Flag high pressure when pressure columns are above selected public dataset
  thresholds.
- Treat `Motor_current` above a low cutoff as a running-state indicator.
- Use rolling averages for pressure and oil temperature trends.
- Create anomaly flags when a sensor is far above its rolling average.

Any thresholds should be described as public-dataset screening thresholds, not
formal LNG plant alarm limits.

## Limitations

- MetroPT-3 is a public compressor dataset, not ExxonMobil or PNG LNG operating
  data.
- The compressor type and service are not equivalent to LNG refrigeration,
  boil-off gas, feed gas, or utility compressor service.
- LNG-style equipment names and dashboard categories are adapted for portfolio
  demonstration.
- Sensor thresholds derived from this dataset are screening values only.
- The dataset does not provide full maintenance work orders, production impact,
  or verified downtime records.
- Later dashboard metrics should use phrases such as "surveillance estimate",
  "screening flag", and "adapted for LNG-style compressor surveillance" instead
  of claiming formal operating limits or production reliability results.
