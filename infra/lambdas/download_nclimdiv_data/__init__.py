import boto3
import os
import requests
from bs4 import BeautifulSoup

s3 = boto3.client("s3")
bucket = os.environ["RAW_BUCKET"]
prefix = "nclimdiv-county/"
base_url = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/"

FILE_PREFIXES = [
    "climdiv-tmaxcy",
    "climdiv-tmincy",
    "climdiv-tmpccy",
    "climdiv-pcpncy",
    "climdiv-pdsicy"
]

def get_latest_file_urls():
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")

    file_urls = {}
    for a in soup.find_all("a", href=True):
        for prefix in FILE_PREFIXES:
            if a['href'].startswith(prefix) and a['href'].endswith(".dat"):
                # Always update to most recent match
                file_urls[prefix] = base_url + a['href']
    return file_urls

def lambda_handler(event, context):
    print("🔍 Searching for latest NOAA nClimDiv files...")
    files = get_latest_file_urls()

    for prefix, url in files.items():
        local_file = f"/tmp/{os.path.basename(url)}"
        s3_key = prefix + "/" + os.path.basename(url)

        print(f"⬇️  Downloading {url}")
        r = requests.get(url)
        with open(local_file, "wb") as f:
            f.write(r.content)

        print(f"📤 Uploading to s3://{bucket}/{prefix}{os.path.basename(url)}")
        s3.upload_file(local_file, bucket, f"{prefix}{os.path.basename(url)}")

    print("✅ All files downloaded and uploaded to S3.")

    # Emit EventBridge event to trigger downstream
    return {
        "status": "success",
        "files": list(files.values())
    }
