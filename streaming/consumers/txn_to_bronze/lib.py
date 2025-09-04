"""Pure helpers for the txn → bronze consumer to enable unit testing."""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from typing import Callable, Iterable, Tuple

import pyarrow as pa
import pyarrow.parquet as pq


def partition_path(ts_iso: str) -> str:
    """Return dt=YYYY-MM-DD from an ISO timestamp. Accepts Z or offset."""
    dt = datetime.fromisoformat(ts_iso.replace("Z", "+00:00"))
    return f"dt={dt.date().isoformat()}"


def to_parquet_bytes(records: list[dict]) -> bytes:
    if not records:
        return b""
    table = pa.Table.from_pylist(records)
    sink = io.BytesIO()
    pq.write_table(table, sink)
    return sink.getvalue()


def upload_parquet_bytes(s3, bucket: str, key: str, body: bytes) -> None:
    if not body:
        return
    s3.put_object(Bucket=bucket, Key=key, Body=body)


def process_batch(
    messages: Iterable,
    s3,
    bucket: str,
    prefix: str,
    commit: Callable[[Tuple[str, int, int]], None] | None = None,
) -> int:
    records: list[dict] = []
    last_offset: Tuple[str, int, int] | None = None
    for msg in messages:
        payload = json.loads(msg.value().decode("utf-8"))
        records.append(payload)
        last_offset = (msg.topic(), msg.partition(), msg.offset())
    if not records:
        return 0
    ts = records[0].get("event_time") or records[0].get("ts") or datetime.now(timezone.utc).isoformat()
    part = partition_path(ts)
    key = f"{prefix}transactions/{part}/part-{int(datetime.now().timestamp())}.parquet"
    body = to_parquet_bytes(records)
    upload_parquet_bytes(s3, bucket, key, body)
    if commit and last_offset:
        commit(last_offset)
    return len(records)
