"""
Broken implementation demonstrating the flaw in lab-04-cartesian-product-join-explosion.
"""
# Broken: Non-unique join key causes Cartesian explosion
def join_orders_users(orders, users):
    out = []
    for o in orders:
        for u in users:
            if o["user_id"] == u["user_id"]: # Duplicate user records multiply order!
                out.append({**o, **u})
    return out
