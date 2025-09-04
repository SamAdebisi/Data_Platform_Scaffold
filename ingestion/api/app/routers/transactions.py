import json, os, time
from fastapi import APIRouter, Request, Header, HTTPException
from confluent_kafka import Producer
from redis import Redis
from ..auth import verify_jwt
from ..validation.avro_validator import validate_transaction
from ..config import KAFKA_BROKERS, KAFKA_TOPIC, REDIS_URL
router = APIRouter()
producer = Producer({"bootstrap.servers": KAFKA_BROKERS})
redis = Redis.from_url(REDIS_URL, decode_responses=True)
@router.post("/ingest/transactions")
async def ingest(request: Request, idempotency_key: str = Header(default=""), payload=verify_jwt):
    body = await request.body()
    if not idempotency_key: raise HTTPException(status_code=400, detail="Idempotency-Key required")
    if redis.setnx(f"idemp:{idempotency_key}", int(time.time())) is False:
        return {"status":"duplicate","idempotency_key":idempotency_key}
    redis.expire(f"idemp:{idempotency_key}", 86400)
    records = [json.loads(line) for line in body.splitlines() if line.strip()]
    for rec in records:
        validate_transaction(rec)
        producer.produce(KAFKA_TOPIC, json.dumps(rec).encode("utf-8"))
    producer.flush()
    return {"status":"ok","count":len(records)}
