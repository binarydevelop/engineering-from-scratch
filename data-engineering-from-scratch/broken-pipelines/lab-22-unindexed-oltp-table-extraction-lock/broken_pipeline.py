"""
Broken implementation demonstrating the flaw in lab-22-unindexed-oltp-table-extraction-lock.
"""
def extract_query_broken():
    return "SELECT * FROM orders WHERE updated_at > '2026-09-01';"
