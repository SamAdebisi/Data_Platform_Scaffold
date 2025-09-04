select * 
    from (
        select null::varchar as event_id, 
                null::varchar as txn_id, 
                null::varchar as rule_id, 
                'v0' as model_version, 
                0.0 as score, 
                'allow' as decision, 
                current_timestamp as ts
                ) 
                where 1=0
