"""
Broken implementation demonstrating the flaw in lab-18-scd2-overlapping-effective-dates.
"""
def update_scd2_broken(records, new_record):
    records.append(new_record) # Appends without setting valid_to on previous!
