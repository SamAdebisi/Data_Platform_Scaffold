# Data Platform (MVP Scaffold)
Targets: ingestion, streaming, ELT with dbt, feature serving with Feast, compliance, reverse ETL, observability, and security.

## Quick start (local)
1) prerequisites: docker, docker-compose, make
2) cp env/dev/.env.sample env/dev/.env && edit as needed
3) make up
4) Ingest sample: make seed && make ingest-sample
5) Run ELT: make dbt-build
6) Check GE: make ge-run
7) Features API: http://localhost:8090/docs  (served by the ingestion_api container)
8) Airflow: http://localhost:8080  (user: airflow / pw: airflow)
9) Metabase: http://localhost:3000
10) Tear down: make down

## Notes
- Kafka: Redpanda at localhost:19092; topic txn.raw.v1
- Object store: MinIO at http://localhost:9000 (console :9001)
- Warehouse (local): DuckDB via dbt. Parquet lake in MinIO.
- The **txn stream → bronze** DAG relies on the new `./streaming` mount and S3/Kafka envs added above.

```
make up
make seed
make dbt-build
# make ge-run      # optional placeholder  # GE marker example (optional)
# open http://localhost:8090/docs   # Features API (served by features_api service)
python - <<'PY'
import boto3
s3=boto3.client('s3',endpoint_url='http://localhost:9000',aws_access_key_id='minio',aws_secret_access_key='minio123')
s3.put_object(Bucket='bronze',Key='ge/checkpoints/last_success.marker',Body=b'ok')
print('marker written')
PY
```
