
# 🔥 Wildfire Risk Analytics Platform (AWS Cloud-Native)

A fully automated, scalable pipeline for wildfire risk intelligence, built on Amazon Web Services. This platform integrates climate, fire incident, and exposure datasets to deliver county-level wildfire risk metrics—tailored for insurance underwriting, portfolio rebalancing, and reinsurance analytics.

---

## 📌 Project Highlights

- 🧱 **Infrastructure-as-Code** with AWS CDK
- 🛰️ **Open Datasets**: NOAA nClimDiv, FPA FOD, Wildfire Risk to Communities (WRC)
- 🧪 **ETL** using AWS Glue, Athena, and Lambda
- 📊 **Dashboard** via Amazon QuickSight
- 🏢 **Insurance Focus**: Risk scores, housing exposure, and wildfire hazard normalized for underwriting decisions

---

## 🛠️ Quick Setup Guide

### 1. Clone and Set Up the Environment

```bash
git clone https://github.com/HarshaKatreddy/wildfire-risk-analytics.git
cd wildfire-risk-analytics
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

> ⚠️ Create a `.env` file based on `.env.template` and provide AWS credentials + paths.

---

### 2. Deploy Full Infrastructure (via CDK + Shell Script)

```bash
cdk bootstrap
./start_pipeline.sh
```

This will:
- 🚀 Deploy AWS resources via CDK (S3, Lambda, Glue, IAM, EventBridge)
- 📁 Upload raw datasets to S3
- 🧹 Run Glue Crawlers
- 🧮 Build Athena tables for downstream analytics

---

## 🧠 Project Architecture

```text
📁 raw S3
  └── fpa-fod/
  └── wrc-v2/
  └── nclimdiv-county/
       └── climdiv-pcpncy/
       └── climdiv-tmaxcy/
       ...

📁 processed S3
  └── nclimdiv/ (converted to long-format CSV)

🧠 Glue Databases
  └── wildfire_fpa_fod_db
  └── wildfire_wrc_db
  └── wildfire_nclimdiv_db
  └── wildfire_clean_db (transformed tables)

🧮 Athena ETL
  └── Joins all datasets on `geoid`
  └── Normalizes & imputes risk metrics

📊 QuickSight
  └── Live connection to Athena
  └── Visual dashboards for insurers
```

---

## 📊 Analysis & Dashboard

- **Notebook-based EDA**: See [`notebooks/eda_athena.ipynb`](notebooks/eda_athena.ipynb) for analysis, sanity checks, and feature generation using Athena queries.
- **Final Dashboard**: Built on Athena outputs. Features:
  - Choropleth risk maps by county
  - Climate trends (precipitation, PDSI, temperature)
  - Burn probability & housing exposure metrics
  - KPI cards for hazard potential, normalized risks

---

## 📁 Key Files

```text
📦 src/
 ├── data/                   # Upload scripts for WRC, FPA, NOAA
 ├── orchestrator/           # Trigger Glue crawlers
 ├── config.py               # Centralized environment config
📦 infra/
 ├── lambdas/                # Two Lambda functions (download NOAA, convert to CSV)
 ├── wildfire_risk_stack.py  # CDK Stack definition
📦 scripts/
 └── convert_nclimdiv_manually.py
📦 notebooks/
 └── eda_athena.ipynb        # Interactive exploration
start_pipeline.sh            # Runs full ingestion and crawler pipeline
requirements.txt
```

---

## 🧾 Use Cases for Insurers

- 🔍 Evaluate wildfire exposure at the **county level**
- ✍️ Price premiums by combining burn probability and housing risk
- 🧮 Identify underweight/overweight portfolios in **WUI regions**
- ♻️ Support **reinsurance negotiations** with empirical risk signals

---

## 📌 Future Enhancements

- 🔄 Auto-trigger crawlers and QuickSight refresh on new data arrival
- 🤖 Integrate predictive modeling using SageMaker
- 🧬 Incorporate real-time fire feeds (e.g., NASA FIRMS)

---

## 📜 License

This project is open-source under the MIT License.

---

Let me know if you want me to add:

- A QuickSight dashboard preview image
- Architecture diagram in Mermaid or PNG
- GitHub Actions CI/CD instructions

Would you like this version pushed directly to your repo as a `README.md`?