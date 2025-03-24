import boto3
from dotenv import load_dotenv
load_dotenv()

from botocore.exceptions import ClientError
from src.config import RAW_BUCKET, FPA_FOD_LOCAL_PATH, FPA_FOD_S3_KEY

def upload_fpa_fod_to_s3():
    s3 = boto3.client("s3")
    try:
        s3.upload_file(FPA_FOD_LOCAL_PATH, RAW_BUCKET, FPA_FOD_S3_KEY)
        print(f"✅ Uploaded FPA/FOD to s3://{RAW_BUCKET}/{FPA_FOD_S3_KEY}")
    except ClientError as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    upload_fpa_fod_to_s3()
