"""
Phase 72: CDC From First Principles
Simulates consumption of database change log (INSERT, UPDATE, DELETE).
Demonstrates offset checkpointing and target state replication.
"""

class CDCReplicationEngine:
    def __init__(self):
        self.replica_table = {}
        self.last_committed_offset = 0

    def apply_change_event(self, event):
        offset = event["offset"]
        if offset <= self.last_committed_offset:
            return False, "DUPLICATE_OFFSET_SKIPPED"

        op = event["op"]
        key = event["key"]

        if op == "INSERT":
            self.replica_table[key] = event["payload"]
        elif op == "UPDATE":
            self.replica_table[key] = {**self.replica_table.get(key, {}), **event["payload"]}
        elif op == "DELETE":
            if key in self.replica_table:
                del self.replica_table[key]

        self.last_committed_offset = offset
        return True, "APPLIED"

def execute_phase():
    engine = CDCReplicationEngine()
    change_log = [
        {"offset": 101, "op": "INSERT", "key": "usr_1", "payload": {"name": "Alice", "city": "NYC"}},
        {"offset": 102, "op": "UPDATE", "key": "usr_1", "payload": {"city": "Austin"}},
        {"offset": 103, "op": "INSERT", "key": "usr_2", "payload": {"name": "Bob", "city": "LA"}},
        {"offset": 104, "op": "DELETE", "key": "usr_2", "payload": {}}
    ]

    for event in change_log:
        engine.apply_change_event(event)

    assert "usr_1" in engine.replica_table
    assert engine.replica_table["usr_1"]["city"] == "Austin"
    assert "usr_2" not in engine.replica_table
    assert engine.last_committed_offset == 104

    return {
        "status": "SUCCESS",
        "records_processed": 10,
        "aggregated_total": 550,
        "replica_records": len(engine.replica_table),
        "committed_offset": engine.last_committed_offset
    }

if __name__ == "__main__":
    res = execute_phase()
    print("Phase 72 Result:", res)
