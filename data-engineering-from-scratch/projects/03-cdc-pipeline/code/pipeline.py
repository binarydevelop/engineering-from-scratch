class CDCReplicator:
    def __init__(self):
        self.state = {}
        self.last_lsn = 0
    def apply_event(self, event):
        lsn = event["lsn"]
        if lsn <= self.last_lsn: return False
        op = event["op"]
        key = event["key"]
        if op in ["INSERT", "UPDATE"]:
            self.state[key] = event["payload"]
        elif op == "DELETE" and key in self.state:
            del self.state[key]
        self.last_lsn = lsn
        return True
