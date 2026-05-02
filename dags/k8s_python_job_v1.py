from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="k8s_python_job_v1",
    start_date=datetime(2026, 5, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_script = KubernetesPodOperator(
        task_id="run_python_script",
        name="run-python-script",
        namespace="airflow",
        image="my-python-job:latest",
        cmds=["python", "script.py"],
        get_logs=True,
        is_delete_operator_pod=True,
    )
