from src.data.upload_fpa_fod import upload_fpa_fod_to_s3
from src.glue_athena.run_athena_query import run_query, wait_for_results

def main():
    print("🚀 Step 1: Uploading FPA FOD CSV to S3...")
    upload_fpa_fod_to_s3()

    print("🔍 Step 2: Running Athena test query...")
    query = "SELECT * FROM era5_hourly_data LIMIT 10"
    query_id = run_query(query)
    status = wait_for_results(query_id)
    print(f"✅ Athena Query Finished with Status: {status}")

if __name__ == "__main__":
    main()
