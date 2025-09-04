import json, os, redis
from datetime import datetime, timezone
r = redis.from_url(os.getenv("REDIS_URL","redis://redis:6379/0"), decode_responses=True)
sample_path = "/project/samples/data/transactions_sample.jsonl"
with open(sample_path) as f:
    for line in f:
        if not line.strip():
            continue
        rec = json.loads(line)
        features = {"velocity_1h": 1, "mcc_risk": 0.1}
        # 6h TTL to mimic Feast online TTL
        r.setex(f"feast:txn:{rec['txn_id']}", 6*3600, json.dumps(features))