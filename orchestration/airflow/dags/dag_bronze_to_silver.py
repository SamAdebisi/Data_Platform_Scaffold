from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
with DAG("bronze_to_silver", start_date=datetime(2024,1,1), schedule="@hourly", catchup=False) as dag:
    dbt = BashOperator(task_id="dbt_run", bash_command="dbt run --project-dir /project/transform/dbt/enflab --profiles-dir /project/transform/dbt --select tag:bronze_to_silver")
    ge  = BashOperator(task_id="ge_checkpoint", bash_command="great_expectations checkpoint run -c /observability/great_expectations/checkpoints/silver_checkpoint.yml")
    dbt >> ge
