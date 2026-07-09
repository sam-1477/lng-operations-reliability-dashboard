# Data Inventory

This document records the public datasets downloaded for the LNG Operations Technical Reliability Dashboard project.

## Raw Dataset Files

| Dataset | Local File | Purpose in Project | Source Type | GitHub Status |
|---|---|---|---|---|
| PHMSA LNG Incident Data | data/raw/phmsa_lng_incident_data_2011_present.zip | LNG facility incident and risk analysis | Public regulatory data | Not committed |
| PHMSA Gas Transmission Incident Data | data/raw/phmsa_gas_transmission_incident_data_2010_present.zip | Pipeline incident and mechanical integrity risk analysis | Public regulatory data | Not committed |
| MetroPT-3 Compressor Dataset | data/raw/metropt-3-dataset.zip | Compressor condition monitoring and process surveillance | Public industrial condition-monitoring data | Not committed |
| Microsoft Azure Predictive Maintenance Dataset | data/raw/azure_predictive_maintenance_dataset.zip | Maintenance, telemetry, errors, failures, and machine metadata | Public predictive maintenance dataset | Not committed |

## Important Note

Raw datasets are stored locally only and are not committed to GitHub. The repository will contain documentation, processing scripts, small processed samples, screenshots, and reports.

## Data Usage Strategy

The project uses public industrial datasets as the technical backbone. A small LNG-style asset mapping layer will be created to organize these datasets into portfolio equipment categories such as compressors, pumps, pipeline sections, motors, and mechanical integrity items.

This project does not use ExxonMobil, PNG LNG, or confidential operating data.