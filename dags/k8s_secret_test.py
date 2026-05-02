from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import V1SecretKeySelector, V1EnvVar, V1EnvVarSource

with DAG(
    dag_id="k8s_secret_test",
    start_date=datetime(2026, 5, 1),
    schedule=None,
    catchup=False,
) as dag:

    test_secret = KubernetesPodOperator(
        task_id="read_secret",
        name="secret-test-pod",
        namespace="airflow",
        image="python:3.11-slim",
        cmds=["python", "-c"],
        arguments=[
            "import os; "
            "print('SECRET VALUE:', os.getenv('MY_API_KEY'))"
        ],
        env_vars=[
            V1EnvVar(
                name="MY_API_KEY",
                value_from=V1EnvVarSource(
                    secret_key_ref=V1SecretKeySelector(
                        name="demo-secret",
                        key="MY_API_KEY",
                    )
                ),
            )
        ],
        get_logs=True,
        is_delete_operator_pod=False,
    )
