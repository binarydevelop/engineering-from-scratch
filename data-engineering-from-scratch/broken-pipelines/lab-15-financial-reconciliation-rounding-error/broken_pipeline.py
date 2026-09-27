"""
Broken implementation demonstrating the flaw in lab-15-financial-reconciliation-rounding-error.
"""
def sum_revenue_float(amounts):
    return sum(amounts) # Float addition yields 0.30000000000000004
