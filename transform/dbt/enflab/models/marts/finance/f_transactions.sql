select
  txn_id, auth_id, customer_id, mcc, country, device_id, channel,
  ts as txn_ts, amount, currency, status,
  null as risk_score, 0 as dispute_flag, 0 as chargeback_flag
from {{ ref('int_transactions_clean') }}
