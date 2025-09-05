from __future__ import annotations


def _good_payload():
    return {
        "txn_id": "t-123",
        "auth_id": "a-123",
        "customer_id": "c-123",
        "card_pan_token": "tok-abc",
        "amount": 9.99,
        "currency": "EUR",
        "mcc": "5812",
        "country": "FI",
        "device_id": "d-1",
        "channel": "card_not_present",
        "ts": 1710000000,
        "status": "auth",
    }


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_missing_bearer(client):
    r = client.post("/ingest/transactions", json=_good_payload())
    assert r.status_code == 401


def test_invalid_token(client):
    r = client.post(
        "/ingest/transactions",
        json=_good_payload(),
        headers={"Authorization": "Bearer bad"},
    )
    assert r.status_code == 401


def test_avro_validation_fail(client, jwt_token):
    p = _good_payload()
    p.pop("txn_id")
    r = client.post(
        "/ingest/transactions",
        json=p,
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    assert r.status_code == 400


def test_ok_and_idempotent(client, jwt_token):
    p = _good_payload()
    h = {"Authorization": f"Bearer {jwt_token}"}
    r1 = client.post("/ingest/transactions", json=p, headers=h)
    r2 = client.post("/ingest/transactions", json=p, headers=h)
    assert r1.status_code == 200 and r1.json()["status"] == "ok"
    assert r2.status_code == 200 and r2.json()["status"] == "duplicate"
