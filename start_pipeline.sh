#!/bin/bash
set -e

echo "🚀 Deploying CDK..."
cdk deploy --outputs-file cdk_outputs.json

echo "🔍 Uploading fpa fod data to S3..."
python -m src.data.upload_fpa_fod

echo "🔍 Processing nclimdiv raw data..."
python -m scripts.convert_nclimdiv_manually

echo "▶️ Running FPA FOD crawler..."
python -m src.orchestrator.run_fpa_fod_crawler

echo "▶️ Running nclimdiv crawler..."
python -m src.orchestrator.run_nclimdiv_crawler

echo "✅ All done!"
