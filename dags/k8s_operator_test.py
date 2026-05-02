from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id="k8s_operator_test",
    start_date=datetime(2026, 5, 1),
    schedule=None,
    catchup=False,
) as dag:

    test_k8s = KubernetesPodOperator(
        task_id="run_test_pod",
        name="k8s-test-pod",
        namespace="airflow",

        # use public image (no registry headaches)
        image="python:3.11-slim",

        cmds=["python", "-c"],
        arguments=["import time; print('start'); time.sleep(30); print('end')"],

        get_logs=True,
        is_delete_operator_pod=True,
    )
