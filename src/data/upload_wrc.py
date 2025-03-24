import boto3
from dotenv import load_dotenv
load_dotenv()

from botocore.exceptions import ClientError
from src.config import RAW_BUCKET, WRC_LOCAL_PATH, WRC_S3_KEY

def upload_wrc_to_s3():
    s3 = boto3.client("s3")
    try:
        s3.upload_file(WRC_LOCAL_PATH, RAW_BUCKET, WRC_S3_KEY)
        print(f"✅ Uploaded WRC to s3://{RAW_BUCKET}/{WRC_S3_KEY}")
    except ClientError as e:
        print(f"❌ Upload failed: {e}")

if __name__ == "__main__":
    upload_wrc_to_s3()
