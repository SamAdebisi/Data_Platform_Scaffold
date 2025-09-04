from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
with DAG("fraud_feature_build", start_date=datetime(2024,1,1), schedule="*/15 * * * *", catchup=False) as dag:
    feat = BashOperator(task_id="feast_materialize", bash_command="python /project/feature_store/feast_repo/materialize_to_online.py")
