import os, json, io, datetime as dt
from confluent_kafka import Consumer, KafkaException
import boto3, pyarrow as pa, pyarrow.parquet as pq
import time 
from fastavro import parse_schema, validate
from .lib import process_batch 

SCHEMA = parse_schema(json.load(open(os.path.join(os.path.dirname(__file__),"../../kafka/schema_registry/transaction_v1.avsc"))))
# KAFKA = os.getenv("KAFKA_BROKERS","localhost:9092")
# TOPIC = os.getenv("KAFKA_TOPIC","txn.raw.v1")
# S3_EP = os.getenv("S3_ENDPOINT","http://localhost:9000")
S3_KEY = os.getenv("S3_ACCESS_KEY","minio")
S3_SEC = os.getenv("S3_SECRET_KEY","minio123")
# BUCKET = os.getenv("BRONZE_BUCKET","bronze")
BROKERS = os.getenv("KAFKA_BROKERS", "redpanda:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "txn.raw.v1")
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://minio:9000")
BUCKET = os.getenv("BRONZE_BUCKET", "bronze")
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
    consumer = Consumer(
        {
            "bootstrap.servers": BROKERS,
            "group.id": "txn_bronze_cg",
            "enable.auto.commit": False,
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe([TOPIC])
    s3 = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    batch = []
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
    while True:
        msg = consumer.poll(0.5)
        if msg is None:
            if batch:
                process_batch(batch, s3, BUCKET, prefix="", commit=lambda _: consumer.commit(asynchronous=False))
                batch = []
            continue
        if msg.error():
            continue
        batch.append(msg)
        if len(batch) >= BATCH_SIZE:
            process_batch(batch, s3, BUCKET, prefix="", commit=lambda _: consumer.commit(asynchronous=False))
            batch = []
        time.sleep(0.01)
if __name__=="__main__": 
    main()

