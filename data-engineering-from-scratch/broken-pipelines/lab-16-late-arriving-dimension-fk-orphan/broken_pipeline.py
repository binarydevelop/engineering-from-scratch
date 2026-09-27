"""
Broken implementation demonstrating the flaw in lab-16-late-arriving-dimension-fk-orphan.
"""
def resolve_customer(fact, dim_customers):
    return dim_customers[fact["user_id"]] # KeyError if customer not arrived yet!
