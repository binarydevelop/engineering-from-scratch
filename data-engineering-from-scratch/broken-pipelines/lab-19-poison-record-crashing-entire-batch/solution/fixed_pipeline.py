"""
Resilient, production-ready solution for lab-19-poison-record-crashing-entire-batch.
"""
import json
def process_batch_quarantine(lines):
    valid, quarantine = [], []
    for idx, l in enumerate(lines):
        try:
            valid.append(json.loads(l))
        except Exception as e:
            quarantine.append({"line_idx": idx, "raw": l, "error": str(e)})
    return valid, quarantine
