# import json
# from fastavro import parse_schema, validate
# from typing import Any, Dict
# with open(__file__.replace("avro_validator.py", "../schemas/transaction_v1.avsc")) as f:
#     AVRO_SCHEMA = parse_schema(json.load(f))
# def validate_transaction(rec: Dict[str, Any]) -> None:
#     if not validate(rec, AVRO_SCHEMA): 
#         raise ValueError("schema validation failed")

from __future__ import annotations
import json
import os
from fastavro import parse_schema, validate
from .config import SCHEMA_PATH

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    AVRO_SCHEMA = parse_schema(json.load(f))


def validate_record(record: dict) -> bool:
    # Why: strict schema in ingestion to avoid malformed downstream data
    return validate(record, AVRO_SCHEMA)
