from fastapi import APIRouter, HTTPException
from redis import Redis
import json, os
router = APIRouter()
redis = Redis.from_url(os.getenv("REDIS_URL","redis://localhost:6379/0"), decode_responses=True)
@router.get("/features/{txn_id}")
def get_features(txn_id: str):
    s = redis.get(f"feast:txn:{txn_id}")
    if not s: raise HTTPException(404, "not found")
    return json.loads(s)
