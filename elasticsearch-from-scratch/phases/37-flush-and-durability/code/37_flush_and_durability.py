#!/usr/bin/env python3

class TranslogAndFlushSim:
    def __init__(self):
        self.translog = []
        self.persisted_segments = []
        self.memory_buffer = []

    def write(self, doc_id, text):
        # 1. Write to memory buffer
        self.memory_buffer.append((doc_id, text))
        # 2. Append to translog on disk
        self.translog.append(f"INDEX doc_id={doc_id}")

    def refresh(self):
        print(f"  [Refresh] Made {len(self.memory_buffer)} docs searchable in OS cache.")
        self.memory_buffer.clear()

    def flush(self):
        print(f"  [Flush] Calling fsync(). Syncing segments to disk.")
        self.persisted_segments.append(f"Segment_committed_{len(self.persisted_segments)}")
        print(f"  [Flush] Truncating translog ({len(self.translog)} ops cleared).")
        self.translog.clear()

if __name__ == "__main__":
    engine = TranslogAndFlushSim()
    print("1. Indexing 3 documents...")
    engine.write(1, "doc one")
    engine.write(2, "doc two")
    engine.write(3, "doc three")
    print(f"Translog contains: {engine.translog}")

    print("\n2. Running Refresh:")
    engine.refresh()
    print(f"Translog still contains {len(engine.translog)} ops (still needed for crash recovery!)")

    print("\n3. Running Flush:")
    engine.flush()
    print(f"Translog after flush: {engine.translog} (Completely clean)")
