from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
with DAG("reverse_etl_sync", start_date=datetime(2024,1,1), schedule="*/10 * * * *", catchup=False) as dag:
    run = BashOperator(task_id="airbyte_sync", bash_command="python /project/reverse_etl/airbyte/run_connection.py")
