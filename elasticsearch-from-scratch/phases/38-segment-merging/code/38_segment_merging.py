#!/usr/bin/env python3

class MergeSimulator:
    def __init__(self):
        # list of dicts: {"id": str, "docs": {doc_id: text}, "deleted": set()}
        self.segments = []

    def add_segment(self, seg_id, docs, deleted=None):
        self.segments.append({
            "id": seg_id,
            "docs": docs,
            "deleted": deleted or set()
        })

    def merge_segments(self, seg_indices):
        merged_docs = {}
        for idx in seg_indices:
            seg = self.segments[idx]
            for doc_id, text in seg["docs"].items():
                if doc_id not in seg["deleted"]:
                    merged_docs[doc_id] = text
        # Remove old segments and append merged
        self.segments = [s for i, s in enumerate(self.segments) if i not in seg_indices]
        new_id = f"merged_{len(self.segments)}"
        self.segments.append({"id": new_id, "docs": merged_docs, "deleted": set()})

if __name__ == "__main__":
    sim = MergeSimulator()
    sim.add_segment("seg_0", {1: "doc 1", 2: "doc 2"}, deleted={1})
    sim.add_segment("seg_1", {3: "doc 3", 4: "doc 4"}, deleted={4})

    print("Before Merge:")
    for s in sim.segments:
        print(f"  {s['id']}: docs={list(s['docs'].keys())}, deleted={s['deleted']}")

    print("\nExecuting Segment Merge...")
    sim.merge_segments([0, 1])

    print("After Merge:")
    for s in sim.segments:
        print(f"  {s['id']}: docs={list(s['docs'].keys())}, deleted={s['deleted']}")
    print("Deleted docs 1 and 4 have been physically purged!")
