import json
from types import SimpleNamespace
from streaming.consumers.txn_to_bronze.lib import process_batch, partition_path, to_parquet_bytes


class FakeMsg:
    def __init__(self, payload: dict, topic="txn.raw.v1", partition=0, offset=1):
        self._payload = payload
        self._topic = topic
        self._partition = partition
        self._offset = offset

    def value(self):
        return json.dumps(self._payload).encode("utf-8")

    def topic(self):
        return self._topic

    def partition(self):
        return self._partition

    def offset(self):
        return self._offset


def test_partition_path():
    assert partition_path("2025-08-23T12:34:56Z") == "dt=2025-08-23"


def test_to_parquet_bytes_nonempty():
    body = to_parquet_bytes([{"a": 1}])
    assert isinstance(body, (bytes, bytearray)) and len(body) > 0


def test_commit_on_success(monkeypatch):
    put_calls = []

    class S3:
        def put_object(self, **kw):
            put_calls.append(kw)

    committed = {"n": 0}

    def commit(_last):
        committed["n"] += 1

    msgs = [FakeMsg({"txn_id": "1", "event_time": "2025-08-23T00:00:00Z", "amount": 10})]
    n = process_batch(msgs, S3(), bucket="bronze", prefix="", commit=commit)
    assert n == 1
    assert committed["n"] == 1
    assert len(put_calls) == 1


def test_no_commit_on_upload_failure():
    class S3:
        def put_object(self, **kw):
            raise RuntimeError("fail")

    committed = {"n": 0}

    def commit(_last):
        committed["n"] += 1

    msgs = [FakeMsg({"txn_id": "1", "event_time": "2025-08-23T00:00:00Z"})]
    try:
        process_batch(msgs, S3(), bucket="bronze", prefix="", commit=commit)
    except RuntimeError:
        pass
    assert committed["n"] == 0
