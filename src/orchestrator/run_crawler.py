import boto3
from src.config import REGION, GLUE_CRAWLER_NAME

def run_crawler():
    glue = boto3.client("glue", region_name=REGION)
    glue.start_crawler(Name=GLUE_CRAWLER_NAME)
    print(f"🚀 Started crawler: {GLUE_CRAWLER_NAME}")

if __name__ == "__main__":
    run_crawler()
