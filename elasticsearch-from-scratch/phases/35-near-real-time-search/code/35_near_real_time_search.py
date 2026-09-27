#!/usr/bin/env python3
import time

class NRTSimulator:
    def __init__(self, refresh_interval=1.0):
        self.buffer = {}
        self.searchable_segments = {}
        self.refresh_interval = refresh_interval
        self.last_refresh = time.time()

    def index(self, doc_id, text):
        # Acknowledged immediately
        self.buffer[doc_id] = text
        return {"status": 201, "acknowledged": True}

    def search(self, term):
        # Only searches refreshed segments
        hits = []
        for d_id, text in self.searchable_segments.items():
            if term in text:
                hits.append(d_id)
        return hits

    def refresh(self):
        # Flushes buffer into searchable segment
        self.searchable_segments.update(self.buffer)
        self.buffer.clear()
        self.last_refresh = time.time()

if __name__ == "__main__":
    nrt = NRTSimulator(refresh_interval=1.0)
    print("1. Indexing Doc 101...")
    nrt.index(101, "wireless mouse")
    print("2. Immediate search for 'wireless' -> Hits:", nrt.search("wireless"))
    print("   (Document is in memory buffer, not yet in a segment!)")
    print("3. Executing Refresh...")
    nrt.refresh()
    print("4. Search after refresh -> Hits:", nrt.search("wireless"))
