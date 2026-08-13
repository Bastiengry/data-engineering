import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count, round

def main():
    # 1. Initialisation de la Session Spark (AVEC le driver JDBC PostgreSQL)
    spark = SparkSession.builder \
        .appName("SalesDataProcessing") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
        .getOrCreate()

    # Masquer les logs verbeux
    spark.sparkContext.setLogLevel("WARN")
    print("=== DÉBUT DU TRAITEMENT DES VENTES ===")

    # 2. Chemin du fichier adapté au conteneur Airflow
    input_path = "/opt/airflow/data/sales.csv"

    if not os.path.exists(input_path):
        print(f"Erreur : Le fichier {input_path} n'existe pas.")
        return

    # 3. Lecture du fichier CSV
    print(f"Lecture du fichier : {input_path}")
    df_raw = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(input_path)

    # 4. Transformations des données
    df_transformed = df_raw \
        .withColumn("line_total", col("quantity") * col("price")) \
        .groupBy("product_id") \
        .agg(
            _sum("quantity").alias("total_quantity"),
            round(_sum("line_total"), 2).alias("total_revenue"),
            count("product_id").alias("transaction_count")
        )

    print("--- Résultat de la transformation ---")
    df_transformed.show()

    # 5. Configuration JDBC pour écriture dans postgres-datamart
    jdbc_url = "jdbc:postgresql://postgres-datamart:5432/datamart"
    db_properties = {
        "user": "datamart",
        "password": "datamart",
        "driver": "org.postgresql.Driver"
    }

    # 6. Écriture dans la base PostgreSQL
    print("Écriture dans la base PostgreSQL (Datamart)...")
    df_transformed.write \
        .jdbc(url=jdbc_url, table="sales_summary", mode="overwrite", properties=db_properties)

    print("=== TRAITEMENT TERMINÉ AVEC SUCCÈS ===")
    spark.stop()

if __name__ == "__main__":
    main()