"""
Resilient, production-ready solution for lab-03-duplicate-records-missing-idempotency.
"""
# Fixed: Deduplicated upsert using unique business key
def load_records(db_table, batch):
    # Upsert by ID
    existing_ids = {r["id"] for r in db_table}
    for item in batch:
        if item["id"] in existing_ids:
            # Update existing
            for idx, r in enumerate(db_table):
                if r["id"] == item["id"]:
                    db_table[idx] = item
        else:
            db_table.append(item)
            existing_ids.add(item["id"])
