from feast import Entity
transaction = Entity(name="transaction", join_keys=["txn_id"])
customer = Entity(name="customer", join_keys=["customer_id"])
