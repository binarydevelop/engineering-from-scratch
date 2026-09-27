"""
Broken implementation demonstrating the flaw in lab-10-small-files-partition-explosion.
"""
def get_partition_path(user_id, minute):
    return f"users/{user_id}/minute={minute}/data.parquet" # Millions of 100-byte files!
