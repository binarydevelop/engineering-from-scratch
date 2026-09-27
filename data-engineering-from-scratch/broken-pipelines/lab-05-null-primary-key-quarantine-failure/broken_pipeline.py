"""
Broken implementation demonstrating the flaw in lab-05-null-primary-key-quarantine-failure.
"""
def validate_record(rec):
    return len(rec) > 0 # Allows null or empty ID
