from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
with DAG("silver_to_gold", start_date=datetime(2024,1,1), schedule="@hourly", catchup=False) as dag:
    build = BashOperator(task_id="dbt_build", bash_command="dbt build --project-dir /project/transform/dbt/enflab --profiles-dir /project/transform/dbt --select tag:silver_to_gold")
