"""
Resilient, production-ready solution for lab-04-cartesian-product-join-explosion.
"""
# Fixed: Deduplicate dimension on surrogate key / current flag before joining
def join_orders_users(orders, users):
    latest_users = {u["user_id"]: u for u in users if u.get("is_current", True)}
    out = []
    for o in orders:
        u = latest_users.get(o["user_id"], {})
        out.append({**o, "user_name": u.get("name", "UNKNOWN")})
    return out
