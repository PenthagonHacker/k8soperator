from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime

default_args = {
    "start_date": datetime(2026, 5, 5),
    "retries": 0,
}

with DAG(
    dag_id="k8s_pyspark_test",
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["pyspark"],
) as dag:

    run_pyspark = KubernetesPodOperator(
        namespace="airflow",
        name="pyspark-job",
        task_id="run_pyspark",
        image="octoenergy/pyspark:3.5.2",
        cmds=["bash", "-c"],
        arguments=[
            """
            python - << 'EOF'
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Airflow-K8s-PySpark") \
    .getOrCreate()

data = [
    ("Alice", 34),
    ("Bob", 45),
    ("Charlie", 29),
    ("Diana", 40)
]

df = spark.createDataFrame(data, ["name", "age"])

print("📊 Original DataFrame:")
df.show()

df_filtered = df.filter(df.age > 35)

print("🔥 Filtered (age > 35):")
df_filtered.show()

print("✅ PySpark job finished successfully")

spark.stop()
EOF
            """
        ],
        get_logs=True,
        is_delete_operator_pod=True,
    )
