from fastapi import FastAPI, HTTPException
import os, json, redis

app = FastAPI(title="Features API", version="0.1.0")
r = redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"), decode_responses=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/features/{txn_id}")
def get_features(txn_id: str):
    val = r.get(f"feast:txn:{txn_id}")
    if not val:
        raise HTTPException(status_code=404, detail="not found")
    return json.loads(val)
