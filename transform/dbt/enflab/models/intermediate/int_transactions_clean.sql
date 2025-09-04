with src as (select * from {{ ref('stg_transactions') }}), dedup as (
  select *, row_number() over(partition by txn_id, status order by ts desc) as rn
  from src
)
select * exclude(rn) from dedup where rn=1
