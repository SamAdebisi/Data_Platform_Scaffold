import os
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS","localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC","txn.raw.v1")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__),"schemas","transaction.avsc")
REDIS_URL = os.getenv("REDIS_URL","redis://localhost:6379/0")
JWT_ISSUER = os.getenv("JWT_ISSUER","local")
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE","ingestion")
JWT_PUBLIC_KEY_BASE64 = os.getenv("JWT_PUBLIC_KEY_BASE64","")
