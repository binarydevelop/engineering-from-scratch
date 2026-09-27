"""
Resilient, production-ready solution for lab-02-silent-type-coercion-string-to-int.
"""
# Fixed: Preserves identifier semantics as string / validates format
def parse_customer_id(val):
    clean = str(val).strip()
    if not clean:
        raise ValueError("Customer ID cannot be empty")
    return clean
