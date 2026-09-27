"""
Resilient, production-ready solution for lab-05-null-primary-key-quarantine-failure.
"""
def validate_record(rec):
    pk = rec.get("id")
    if pk is None or str(pk).strip() == "":
        return False, "NULL_OR_EMPTY_PK"
    return True, "VALID"
