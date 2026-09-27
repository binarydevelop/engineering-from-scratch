"""
Broken implementation demonstrating the flaw in lab-25-iceberg-metadata-snapshot-mismatch.
"""
def commit_snapshot_naive(current_v, new_v):
    return new_v # Overwrites blindly without validating parent snapshot
