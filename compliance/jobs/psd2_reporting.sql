select customer_id, 
count(*) as txn_count, 
sum(amount) as total_amount, max(ts) as last_ts 
    from f_transactions group by 1
