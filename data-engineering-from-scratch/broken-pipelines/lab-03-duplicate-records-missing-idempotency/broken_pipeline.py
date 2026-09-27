"""
Broken implementation demonstrating the flaw in lab-03-duplicate-records-missing-idempotency.
"""
# Broken: Blind append
def load_records(db_table, batch):
    db_table.extend(batch) # Doubles rows on rerun!
