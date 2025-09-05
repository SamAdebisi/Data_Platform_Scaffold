{% snapshot transactions_snapshot %}
{{
  config(
    target_schema='snapshots',
    unique_key='txn_id',
    strategy='timestamp',
    updated_at='ts'
  )
}}
SELECT * FROM {{ ref('transactions_silver') }}
{% endsnapshot %}
