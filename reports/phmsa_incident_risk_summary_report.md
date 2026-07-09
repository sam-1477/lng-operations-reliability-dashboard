# PHMSA Incident Risk Summary Report

## What The PHMSA Datasets Represent

The PHMSA LNG incident dataset contains public incident records for US LNG facilities. The PHMSA Gas Transmission incident dataset contains public incident records for US gas transmission and gathering pipeline systems.

For this project, the data is adapted for LNG-style incident risk awareness as a portfolio demonstration. It is not ExxonMobil or PNG LNG operating data.

## Why This Helps The Dashboard

Public PHMSA incident data gives the LNG Operations Technical Reliability Dashboard a credible public-data basis for incident awareness, pipeline incident trends, consequence severity, cause category review, and mechanical integrity context.

Useful dashboard sections supported by this data include:

- LNG incident awareness
- Pipeline incident trends
- Consequence severity
- Cause category review
- Mechanical integrity and risk context

## Fields Available And Matched

### PHMSA LNG Incidents

```text
                            logical_field         selected_column
                                     year                   IYEAR
     state_or_location_field_if_available          FACILITY_STATE
              cause_category_if_available                   CAUSE
incident_type_or_system_type_if_available           ITEM_INVOLVED
        total_estimated_cost_if_available                   PRPTY
                  fatalities_if_available                   FATAL
                    injuries_if_available                  INJURE
      ignition_or_fire_field_if_available              IGNITE_IND
       release_or_leak_field_if_available COMMODITY_RELEASED_TYPE
```

### PHMSA Gas Transmission Incidents

```text
                            logical_field            selected_column
                                     year                      IYEAR
     state_or_location_field_if_available ONSHORE_STATE_ABBREVIATION
              cause_category_if_available                      CAUSE
incident_type_or_system_type_if_available          PIPELINE_FUNCTION
        total_estimated_cost_if_available                      PRPTY
                  fatalities_if_available                      FATAL
                    injuries_if_available                     INJURE
      ignition_or_fire_field_if_available                 IGNITE_IND
       release_or_leak_field_if_available               RELEASE_TYPE
```

## Incident-Risk Summary Created

The processed file `data/processed/phmsa_incident_risk_summary.csv` groups incidents by public dataset, year, location/state field, cause category, incident or system type, ignition/fire indicator, and release/leak field where available.

The summary includes incident counts, summed estimated cost, summed fatalities, summed injuries, and a short dashboard risk note.

This is a risk-awareness summary, not a formal integrity assessment.

## Output Snapshot

- Grouped summary rows: 1,564
- Source incident rows used:
- PHMSA Gas Transmission Incidents: 2,025
- PHMSA LNG Incidents: 51

## Limitations

- PHMSA records are public US incident data, not PNG LNG operating data.
- PHMSA incident forms and field definitions differ between LNG and Gas Transmission datasets.
- Best-effort column matching is used where exact field names differ.
- Cost, release, fire, injury, fatality, and cause fields depend on reported PHMSA form data and may change after supplemental reports.
- The summary is intended for portfolio demonstration and dashboard screening, not regulatory analysis or a formal mechanical integrity assessment.
