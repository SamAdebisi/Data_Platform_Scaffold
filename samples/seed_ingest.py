# import json, os, requests, jwt
# url=os.getenv("INGEST_URL","http://localhost:8000/ingest/transactions")
# token=jwt.encode({"iss":"local","aud":"ingestion"}, "secret", algorithm="HS256")
# with open("samples/data/transactions_sample.jsonl") as f:
#     data=f.read()
# r=requests.post(url, headers={"Authorization":f"Bearer {token}","Idempotency-Key":"seed-1"}, data=data)
# print(r.status_code, r.text)


import os, json, time, random
import requests

INGEST_URL = os.getenv("INGEST_URL", "http://localhost:8000/ingest/transactions")
JWT = os.getenv("JWT") or __import__("jwt").encode({"iss":"local","aud":"ingestion"}, "secret", algorithm="HS256")

sample = {
  "txn_id": "t-" + str(int(time.time()*1000)),
  "auth_id": "a-" + str(random.randint(1, 999999)).zfill(6),
  "customer_id": "c-" + str(random.randint(1, 99)).zfill(4),
  "card_pan_token": "tok-" + str(random.randint(1, 9999)).zfill(4),
  "amount": round(random.uniform(1, 100), 2),
  "currency": "EUR",
  "mcc": random.choice(["5812","5411","7995"]),
  "country": random.choice(["FI","SE","NO"]),
  "device_id": "d-" + str(random.randint(1,9)),
  "channel": random.choice(["card_present","card_not_present"]),
  "ts": int(time.time()),
  "status": "auth"
}

r = requests.post(INGEST_URL, json=sample, headers={"Authorization": f"Bearer {JWT}"})
print(r.status_code, r.text)
