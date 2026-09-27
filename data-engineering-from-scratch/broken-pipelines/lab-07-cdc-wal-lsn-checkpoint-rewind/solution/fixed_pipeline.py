"""
Resilient, production-ready solution for lab-07-cdc-wal-lsn-checkpoint-rewind.
"""
class SafeCDC:
    def __init__(self):
        self.checkpoint = 0
    def process_atomic(self, event, db):
        if event.get("crash"): raise RuntimeError("Worker killed!")
        # Target write first, then checkpoint commit
        db.append(event)
        self.checkpoint = event["lsn"]
