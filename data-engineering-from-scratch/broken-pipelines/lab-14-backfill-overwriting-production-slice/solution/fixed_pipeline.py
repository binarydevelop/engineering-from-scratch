"""
Resilient, production-ready solution for lab-14-backfill-overwriting-production-slice.
"""
def backfill_slice_safe(target_db, partition_date, new_data):
    # Isolated partition replacement
    target_db[:] = [r for r in target_db if r.get("date") != partition_date]
    target_db.extend(new_data)
