import sys
sys.path.append("/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from scripts.extract import extract 
from scripts.transform import transform
from scripts.load import load

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id = "weather_etl_pipeline",
    default_args = default_args,
    start_date = datetime(2024, 1, 1),
    schedule_interval = "@hourly",
    catchup = False,
) as dag:

    extract_task = PythonOperator(
        task_id = "extract",
        python_callable = extract
    )

    transform_task = PythonOperator(
        task_id = "transform",
        python_callable = transform
    )

    load_task = PythonOperator(
        task_id = "load",
        python_callable = load
    )

extract_task >> transform_task >> load_task