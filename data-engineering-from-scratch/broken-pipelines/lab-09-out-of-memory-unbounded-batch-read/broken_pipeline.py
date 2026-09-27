"""
Broken implementation demonstrating the flaw in lab-09-out-of-memory-unbounded-batch-read.
"""
# Broken: Reads entire file at once
def read_all(lines):
    return [l for l in lines] # OOM on huge files
