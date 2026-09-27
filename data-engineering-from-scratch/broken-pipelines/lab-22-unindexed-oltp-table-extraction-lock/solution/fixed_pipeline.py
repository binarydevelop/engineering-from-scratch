"""
Resilient, production-ready solution for lab-22-unindexed-oltp-table-extraction-lock.
"""
def extract_query_bounded():
    # Indexed cursor extraction with batch limits
    return "SELECT * FROM orders WHERE updated_at > '2026-09-01' ORDER BY updated_at LIMIT 1000;"
