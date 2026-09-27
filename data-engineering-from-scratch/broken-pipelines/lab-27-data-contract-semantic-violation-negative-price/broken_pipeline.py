"""
Broken implementation demonstrating the flaw in lab-27-data-contract-semantic-violation-negative-price.
"""
def validate_price(price):
    return isinstance(price, (int, float)) # Passes -50.00
