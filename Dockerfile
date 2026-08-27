FROM apache/airflow:2.8.1-python3.9

USER root

# Installation de Java pour PySpark
RUN apt-get update \
  && apt-get install -y --no-install-recommends default-jre-headless \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

USER airflow

# Mise à jour de pip et installation des dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "pyspark>=3.4.0,<3.5.0" \
    psycopg2-binary \
    dbt-core \
    dbt-clickhouse \
    astronomer-cosmos