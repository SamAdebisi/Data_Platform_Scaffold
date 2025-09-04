{% snapshot dim_customer_snapshot %}
{{
  config(
    target_schema='snapshots',
    strategy='check',
    unique_key='customer_id',
    check_cols=['hashed_email','country','segment','kyc_level']
  )
}}
select * 
    from (
        select null::varchar as customer_id, 
                null::varchar as hashed_email, 
                null::varchar as country, 
                null::varchar as segment, 
                null::varchar as kyc_level) 
                where 1=0
{% endsnapshot %}
