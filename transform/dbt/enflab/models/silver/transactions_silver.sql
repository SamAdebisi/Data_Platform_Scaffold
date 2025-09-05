{{ config(materialized='table') }}
WITH ranked AS (
    SELECT *, row_number() OVER (PARTITION BY txn_id ORDER BY ts DESC) AS rn
    FROM {{ ref('transactions_bronze') }}
)
SELECT * EXCLUDE(rn)
FROM ranked
WHERE rn = 1;
