"""
Broken implementation demonstrating the flaw in lab-07-cdc-wal-lsn-checkpoint-rewind.
"""
class NaiveCDC:
    def __init__(self):
        self.checkpoint = 0
    def process_and_commit_first(self, event, db):
        self.checkpoint = event["lsn"] # Commits checkpoint BEFORE target write!
        if event.get("crash"): raise RuntimeError("Worker killed!")
        db.append(event)
