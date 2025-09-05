import os, json, io, datetime as dt
from confluent_kafka import Consumer, KafkaException
import boto3, pyarrow as pa, pyarrow.parquet as pq
import time 
from fastavro import parse_schema, validate
from .lib import process_batch 

# Support running as a script or as a package module
try:  # when executed via `python -m streaming.consumers.txn_to_bronze.main`
    from .lib import process_batch  # type: ignore
except Exception:  # when executed via `python main.py`
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parent))
    from lib import process_batch  # type: ignore

SCHEMA = parse_schema(json.load(open(os.path.join(os.path.dirname(__file__),"../../kafka/schema_registry/transaction_v1.avsc"))))
KAFKA = os.getenv("KAFKA_BROKERS", "redpanda:9092")
TOPIC = os.getenv("KAFKA_TOPIC","txn.raw.v1")
S3_EP = os.getenv("S3_ENDPOINT", "http://minio:9000")
# S3_EP = os.getenv("S3_ENDPOINT","http://localhost:9000")
S3_KEY = os.getenv("S3_ACCESS_KEY","minio")
S3_SEC = os.getenv("S3_SECRET_KEY","minio123")
# BUCKET = os.getenv("BRONZE_BUCKET","bronze")
BROKERS = os.getenv("KAFKA_BROKERS", "redpanda:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "txn.raw.v1")
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://minio:9000")   # container-internal URL
BUCKET = os.getenv("BRONZE_BUCKET", "bronze")
AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "minio")
AWS_SEC = os.getenv("AWS_SECRET_ACCESS_KEY", "minio123")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "minio")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minio123")

def write_parquet_s3(records):
    table = pa.Table.from_pylist(records)
    buf = io.BytesIO()
    pq.write_table(table, buf, compression="snappy")
    s3 = boto3.client("s3", endpoint_url=S3_EP, aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SEC)
    key = f"transactions/dt={dt.date.today().isoformat()}/part-{int(dt.datetime.utcnow().timestamp())}.parquet"
    s3.put_object(Bucket=BUCKET, Key=key, Body=buf.getvalue())
    
def main():
    c = Consumer({
        "bootstrap.servers": KAFKA, 
        "group.id": "txn-bronze", 
        "auto.offset.reset": "earliest", 
        "enable.auto.commit": False
        })
    c.subscribe([TOPIC])
    batch = []
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                if batch:
                    write_parquet_s3(batch)
                    c.commit()
                    batch = []
                continue
            if msg.error():
                raise KafkaException(msg.error())
            rec = json.loads(msg.value().decode("utf-8"))
            if not validate(rec, SCHEMA):
                continue
            batch.append(rec)
            if len(batch) >= 500:
                write_parquet_s3(batch)
                c.commit()
                batch = []
    finally:
        if batch:
            write_parquet_s3(batch)
            c.commit()
        c.close()
        

if __name__=="__main__": 
    main()

