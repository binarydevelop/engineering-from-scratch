"""
Resilient, production-ready solution for lab-16-late-arriving-dimension-fk-orphan.
"""
def resolve_customer(fact, dim_customers):
    # Route to placeholder surrogate key: -1 (UNKNOWN / Late Dimension)
    return dim_customers.get(fact["user_id"], {"customer_sk": -1, "name": "UNKNOWN_PENDING_DIM"})
