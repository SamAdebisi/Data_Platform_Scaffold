from airflow import DAG
from airflow.sensors.python import PythonSensor
from datetime import datetime
import os
import boto3
import botocore

BUCKET = os.getenv("BRONZE_BUCKET", "bronze")
MARKER_KEY = os.getenv("GE_MARKER_KEY", "ge/checkpoints/last_success.marker")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def marker_exists() -> bool:
    s3 = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    try:
        s3.head_object(Bucket=BUCKET, Key=MARKER_KEY)
        return True
    except botocore.exceptions.ClientError:
        return False


with DAG(
    "ge_checkpoint_sensor",
    start_date=datetime(2024, 1, 1),
    schedule="@hourly",
    catchup=False,
    default_args={"retries": 0},
) as dag:
    PythonSensor(
        task_id="wait_for_ge_marker",
        python_callable=marker_exists,
        poke_interval=30,
        timeout=300,
        mode="poke",
    )
