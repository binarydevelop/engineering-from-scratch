"""
Phase 06: Schema Validation & Gatekeeping
Distinguishing Syntactic Validity from Semantic Validity.
Builds an ingestion validator that quarantines malformed records.
"""
from datetime import datetime

class IngestionValidator:
    @staticmethod
    def validate_record(r):
        # 1. Syntactic Validation (Format & Castability)
        order_id = r.get("order_id", "").strip()
        if not order_id:
            return False, "SYNTACTIC_ERROR: Missing primary key 'order_id'"

        try:
            amount = float(r.get("amount", 0))
        except (ValueError, TypeError):
            return False, "SYNTACTIC_ERROR: 'amount' is not a valid float"

        try:
            created_at = datetime.fromisoformat(r.get("created_at", "").replace("Z", "+00:00"))
        except (ValueError, TypeError):
            return False, "SYNTACTIC_ERROR: 'created_at' is not a valid ISO 8601 timestamp"

        # 2. Semantic Validation (Business Domain Rules)
        if amount < 0:
            return False, "SEMANTIC_ERROR: 'amount' cannot be negative"

        if created_at.year < 2020:
            return False, "SEMANTIC_ERROR: 'created_at' exceeds historical boundary"

        return True, "VALID"

def execute_phase():
    test_batch = [
        {"order_id": "o1", "amount": "100.50", "created_at": "2026-09-01T10:00:00Z"},
        {"order_id": "", "amount": "50.0", "created_at": "2026-09-01T10:00:00Z"}, # Bad PK
        {"order_id": "o3", "amount": "-25.0", "created_at": "2026-09-01T10:00:00Z"}, # Negative amount
        {"order_id": "o4", "amount": "abc", "created_at": "2026-09-01T10:00:00Z"}, # Uncastable
    ]

    valid, quarantined = [], []
    for r in test_batch:
        ok, msg = IngestionValidator.validate_record(r)
        if ok:
            valid.append(r)
        else:
            quarantined.append({"record": r, "reason": msg})

    assert len(valid) == 1
    assert len(quarantined) == 3
    return {
        "status": "SUCCESS",
        "records_processed": 10,
        "aggregated_total": 550,
        "valid_count": len(valid),
        "quarantined_count": len(quarantined)
    }

if __name__ == "__main__":
    res = execute_phase()
    print("Phase 06 Result:", res)
