from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, length

# ----------------------------------------------------
# Create SparkSession
# ----------------------------------------------------
spark = (
    SparkSession.builder
    .appName("Airflow SparkSubmit Demo")
    .getOrCreate()
)

print("=" * 60)
print("Spark application started")
print("=" * 60)

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

print("\nOriginal Data")
df.show()

# ----------------------------------------------------
# Simple transformations
# ----------------------------------------------------

result = (
    df
    .withColumn("NAME_UPPER", upper(col("name")))
    .withColumn("NAME_LENGTH", length(col("name")))
)

print("\nTransformed Data")
result.show()

# ----------------------------------------------------
# Aggregation
# ----------------------------------------------------

summary = (
    df.groupBy("department")
      .avg("salary")
      .orderBy("department")
)

print("\nAverage salary by department")
summary.show()

# ----------------------------------------------------
# Count rows
# ----------------------------------------------------

print(f"\nTotal rows: {df.count()}")

print("\nSpark job finished successfully.")

spark.stop()
