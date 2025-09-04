# Data Platform (MVP Scaffold)
Targets: ingestion, streaming, ELT with dbt, feature serving with Feast, compliance, reverse ETL, observability, and security.

## Quick start (local)
1) prerequisites: docker, docker-compose, make
2) cp env/dev/.env.sample env/dev/.env && edit as needed
3) make up
4) Ingest sample: make seed && make ingest-sample
5) Run ELT: make dbt-build
6) Check GE: make ge-run
7) Fraud API: http://localhost:8090/docs
8) Airflow: http://localhost:8080  (user: airflow / pw: airflow)
9) Metabase: http://localhost:3000
10) Tear down: make down

## Notes
- Kafka: Redpanda at localhost:19092; topic txn.raw.v1
- Object store: MinIO at http://localhost:9000 (console :9001)
- Warehouse (local): DuckDB via dbt. Parquet lake in MinIO.
