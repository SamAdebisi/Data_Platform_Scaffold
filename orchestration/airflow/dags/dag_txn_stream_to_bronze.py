from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
def run_consumer():
    subprocess.check_call(["python","/opt/airflow/dags/../..//streaming/consumers/txn_to_bronze/main.py"])
with DAG("txn_stream_to_bronze", start_date=datetime(2024,1,1), schedule="@continuous", catchup=False) as dag:
    PythonOperator(task_id="consume_and_land", python_callable=run_consumer)
