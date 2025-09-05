from __future__ import annotations
import time
from typing import Annotated
from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from redis import Redis
from .config import REDIS_URL
from .auth import verify_jwt
from .validation.avro_validator import validate_record
from .producer import produce_transaction

api = FastAPI(title="Ingestion API", version="0.1.0")
redis = Redis.from_url(REDIS_URL, decode_responses=True)


class Txn(BaseModel):
    txn_id: str
    auth_id: str
    customer_id: str
    card_pan_token: str
    amount: float
    currency: str
    mcc: str
    country: str
    device_id: str
    channel: str  # enum in Avro; free-form here then validated
    ts: int
    status: str


@api.get("/health")
def health():
    return {"status": "ok"}


@api.post("/ingest/transactions")
def ingest_transaction(
    txn: Txn,
    authorization: Annotated[str | None, Header()] = None,
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authorization.split(" ", 1)[1]
    verify_jwt(token)

    data = txn.model_dump()
    if not validate_record(data):
        raise HTTPException(status_code=400, detail="avro validation failed")

    # Idempotency on txn_id for 24h
    if not redis.set(name=f"idemp:txn:{txn.txn_id}", value="1", nx=True, ex=86400):
        return {"status": "duplicate"}

    # Enrich with receive time for downstream partitioning if ts is missing
    data.setdefault("ingest_ts_ms", int(time.time() * 1000))
    produce_transaction(data)
    return {"status": "ok"}
