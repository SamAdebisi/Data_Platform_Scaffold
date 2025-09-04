FROM apache/airflow:2.9.3-python3.11
USER root

# Healthcheck needs curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Why: operators need Kafka, S3, Parquet, Redis, and crypto clients
RUN pip install --no-cache-dir \
    dbt-core dbt-duckdb \
    great_expectations requests \
    boto3 pyarrow s3fs \
    fastavro confluent-kafka redis pgpy paramiko
USER airflow
