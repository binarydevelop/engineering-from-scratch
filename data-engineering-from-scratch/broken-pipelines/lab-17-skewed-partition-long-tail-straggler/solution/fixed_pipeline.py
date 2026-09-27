"""
Resilient, production-ready solution for lab-17-skewed-partition-long-tail-straggler.
"""
import random
def salted_key(country, salt_factor=5):
    # Salting spreads hot key across multiple sub-partitions
    if country == "US":
        return f"US_{random.randint(0, salt_factor - 1)}"
    return country
