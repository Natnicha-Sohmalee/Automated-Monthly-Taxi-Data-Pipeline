from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scripts.extract_bronze import move_new_file_to_bronze
from scripts.transform_silver import clean_data
from scripts.build_gold import build_gold

with DAG(
    dag_id="monthly_taxi_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id="extract_bronze",
        python_callable=move_new_file_to_bronze
    )

    transform = PythonOperator(
        task_id="transform_silver",
        python_callable=clean_data,
        op_args=[
            "{{ ti.xcom_pull(task_ids='extract_bronze') }}"
        ]
    )

    gold = PythonOperator(
        task_id="build_gold",
        python_callable=build_gold,
        op_args=[
            "{{ ti.xcom_pull(task_ids='transform_silver') }}"
        ]
    )

    extract >> transform >> gold