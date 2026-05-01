from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def hello():
    print("Hello from Kubernetes DAG 🚀")

with DAG(
    dag_id="hello_k8s",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    task = PythonOperator(
        task_id="say_hello",
        python_callable=hello,
    )