import boto3
import time
from src.config import REGION, FPA_FOD_CRAWLER_NAME

def run_crawler_and_wait(crawler_name):
    glue = boto3.client("glue", region_name=REGION)

    print(f"▶️ Starting crawler: {crawler_name}...")
    glue.start_crawler(Name=crawler_name)

    while True:
        state = glue.get_crawler(Name=crawler_name)["Crawler"]["State"]
        if state == "READY":
            print(f"✅ Crawler {crawler_name} completed successfully.")
            break
        elif state in ("RUNNING", "STOPPING"):
            print(f"⏳ Crawler is {state.lower()}...")
            time.sleep(10)
        else:
            raise RuntimeError(f"❌ Unexpected crawler state: {state}")

if __name__ == "__main__":
    run_crawler_and_wait(FPA_FOD_CRAWLER_NAME)
