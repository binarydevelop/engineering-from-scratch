#!/usr/bin/env python3
"""
Tiny Key-Value Store with Append-Only Log (WAL) & Crash Recovery
Implements the simplest persistent storage model:
- Writes append sequentially to an on-disk Write-Ahead Log
- In-memory hash index maps key to byte offset for O(1) lookups
- Crash recovery replays WAL from disk to rebuild in-memory state
- Background log compaction reclaims disk space
"""

import os
import json
from typing import Optional, Dict

class TinyKV:
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.index: Dict[str, int] = {}  # key -> byte offset in file
        self._init_storage()

    def _init_storage(self):
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w") as f:
                pass
        self._recover()

    def _recover(self):
        """Replay log file from beginning to reconstruct index in memory"""
        self.index.clear()
        if not os.path.exists(self.log_path):
            return
        with open(self.log_path, "r") as f:
            while True:
                offset = f.tell()
                line = f.readline()
                if not line:
                    break
                try:
                    record = json.loads(line)
                    k = record["key"]
                    op = record.get("op", "PUT")
                    if op == "DELETE":
                        self.index.pop(k, None)
                    else:
                        self.index[k] = offset
                except json.JSONDecodeError:
                    continue

    def put(self, key: str, value: any):
        with open(self.log_path, "a") as f:
            offset = f.tell()
            record = {"op": "PUT", "key": key, "val": value}
            f.write(json.dumps(record) + "\n")
            f.flush()
            self.index[key] = offset

    def get(self, key: str) -> Optional[any]:
        if key not in self.index:
            return None
        offset = self.index[key]
        with open(self.log_path, "r") as f:
            f.seek(offset)
            line = f.readline()
            if line:
                record = json.loads(line)
                return record["val"]
        return None

    def delete(self, key: str):
        if key in self.index:
            with open(self.log_path, "a") as f:
                record = {"op": "DELETE", "key": key}
                f.write(json.dumps(record) + "\n")
                f.flush()
            del self.index[key]

    def compact(self):
        """Rewrite log file containing only the latest live keys"""
        compact_path = self.log_path + ".compact"
        with open(compact_path, "w") as f_out:
            for k in list(self.index.keys()):
                val = self.get(k)
                if val is not None:
                    offset = f_out.tell()
                    record = {"op": "PUT", "key": k, "val": val}
                    f_out.write(json.dumps(record) + "\n")
        os.replace(compact_path, self.log_path)
        self._recover()

def run_simulation():
    log_file = "/tmp/tiny_kv_demo.log"
    if os.path.exists(log_file):
        os.remove(log_file)

    print("======================================================================")
    print(" TINY KEY-VALUE STORE: WAL + IN-MEMORY HASH INDEX")
    print("======================================================================")

    store = TinyKV(log_file)
    print("Writing keys...")
    store.put("sess_abc", {"user_id": 42, "role": "admin"})
    store.put("sess_def", {"user_id": 99, "role": "viewer"})
    store.put("sess_abc", {"user_id": 42, "role": "superadmin"})  # Mutation update

    print("Get sess_abc:", store.get("sess_abc"))
    print("Get sess_def:", store.get("sess_def"))

    print("\nSimulating Server Crash and Cold Restart...")
    # Re-instantiate TinyKV pointing to same disk file
    recovered_store = TinyKV(log_file)
    print("State successfully recovered from disk WAL:")
    print("Get sess_abc after crash:", recovered_store.get("sess_abc"))

    print("\nExecuting Log Compaction...")
    pre_size = os.path.getsize(log_file)
    recovered_store.compact()
    post_size = os.path.getsize(log_file)
    print(f"WAL Size: {pre_size} bytes ──> Compacted: {post_size} bytes")
    print("Compacted read:", recovered_store.get("sess_abc"))

if __name__ == "__main__":
    run_simulation()
