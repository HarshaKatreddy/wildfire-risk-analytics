# Wildfire Risk Analytics (AWS Cloud-Native, CDK + Boto3-Driven)

## 📁 Folder Structure

- `wildfire_risk_analytics/`: CDK stack definition (infrastructure-as-code)
- `src/`: Python modules for data ingestion, config, orchestrator
- `.env`: AWS credentials (excluded from Git)
- `requirements.txt`: Python package dependencies
- `README.md`: Project setup and instructions

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repo and enter the project
git clone https://github.com/yourusername/wildfire-risk-analytics.git
cd wildfire-risk-analytics

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install AWS CDK globally
npm install -g aws-cdk
cdk --version

# 5. Initialize CDK Project (already done in this repo)
# Skip this if CDK files are present. If starting fresh:
cdk init app --language python

# 6. Bootstrap the environment (only once per account/region)
cdk bootstrap

# 7. Deploy infrastructure using CDK
cdk deploy

# ✅ Post-CDK Setup

Once CDK deployment completes successfully, a file named `cdk_outputs.json` will be generated.

Make sure it's present in the **root directory** as it contains the dynamically generated:

- Raw S3 bucket name
- Processed S3 bucket name
- Glue IAM role ARN

We use this file in our config to avoid hardcoding any AWS resource names.

> ⚠️ Important: Do not check this file into Git. It is auto-generated and account-specific.

```bash
# .gitignore
cdk_outputs.json

🔐 Environment Variables
Create a .env file in the project root with the following:

AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1

⚙️ Configuration
All environment-aware and AWS-aware settings are centralized in:
src/config.py