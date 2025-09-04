select
  t.txn_id,
  json('{"velocity_1h": 1, "mcc_risk": 0.1}') as feature_vector,
  to_timestamp(ts) as ts
from {{ ref('int_transactions_clean') }} t
