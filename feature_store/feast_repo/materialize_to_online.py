import json, os, pyarrow.parquet as pq, redis
from datetime import datetime, timezone
r = redis.from_url(os.getenv("REDIS_URL","redis://redis:6379/0"), decode_responses=True)
table = pq.read_table("/project/samples/data/transactions_sample.parquet").to_pylist()
for rec in table:
    features={"velocity_1h":1,"mcc_risk":0.1}
    r.setex(f"feast:txn:{rec['txn_id']}", 6*3600, json.dumps(features))
