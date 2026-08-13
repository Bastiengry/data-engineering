from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data-engineers',
    'start_date': datetime(2026, 1, 1),
    'retries': 0,
}

with DAG(
    '02_process_sales',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['spark', 'etl'],
) as dag:

    submit_spark_job = BashOperator(
        task_id='submit_spark_job',
        bash_command='python /opt/airflow/spark/app/process_sales.py',
    )