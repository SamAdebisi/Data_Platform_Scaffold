from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
with DAG("compliance_daily", start_date=datetime(2024,1,1), schedule="0 3 * * *", catchup=False) as dag:
    run = BashOperator(task_id="run_psd2", bash_command="python /project/compliance/delivery/job_runner.py daily")
