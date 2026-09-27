"""
Resilient, production-ready solution for lab-27-data-contract-semantic-violation-negative-price.
"""
def validate_price(price):
    return isinstance(price, (int, float)) and price >= 0.0
