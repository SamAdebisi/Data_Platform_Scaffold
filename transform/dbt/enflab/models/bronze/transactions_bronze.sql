{{ config(materialized='table') }}
SELECT *
FROM read_parquet('s3://bronze/transactions/**/*.parquet');
