"""
Broken implementation demonstrating the flaw in lab-19-poison-record-crashing-entire-batch.
"""
import json
def process_batch_broken(lines):
    return [json.loads(l) for l in lines] # 1 corrupted byte crashes entire batch
