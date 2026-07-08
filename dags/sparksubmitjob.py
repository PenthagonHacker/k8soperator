from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, length

def log(message):
print("=" * 60, flush=True)
print(message, flush=True)
print("=" * 60, flush=True)

spark = (
SparkSession.builder
.appName("Airflow SparkSubmit Demo")
.getOrCreate()
)

try:
log("Spark application started")

```
print(f"Spark version: {spark.version}", flush=True)

# ----------------------------------------------------
# Sample data
# ----------------------------------------------------

data = [
    (1, "Alice", "Engineering", 5200),
    (2, "Bob", "Finance", 4300),
    (3, "Charlie", "Engineering", 6100),
    (4, "David", "Sales", 3900),
    (5, "Eva", "Finance", 4700),
]

columns = [
    "id",
    "name",
    "department",
    "salary",
]

df = spark.createDataFrame(data, columns)

print("\nOriginal Data", flush=True)
df.show(truncate=False)

print(f"Input row count: {df.count()}", flush=True)

# ----------------------------------------------------
# Transformations
# ----------------------------------------------------

result = (
    df
    .withColumn("NAME_UPPER", upper(col("name")))
    .withColumn("NAME_LENGTH", length(col("name")))
)

print("\nTransformed Data", flush=True)
result.show(truncate=False)

# ----------------------------------------------------
# Aggregation
# ----------------------------------------------------

summary = (
    df.groupBy("department")
    .avg("salary")
    .orderBy("department")
)

print("\nAverage salary by department", flush=True)
summary.show(truncate=False)

# ----------------------------------------------------
# Final validation
# ----------------------------------------------------

total_rows = result.count()

print(f"\nFinal processed rows: {total_rows}", flush=True)

log("Spark job finished successfully")
```

finally:
spark.stop()
print("Spark session stopped", flush=True)
