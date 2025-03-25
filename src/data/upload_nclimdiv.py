import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

# Import config values
from src.config import RAW_BUCKET

# Mapping of local filenames to S3 keys
NCLIMDIV_FILES = {
    "climdiv-pcpncy-v1.0.0-20250306": "nclimdiv-county/climdiv-pcpncy/climdiv-pcpncy.dat",
    "climdiv-pdsicy-v1.0.0-20250306": "nclimdiv-county/climdiv-pdsicy/climdiv-pdsicy.dat",
    "climdiv-tmaxcy-v1.0.0-20250306": "nclimdiv-county/climdiv-tmaxcy/climdiv-tmaxcy.dat",
    "climdiv-tmincy-v1.0.0-20250306": "nclimdiv-county/climdiv-tmincy/climdiv-tmincy.dat",
    "climdiv-tmpccy-v1.0.0-20250306": "nclimdiv-county/climdiv-tmpccy/climdiv-tmpccy.dat",
}

LOCAL_FOLDER = "data"

def upload_nclimdiv_files():
    s3 = boto3.client("s3")

    for local_filename, s3_key in NCLIMDIV_FILES.items():
        local_path = f"{LOCAL_FOLDER}/{local_filename}"
        try:
            s3.upload_file(local_path, RAW_BUCKET, s3_key)
            print(f"✅ Uploaded {local_filename} to s3://{RAW_BUCKET}/{s3_key}")
        except ClientError as e:
            print(f"❌ Upload failed for {local_filename}: {e}")

if __name__ == "__main__":
    upload_nclimdiv_files()
