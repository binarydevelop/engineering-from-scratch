#!/usr/bin/env python3

class ImmutableSegment:
    def __init__(self, segment_id, doc_dict):
        self.segment_id = segment_id
        # Inverted index within this segment
        self.index = {}
        self.docs = doc_dict
        self.deleted = set()
        for doc_id, text in doc_dict.items():
            for w in text.lower().split():
                self.index.setdefault(w, []).append(doc_id)

    def search(self, term):
        hits = self.index.get(term.lower(), [])
        return [h for h in hits if h not in self.deleted]

    def delete(self, doc_id):
        if doc_id in self.docs:
            self.deleted.add(doc_id)

class ShardWithSegments:
    def __init__(self):
        self.segments = []

    def add_segment(self, doc_dict):
        seg_id = f"_{len(self.segments)}"
        self.segments.append(ImmutableSegment(seg_id, doc_dict))

    def search_all(self, term):
        all_hits = []
        for s in self.segments:
            all_hits.extend(s.search(term))
        return all_hits

if __name__ == "__main__":
    shard = ShardWithSegments()
    shard.add_segment({1: "elasticsearch distributed search", 2: "redis in-memory cache"})
    shard.add_segment({3: "elasticsearch immutable segments", 4: "kafka event log"})

    print("Search 'elasticsearch' across all segments -> Doc IDs:", shard.search_all("elasticsearch"))
    print("Deleting Doc 1 (marking in deletion bitset)...")
    shard.segments[0].delete(1)
    print("Search 'elasticsearch' after delete -> Doc IDs:", shard.search_all("elasticsearch"))
