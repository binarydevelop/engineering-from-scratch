"""
Broken implementation demonstrating the flaw in lab-20-missing-partition-pruning-full-table-scan.
"""
# Inefficient: Function wraps partition column
def generate_filter_broken(date_str):
    return f"WHERE date_trunc('day', event_time) = '{date_str}'"
