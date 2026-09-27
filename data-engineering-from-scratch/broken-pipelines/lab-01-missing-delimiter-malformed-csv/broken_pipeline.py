"""
Broken implementation demonstrating the flaw in lab-01-missing-delimiter-malformed-csv.
"""
# Broken: Naive split on comma
def ingest_records(raw_text):
    rows = []
    for line in raw_text.strip().split("\n"):
        parts = line.split(",") # Fails on unquoted commas
        rows.append({"id": parts[0], "name": parts[1], "city": parts[2]})
    return rows
