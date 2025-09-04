from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess, os

def run_consumer():
    # Why: ensure env points to in-cluster services
    env = {**os.environ}
    subprocess.check_call(
        ["python","/opt/airflow/streaming/consumers/txn_to_bronze/main.py"],
        env=env
    )

with DAG("txn_stream_to_bronze", start_date=datetime(2024,1,1), schedule="@continuous", catchup=False) as dag:
    PythonOperator(task_id="consume_and_land", python_callable=run_consumer)
    