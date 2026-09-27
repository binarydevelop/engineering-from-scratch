"""
Resilient, production-ready solution for lab-18-scd2-overlapping-effective-dates.
"""
def update_scd2_fixed(records, new_record):
    for r in records:
        if r["user_id"] == new_record["user_id"] and r.get("is_current", True):
            r["is_current"] = False
            r["valid_to"] = new_record["valid_from"]
    records.append(new_record)
