from pathlib import Path
from datetime import datetime
from airflow import DAG
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

# Chemins vers le projet dbt
DBT_PROJECT_DIR = Path("/opt/airflow/dbt/my_clickhouse_project")
DBT_PROFILES_FILE = DBT_PROJECT_DIR / "profiles.yml"

default_args = {
    'owner': 'data-engineers',
    'start_date': datetime(2026, 1, 1),
    'retries': 0,
}

# Configuration du profil dbt via profiles.yml
profile_config = ProfileConfig(
    profile_name="clickhouse_profile",
    target_name="dev",
    profiles_yml_filepath=DBT_PROFILES_FILE,
)

with DAG(
    dag_id="03_transform_sales_dbt",
    default_args=default_args,
    schedule=None,
    catchup=False,
) as dag:

    # Transformations SQL via dbt (géré par Cosmos)
    dbt_transform = DbtTaskGroup(
        group_id="dbt_transformation",
        project_config=ProjectConfig(DBT_PROJECT_DIR),
        profile_config=profile_config,
        execution_config=ExecutionConfig(dbt_executable_path="/usr/local/bin/dbt"),
    )