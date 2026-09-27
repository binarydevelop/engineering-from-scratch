"""
Resilient, production-ready solution for lab-25-iceberg-metadata-snapshot-mismatch.
"""
def commit_snapshot_optimistic(expected_parent, actual_parent, new_v):
    if expected_parent != actual_parent:
        raise ValueError("CONCURRENT_MODIFICATION_EXCEPTION: Snapshot conflict, retry required")
    return new_v
