from __future__ import annotations
import json
from typing import Any, Dict
from confluent_kafka import Producer
from .config import KAFKA_BROKERS, KAFKA_TOPIC


def _producer() -> Producer:
    # Idempotence optional. Redpanda accepts these configs.
    return Producer(
        {
            "bootstrap.servers": KAFKA_BROKERS,
            "enable.idempotence": True,
            "linger.ms": 5,
            "acks": "all",
        }
    )


def produce_transaction(payload: Dict[str, Any]) -> None:
    p = _producer()
    key = str(payload.get("txn_id", ""))
    p.produce(KAFKA_TOPIC, key=key, value=json.dumps(payload).encode("utf-8"))
    p.flush(5)
