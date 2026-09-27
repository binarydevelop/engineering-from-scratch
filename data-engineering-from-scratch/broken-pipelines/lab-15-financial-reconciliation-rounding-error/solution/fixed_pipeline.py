"""
Resilient, production-ready solution for lab-15-financial-reconciliation-rounding-error.
"""
from decimal import Decimal
def sum_revenue_decimal(amounts):
    return sum([Decimal(str(a)) for a in amounts])
