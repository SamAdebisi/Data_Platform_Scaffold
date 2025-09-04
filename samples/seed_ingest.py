import json, os, requests, jwt
url=os.getenv("INGEST_URL","http://localhost:8000/ingest/transactions")
token=jwt.encode({"iss":"local","aud":"ingestion"}, "secret", algorithm="HS256")
with open("samples/data/transactions_sample.jsonl") as f:
    data=f.read()
r=requests.post(url, headers={"Authorization":f"Bearer {token}","Idempotency-Key":"seed-1"}, data=data)
print(r.status_code, r.text)