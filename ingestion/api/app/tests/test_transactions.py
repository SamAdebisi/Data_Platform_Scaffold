import json, jwt, base64
from httpx import AsyncClient
from app.main import api
def make_token():
    return jwt.encode({"iss":"local","aud":"ingestion"}, "secret", algorithm="HS256")
async def test_ingest_ok():
    token = make_token()
    payload = {"txn_id":"t1","auth_id":"a1","customer_id":"c1","card_pan_token":"tok","amount":1.23,"currency":"EUR","mcc":"5812","country":"FI","device_id":"d1","channel":"card_not_present","ts":1,"status":"auth"}
    async with AsyncClient(app=api, base_url="http://test") as ac:
        r = await ac.post("/ingest/transactions", headers={"Authorization":f"Bearer {token}","Idempotency-Key":"x"}, content=json.dumps(payload))
        assert r.status_code==200
        assert r.json()["status"] in ("ok","duplicate")
