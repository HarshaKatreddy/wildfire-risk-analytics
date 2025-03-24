import os
import json
from pathlib import Path
from dotenv import load_dotenv
import boto3

# Load environment variables
load_dotenv()

# Set AWS region
REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Project root and CDK outputs path
project_root = Path(__file__).resolve().parents[1]
CDK_OUTPUTS_PATH = project_root / "cdk_outputs.json"

if not CDK_OUTPUTS_PATH.exists():
    raise FileNotFoundError(
        "❌ cdk_outputs.json not found. Run:\n\n  cdk deploy --outputs-file cdk_outputs.json"
    )

# Load CDK outputs
with open(CDK_OUTPUTS_PATH) as f:
    cdk_outputs = json.load(f)["WildfireRiskAnalyticsStack"]

# S3 Buckets
RAW_BUCKET = os.getenv("RAW_BUCKET", cdk_outputs["RawBucketName"])
PROCESSED_BUCKET = os.getenv("PROCESSED_BUCKET", cdk_outputs["ProcessedBucketName"])

# Glue & Athena
GLUE_IAM_ROLE = os.getenv("GLUE_IAM_ROLE", cdk_outputs["GlueRoleArn"])
FPA_FOD_CRAWLER_NAME = os.getenv("FPA_FOD_CRAWLER_NAME", cdk_outputs["FpaFodCrawlerName"])
NCLIMDIV_CRAWLER_NAME = os.getenv("NCLIMDIV_CRAWLER_NAME", cdk_outputs["NclimdivCrawlerName"])

ATHENA_OUTPUT_PREFIX = "athena-results/"
ATHENA_OUTPUT_LOCATION = f"s3://{PROCESSED_BUCKET}/{ATHENA_OUTPUT_PREFIX}"

# FPA FOD paths
FPA_FOD_LOCAL_PATH = "data/fpa_fod.csv"
FPA_FOD_S3_KEY = "fpa-fod/fpa_fod.csv"

# S3 prefixes
NCLIMDIV_RAW_PREFIX = "nclimdiv-county/"
NCLIMDIV_PROCESSED_PREFIX = "nclimdiv/"

# AWS clients
glue = boto3.client("glue", region_name=REGION)

# ---------- Dynamic Glue helpers ----------

def get_database_name(prefix: str) -> str:
    """Find the Glue database name starting with a given prefix."""
    paginator = glue.get_paginator("get_databases")
    for page in paginator.paginate():
        for db in page["DatabaseList"]:
            if db["Name"].startswith(prefix.lower()):
                return db["Name"]
    raise ValueError(f"No database found with prefix: {prefix}")

def get_table_names(database_name: str, prefix: str = "") -> list[str]:
    """List all tables in a database, optionally filtered by prefix."""
    tables = []
    paginator = glue.get_paginator("get_tables")
    for page in paginator.paginate(DatabaseName=database_name):
        for table in page["TableList"]:
            if table["Name"].startswith(prefix.lower()):
                tables.append(table["Name"])
    return tables

NCLIMDIV_CRAWLER_NAME = cdk_outputs["NclimdivCrawlerName"]