"""
Resilient, production-ready solution for lab-01-missing-delimiter-malformed-csv.
"""
# Fixed: RFC 4180 compliant CSV parser with quarantine for malformed column counts
import csv
import io

def ingest_records(raw_text):
    valid, quarantined = [], []
    reader = csv.reader(io.StringIO(raw_text.strip()))
    for row_idx, parts in enumerate(reader, 1):
        if len(parts) == 3:
            valid.append({"id": parts[0], "name": parts[1], "city": parts[2]})
        else:
            quarantined.append({"row_idx": row_idx, "raw": parts, "reason": "COLUMN_COUNT_MISMATCH"})
    return valid, quarantined
