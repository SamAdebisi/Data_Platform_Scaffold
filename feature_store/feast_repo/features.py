from feast import FeatureView, Field, FileSource
from feast.types import Float32, Int64
from datetime import timedelta
transactions = FileSource(path="/project/samples/data/transactions_sample.parquet", timestamp_field="ts")
fraud_fv = FeatureView(
    name="fraud_features",
    entities=["transaction"],
    ttl=timedelta(hours=6),
    schema=[Field(name="velocity_1h", dtype=Int64), Field(name="mcc_risk", dtype=Float32)],
    online=True,
    source=transactions
)
