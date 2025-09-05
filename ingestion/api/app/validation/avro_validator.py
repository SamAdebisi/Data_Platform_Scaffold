import json
from fastavro import parse_schema, validate
from typing import Any, Dict
with open(__file__.replace("avro_validator.py", "../schemas/transaction_v1.avsc")) as f:
    AVRO_SCHEMA = parse_schema(json.load(f))
def validate_transaction(rec: Dict[str, Any]) -> None:
    if not validate(rec, AVRO_SCHEMA): 
        raise ValueError("schema validation failed")
