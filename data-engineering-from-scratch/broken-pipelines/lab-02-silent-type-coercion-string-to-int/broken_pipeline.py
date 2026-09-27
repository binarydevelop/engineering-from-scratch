"""
Broken implementation demonstrating the flaw in lab-02-silent-type-coercion-string-to-int.
"""
# Broken: Assumes IDs are always integers
def parse_customer_id(val):
    return int(val) # Crashes on '1004B'
