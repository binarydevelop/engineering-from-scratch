"""
Resilient, production-ready solution for lab-20-missing-partition-pruning-full-table-scan.
"""
# Efficient: SARGable predicate matches physical partition key directly
def generate_filter_pruned(date_str):
    return f"WHERE partition_date = '{date_str}'"
