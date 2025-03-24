import boto3
import os
import requests
from bs4 import BeautifulSoup

s3 = boto3.client("s3")
bucket = os.environ["RAW_BUCKET"]
parent_prefix = "nclimdiv-county/"
base_url = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/"

FILE_PREFIXES = [
    "climdiv-tmaxcy",
    "climdiv-tmincy",
    "climdiv-tmpccy",
    "climdiv-pcpncy",
    "climdiv-pdsicy"
]

EXCLUDE_SUFFIXES = (".pdf", ".html", ".txt")

def get_latest_file_urls():
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    file_urls = {}
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(EXCLUDE_SUFFIXES):
            continue
        for prefix in FILE_PREFIXES:
            if href.startswith(prefix):
                file_urls[prefix] = base_url + href
    return file_urls

def lambda_handler(event, context):
    print("🔍 Searching for latest NOAA nClimDiv files...")
    files = get_latest_file_urls()

    for prefix, url in files.items():
        original_filename = os.path.basename(url)
        local_path = f"/tmp/{original_filename}"
        final_name = f"{prefix}.dat"  # normalized
        s3_key = f"{parent_prefix}{prefix}/{final_name}"

        print(f"⬇️ Downloading (streamed) {url}")
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        print(f"📤 Uploading to s3://{bucket}/{s3_key}")
        s3.upload_file(local_path, bucket, s3_key)

    print("✅ All files downloaded and uploaded to S3.")
    return {
        "status": "success",
        "files_uploaded": list(files.values())
    }
