from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

from kubernetes.client import models as k8s


with DAG(
    dag_id="k8s_spark_submit_demo",
    start_date=datetime(2026, 7, 7),
    schedule_interval=None,
    catchup=False,
) as dag:

    spark_submit = KubernetesPodOperator(
        task_id="spark_submit",
        name="spark-submit-demo",
        namespace="pd-airflow-prod",
        config_file="/home/airflow/.kube/config",
        image="rtlabsipr/pyspark-submit-demo:1.0",
        cmds=["spark-submit"],
        arguments=[
            "/app/job.py",
        ],
        container_resources=k8s.V1ResourceRequirements(
            requests={
                "cpu": "500m",
                "memory": "512Mi",
            },
            limits={
                "cpu": "1",
                "memory": "1Gi",
            },
        ),
        get_logs=True,
        is_delete_operator_pod=True,
    )
