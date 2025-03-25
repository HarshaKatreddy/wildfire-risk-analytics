---

# 🔥 Wildfire Risk Analytics Platform (AWS Cloud-Native)

A fully automated pipeline for wildfire risk intelligence, built on Amazon Web Services. This cloud-native system integrates climate, fire incident, and exposure datasets to deliver county-level wildfire risk metrics — tailored for insurance underwriting, reinsurance planning, and portfolio exposure monitoring.

---

## 📌 Project Highlights

- 🧱 **Infrastructure-as-Code** via AWS CDK (Python)
- 🛰️ **Public Datasets**: NOAA nClimDiv, FPA FOD, Wildfire Risk to Communities (WRC)
- 🧪 **ETL Pipelines**: AWS Lambda, Glue Crawlers, Athena Queries
- 📊 **Dashboard**: Live analytics with Amazon QuickSight
- 🏢 **Insurance Use Case**: Risk normalization, WUI exposure, and hazard scores

---

## 🛠️ Quick Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/HarshaKatreddy/wildfire-risk-analytics.git
cd wildfire-risk-analytics
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

---

### 2. Configure `.env` and AWS CLI

#### ✅ Create `.env`

In your project root, add the following:

```bash
PYTHONPATH=.
AWS_DEFAULT_REGION=us-east-1
```

> No need to set bucket names or roles manually — they’re automatically pulled from `cdk_outputs.json`.

#### 🔐 Set up AWS CLI

Configure your credentials locally:

```bash
aws configure
```

Provide:
- Access Key ID
- Secret Access Key
- Default region: `us-east-1`
- Output format: `json`

> 📦 Install CDK CLI (if first time):

```bash
npm install -g aws-cdk
```

---

### 3. Download Fire Incident Data

📥 [Download `fpa_fod.csv`](https://wildfire-raw-data-863518413936.s3.us-east-1.amazonaws.com/fpa-fod/fpa_fod.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIA4SDNVKRYMO4755HI%2F20250325%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250325T173032Z&X-Amz-Expires=259200&X-Amz-SignedHeaders=host&X-Amz-Signature=e80c863b755cd7bf726be12d9a2ae6bf9193b5bd782e362dcc5d8fddbb779dac)

Save this file as:

```bash
data/fpa_fod.csv
```

---

### 4. Deploy Infrastructure & Ingest Data

```bash
cdk bootstrap
./start_pipeline.sh
```

This will:

- Deploy AWS stack (S3, Lambda, Glue, IAM, EventBridge)
- Upload datasets to raw S3 buckets
- Run Glue Crawlers and create Athena tables
- Prepare data for downstream analysis and dashboarding

---

## 📊 Analysis & Visualization

- 🔍 **Exploratory Analysis**: [`notebooks/eda_athena.ipynb`](notebooks/eda_athena.ipynb)
- ⚙️ **Athena Transformations**: Normalization, joining on GEOID, imputation
- 📈 **Dashboard (QuickSight)**:  
  - Wildfire hazard maps  
  - Housing exposure & WUI impact  
  - PDSI, precipitation, temperature trends  
  - KPI cards for insurers

---

## 🧱 Architecture

```text
📁 raw S3
 ├── fpa-fod/
 ├── wrc-v2/
 └── nclimdiv-county/

📁 processed S3
 └── nclimdiv/

🧠 Glue Databases
 ├── wildfire_fpa_fod_db
 ├── wildfire_wrc_db
 ├── wildfire_nclimdiv_db
 └── wildfire_clean_db

🧮 Athena
 └── SQL ETL via config.py + notebooks

📊 QuickSight
 └── Live visuals for insurance risk
```

---

## 📁 Project Structure

```text
infra/                     # CDK stack + Lambdas
src/
 ├── data/                 # Upload scripts
 ├── orchestrator/        # Run crawlers
 ├── config.py            # CDK + environment resolver
scripts/
 └── convert_nclimdiv_manually.py
notebooks/
 └── eda_athena.ipynb
start_pipeline.sh         # Bootstrap everything
```

---

## 🧾 Key Use Cases for Insurers

- Evaluate **wildfire exposure** at the county level
- Quantify **housing unit risk** across fire-prone zones
- Normalize scores to support **premium setting**
- Inform **reinsurance strategy** based on real-world indicators

---

## 🚀 What’s Next

- Auto-trigger QuickSight refresh
- Add SageMaker predictive models
- Stream real-time fire feeds (NASA FIRMS, GOES)

---

## 📜 License

This project is open-source under the MIT License.

---

## 📚 References

- Short, K. C. (2022). *Spatial wildfire occurrence data for the United States, 1992–2020 [FPA_FOD_20221014]* (6th Edition). Fort Collins, CO: Forest Service Research Data Archive. https://doi.org/10.2737/RDS-2013-0009.6

- Vose, R. S., Applequist, S., Squires, M., Durre, I., Menne, M. J., Williams, C. N., Fenimore, C., Gleason, K., & Arndt, D. (2014). *NOAA Monthly U.S. Climate Divisional Database (NClimDiv)*. NOAA National Climatic Data Center. https://doi.org/10.7289/V5M32STR

- Scott, J. H., Dillon, G. K., Jaffe, M. R., Vogler, K. C., Olszewski, J. H., Callahan, M. N., Karau, E. C., Lazarr, M. T., Short, K. C., Riley, K. L., Finney, M. A., & Grenfell, I. C. (2024). *Wildfire Risk to Communities: Spatial datasets of landscape-wide wildfire risk components for the United States* (2nd Edition). Fort Collins, CO: Forest Service Research Data Archive. https://doi.org/10.2737/RDS-2020-0016-2
