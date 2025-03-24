import boto3
import io
import re
import pandas as pd
from src.config import RAW_BUCKET, PROCESSED_BUCKET, NCLIMDIV_RAW_PREFIX, NCLIMDIV_PROCESSED_PREFIX

# Initialize S3 client
s3 = boto3.client("s3")

# Fixed mappings
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
            print(f"⚠️ Skipped line due to error: {e}")
    return pd.DataFrame(records)

def convert_and_merge_all():
    print("🚀 Starting nClimDiv merged CSV generation...")

    response = s3.list_objects_v2(Bucket=RAW_BUCKET, Prefix=NCLIMDIV_RAW_PREFIX)
    dat_files = [
        obj["Key"] for obj in response.get("Contents", [])
        if obj["Key"].endswith(".dat") and "climdiv-" in obj["Key"]
    ]

    merged_df = None

    for key in dat_files:
        print(f"📄 Processing: {key}")
        match = re.search(r"climdiv-([a-z]+)cy", key)
        if not match:
            print(f"⚠️ Skipping unknown format: {key}")
            continue
        var_prefix = match.group(1)
        var_name = PREFIX_MAP.get(var_prefix, var_prefix)

        obj = s3.get_object(Bucket=RAW_BUCKET, Key=key)
        lines = obj["Body"].read().decode("utf-8").splitlines()
        df = parse_fixed_width_lines(lines, var_name)

        if df.empty:
            print(f"⚠️ No valid data found in {key}")
            continue

        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on=["state_code", "county_fips", "year", "month"], how="outer")

    if merged_df is not None:
        csv_buffer = io.StringIO()
        merged_df.to_csv(csv_buffer, index=False)
        s3_key = f"{NCLIMDIV_PROCESSED_PREFIX}nclimdiv_merged.csv"
        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=s3_key,
            Body=csv_buffer.getvalue().encode("utf-8")
        )
        print(f"✅ Merged CSV uploaded to s3://{PROCESSED_BUCKET}/{s3_key}")
    else:
        print("⚠️ No data was processed, no file uploaded.")

    print("🎉 All conversions complete.")

if __name__ == "__main__":
    convert_and_merge_all()