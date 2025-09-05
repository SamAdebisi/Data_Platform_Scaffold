-- Row level security example templates
-- Postgres
-- ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY tenant_isolation ON transactions USING (tenant_id = current_setting('app.tenant_id')::text);

-- BigQuery
-- CREATE ROW ACCESS POLICY tenant_policy ON dataset.transactions
-- GRANT TO ("group:tenant-a@example.com")
-- FILTER USING (tenant_id = 'tenant-a');

-- Snowflake
-- CREATE ROW ACCESS POLICY tenant_policy AS (tenant_id STRING) RETURNS BOOLEAN -> tenant_id = CURRENT_ROLE();
