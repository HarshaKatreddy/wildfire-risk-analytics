import boto3
import time
from src.config import GLUE_DATABASE_NAME, ATHENA_OUTPUT_LOCATION, REGION

athena = boto3.client("athena", region_name=REGION)

def run_query(query: str):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": GLUE_DATABASE_NAME},
        ResultConfiguration={"OutputLocation": ATHENA_OUTPUT_LOCATION}
    )
    return response["QueryExecutionId"]

def wait_for_results(query_id: str):
    while True:
        response = athena.get_query_execution(QueryExecutionId=query_id)
        status = response["QueryExecution"]["Status"]["State"]
        if status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            return status
        time.sleep(2)

if __name__ == "__main__":
    query = "SELECT * FROM era5_hourly_data LIMIT 10"
    qid = run_query(query)
    status = wait_for_results(qid)
    print(f"✅ Athena query finished with status: {status}")
