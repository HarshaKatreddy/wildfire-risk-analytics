# src/glue_athena/start_glue_crawler.py

import boto3
from src.config import REGION, GLUE_CRAWLER_NAME

def run_glue_crawler():
    glue = boto3.client("glue", region_name=REGION)
    try:
        glue.start_crawler(Name=GLUE_CRAWLER_NAME)
        print(f"🚀 Started Glue crawler: {GLUE_CRAWLER_NAME}")
    except glue.exceptions.CrawlerRunningException:
        print(f"⚠️ Crawler {GLUE_CRAWLER_NAME} is already running.")
    except glue.exceptions.EntityNotFoundException:
        print(f"❌ Crawler {GLUE_CRAWLER_NAME} not found.")
    except Exception as e:
        print(f"❌ Failed to start crawler: {e}")

if __name__ == "__main__":
    run_glue_crawler()
