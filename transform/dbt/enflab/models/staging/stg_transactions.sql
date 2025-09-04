with base as (
  select * from read_parquet('s3://bronze/transactions/*.parquet')
)
select
  txn_id, auth_id, customer_id,
  cast(amount as double) as amount,
  upper(currency) as currency,
  mcc, country, device_id, channel, ts, status,
  card_pan_token
from base
where txn_id is not null and customer_id is not null
