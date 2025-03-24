import boto3
from src.config import RAW_BUCKET, ERA5_BUCKET, ERA5_DATA_PREFIX, REGION

s3 = boto3.resource("s3", region_name=REGION)
src_bucket = s3.Bucket(ERA5_BUCKET)
dst_bucket = s3.Bucket(RAW_BUCKET)

def copy_era5_subset():
    prefix = ERA5_DATA_PREFIX
    copied = 0

    for obj in src_bucket.objects.filter(Prefix=prefix):
        source_key = obj.key
        dest_key = f"era5/{source_key.split('/')[-1]}"

        dst_bucket.copy(
            {
                'Bucket': ERA5_BUCKET,
                'Key': source_key
            },
            dest_key
        )

        copied += 1
        print(f"✅ Copied: {source_key} → s3://{RAW_BUCKET}/{dest_key}")

    print(f"🎉 Finished copying {copied} ERA5 files.")

if __name__ == "__main__":
    copy_era5_subset()
