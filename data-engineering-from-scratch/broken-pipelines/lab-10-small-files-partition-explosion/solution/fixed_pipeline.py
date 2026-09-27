"""
Resilient, production-ready solution for lab-10-small-files-partition-explosion.
"""
def get_partition_path(event_date):
    # Coarse partition key: Date level + compacted batches
    return f"events/date={event_date}/data.parquet"
