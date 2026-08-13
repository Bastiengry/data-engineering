from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data-engineers',
    'start_date': datetime(2026, 1, 1),
    'retries': 0,
}

with DAG(
    '01_simulate_sales',
    default_args=default_args,
    schedule_interval=None,  # Déclenchement manuel (ou ex: '*/10 * * * *' pour toutes les 10 min)
    catchup=False,
    tags=['simulation', 'generator'],
) as dag:

    run_simulation = BashOperator(
        task_id='run_simulate_sales_script',
        bash_command='python /opt/airflow/scripts/simulate_sales.py', # <--- Appelle ton script renommé
    )