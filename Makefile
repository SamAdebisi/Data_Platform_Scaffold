SHELL := /bin/bash
export COMPOSE_PROJECT_NAME=enfuce
up: ; docker compose up -d --build
down: ; docker compose down -v
logs: ; docker compose logs -f --tail=200
seed: ; python3 samples/seed_ingest.py
ingest-sample: ; curl -s -X POST "http://localhost:8000/ingest/transactions" \
 -H "Authorization: Bearer $$JWT" \
 -H "Idempotency-Key: demo-1" -H "Content-Type: application/json" \
 --data-binary @samples/data/transactions_sample.jsonl | jq .
dbt-build: ; docker compose exec dbt bash -lc "dbt deps && dbt build --project-dir /project/transform/dbt/enflab --profiles-dir /project/transform/dbt"
ge-run: ; docker compose exec great_expectations great_expectations checkpoint run -c /project/observability/great_expectations/checkpoints/bronze_checkpoint.yml
test: ; docker compose exec ingestion_api pytest -q
fmt: ; docker compose exec ingestion_api ruff check --fix && black ingestion/api 
plan: ; docker compose exec terraform bash -lc "terraform -chdir=/project/infra/terraform/envs/aws-dev init && terraform -chdir=/project/infra/terraform/envs/aws-dev plan"
