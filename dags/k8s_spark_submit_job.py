from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

from kubernetes.client import models as k8s


with DAG(
    dag_id="k8s_spark_submit_demo",
    start_date=datetime(2026, 7, 7),
    schedule=None,
    catchup=False,
) as dag:

    spark_submit = KubernetesPodOperator(
        task_id="spark_submit",
        name="spark-submit-demo",
        namespace="airflow",
        image="rtlabsipr/pyspark-submit-demo:1.0",
        cmds=["spark-submit"],
        arguments=[
            "--master",
            "local[*]",
            "--driver-memory",
            "1g",
            "--executor-memory",
            "1g",
            "--executor-cores",
            "2",
            "--conf",
            "spark.sql.shuffle.partitions=4",
            "--conf",
            "spark.app.name=AirflowSparkDemo",
            "/app/sparksubmitjob.py",
        ],        
        container_resources=k8s.V1ResourceRequirements(
            requests={
                "cpu": "2",
                "memory": "2Gi",
            },
            limits={
                "cpu": "2",
                "memory": "2Gi",
            },
        ),
        get_logs=True,
        is_delete_operator_pod=True,
    )
