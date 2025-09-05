from __future__ import annotations
import os, requests

AIRBYTE_URL = os.getenv("AIRBYTE_URL", "http://localhost:8001/api")
AIRBYTE_JOB_ID = os.getenv("AIRBYTE_JOB_ID", "")
AIRBYTE_TOKEN = os.getenv("AIRBYTE_TOKEN", "")


def trigger_sync() -> dict:
    # Why: placeholder to keep interface stable for later real integration
    if not AIRBYTE_JOB_ID:
        return {"status": "skipped"}
    headers = {"Authorization": f"Bearer {AIRBYTE_TOKEN}"} if AIRBYTE_TOKEN else {}
    try:
        r = requests.post(f"{AIRBYTE_URL}/v1/jobs/sync", json={"jobId": AIRBYTE_JOB_ID}, headers=headers, timeout=10)
        return {"status": "ok", "code": r.status_code}
    except Exception as e:
        return {"status": "error", "error": str(e)}
