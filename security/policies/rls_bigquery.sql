-- Example row access policy
CREATE ROW ACCESS POLICY rlp_customer ON `dataset.f_transactions`
GRANT TO ("group:data_analysts@example.com")
FILTER USING (customer_id IN UNNEST(session_user_attributes.customer_ids));
