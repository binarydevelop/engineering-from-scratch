"""
Broken implementation demonstrating the flaw in lab-14-backfill-overwriting-production-slice.
"""
def backfill_slice_broken(target_db):
    target_db.clear() # Catastrophic: deletes all partitions!
