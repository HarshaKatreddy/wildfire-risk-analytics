import boto3
import os
import io
import re
import pandas as pd

s3 = boto3.client("s3")
raw_bucket = os.environ["RAW_BUCKET"]
processed_bucket = os.environ["PROCESSED_BUCKET"]

PREFIX_MAP = {
    "tmax": "tmax",
    "tmin": "tmin",
    "tmpc": "tavg",
    "pcpn": "precipitation",
    "pdsi": "pdsi"
}

def parse_fixed_width_lines(lines, var_name):
    records = []
    for line in lines:
        try:
            state = line[0:2]
            county = line[2:5]
            year = int(line[7:11])
            for i in range(12):
                start = 11 + i * 7
                value_str = line[start:start + 7].strip()
                if not value_str or value_str in {"-9.99", "-99.99", "-9999"}:
                    continue
                value = float(value_str)
                records.append({
                    "state_code": state,
                    "county_fips": county,
                    "year": year,
                    "month": i + 1,
                    var_name: value
                })
        except Exception as e:
            print(f"⚠️ Skipped line: {e}")
    return pd.DataFrame(records)

def lambda_handler(event, context):
    print("🚀 Starting nClimDiv fixed-width to CSV conversion...")

    response = s3.list_objects_v2(Bucket=raw_bucket, Prefix="nclimdiv-county/")
    dat_files = [
        obj["Key"] for obj in response.get("Contents", [])
        if obj["Key"].endswith(".dat") and "climdiv-" in obj["Key"]
    ]

    for key in dat_files:
        print(f"📄 Processing: {key}")
        match = re.search(r"climdiv-([a-z]+)cy", key)
        if not match:
            print(f"⚠️ Skipping unknown file: {key}")
            continue

        var_prefix = match.group(1)
        var_name = PREFIX_MAP.get(var_prefix, var_prefix)

        # Step 1: Download
        print("📥 Downloading file from S3...")
        obj = s3.get_object(Bucket=raw_bucket, Key=key)
        content = obj["Body"].read().decode("utf-8")
        lines = content.splitlines()
        print(f"📄 Total lines read: {len(lines)}")

        # Step 2: Parse
        print(f"🧮 Parsing records for variable: {var_name}")
        df = parse_fixed_width_lines(lines, var_name)
        print(f"✅ Parsed records: {len(df)}")

        if df.empty:
            print(f"⚠️ No valid data in {key}")
            continue

        # Step 3: Convert to CSV
        output_csv = f"nclimdiv/{var_name}.csv"
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        print(f"📤 CSV ready, uploading to: {output_csv}")

        # Step 4: Upload
        s3.put_object(
            Bucket=processed_bucket,
            Key=output_csv,
            Body=csv_buffer.getvalue().encode("utf-8")
        )
        print(f"✅ Uploaded full CSV to s3://{processed_bucket}/{output_csv}")

    print("🎉 All conversions complete.")
