from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

def main():
    spark = SparkSession.builder \
        .appName("ProcessSalesToClickHouse") \
        .config("spark.jars.packages", "com.clickhouse:clickhouse-jdbc:0.6.0,org.apache.httpcomponents.client5:httpclient5:5.2.1") \
        .getOrCreate()

    # Définition du schéma correspondant au CSV généré
    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("store", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("price", DoubleType(), True)
    ])

    # 1. Lecture du fichier CSV généré
    input_path = "/opt/airflow/data/sales.csv"
    df = spark.read.csv(input_path, header=True, schema=schema)

    # 2. Transformation : Calcul du montant total par ligne puis agrégation
    df_transformed = df.withColumn("total_amount", F.col("quantity") * F.col("price")) \
                       .groupBy("store", "product_id") \
                       .agg(
                           F.sum("quantity").alias("total_quantity"),
                           F.round(F.sum("total_amount"), 2).alias("total_revenue")
                       )

    # 3. Écriture dans ClickHouse
    clickhouse_url = "jdbc:ch://clickhouse-datamart:8123/datamart"

    df_transformed.write \
        .format("jdbc") \
        .option("url", clickhouse_url) \
        .option("dbtable", "sales_summary") \
        .option("user", "datamart") \
        .option("password", "datamart") \
        .option("createTableOptions", "ENGINE = MergeTree() ORDER BY (store, product_id)") \
        .option("driver", "com.clickhouse.jdbc.ClickHouseDriver") \
        .option("batchsize", "100000") \
        .mode("append") \
        .save()

    print("✅ Données Spark écrites avec succès dans ClickHouse")
    spark.stop()

if __name__ == "__main__":
    main()