class LakehouseTable:
    def __init__(self):
        self.snapshots = {}
        self.current_snapshot_id = 0
    def commit(self, files, schema):
        self.current_snapshot_id += 1
        self.snapshots[self.current_snapshot_id] = {
            "files": list(files),
            "schema": dict(schema)
        }
        return self.current_snapshot_id
    def time_travel(self, snapshot_id):
        return self.snapshots[snapshot_id]
