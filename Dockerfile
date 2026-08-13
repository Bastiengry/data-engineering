FROM apache/airflow:2.8.1-python3.9

USER root

# Installation de Java (JRE) pour PySpark
RUN apt-get update \
  && apt-get install -y --no-install-recommends default-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow

# Installation des paquets Python
RUN pip install --no-cache-dir pyspark psycopg2-binary