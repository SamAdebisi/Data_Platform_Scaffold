-- Minimal export from DuckDB reading Bronze Parquet in MinIO
SELECT txn_id,
       customer_id,
       amount,
       currency,
       country,
       ts
FROM read_parquet('s3://bronze/transactions/**/*.parquet');
