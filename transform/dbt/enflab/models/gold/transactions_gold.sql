{{ config(materialized='table') }}
SELECT country,
       currency,
       count(*) AS txn_cnt,
       sum(amount) AS amount_sum
FROM {{ ref('transactions_silver') }}
GROUP BY 1,2;
