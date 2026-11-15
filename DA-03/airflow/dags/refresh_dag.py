from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="supply_chain_hourly_refresh",
    start_date=datetime(2026, 11, 1),
    schedule="@hourly",
    catchup=False,
    tags=["capstone"],
) as dag:
    refresh_inventory = BashOperator(
        task_id="refresh_inventory",
        bash_command="python /opt/airflow/project/refresh.py",
    )