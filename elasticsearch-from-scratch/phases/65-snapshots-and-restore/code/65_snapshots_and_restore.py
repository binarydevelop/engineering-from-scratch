#!/usr/bin/env python3

class SnapshotRepoSim:
    def __init__(self):
        self.repo_segments = set()
        self.snapshots = {}

    def take_snapshot(self, snapshot_name, active_segments):
        # Only copy new segments (incremental)
        new_segments = [s for s in active_segments if s not in self.repo_segments]
        self.repo_segments.update(new_segments)
        self.snapshots[snapshot_name] = list(active_segments)
        return len(new_segments)

if __name__ == "__main__":
    repo = SnapshotRepoSim()
    print("Time 1: Index has segments [_0, _1]")
    copied = repo.take_snapshot("snap_1", ["seg_0", "seg_1"])
    print(f"  Snapshot 1 copied: {copied} segments.")

    print("\nTime 2: Segment _2 created. Segments are now [_0, _1, _2]")
    copied = repo.take_snapshot("snap_2", ["seg_0", "seg_1", "seg_2"])
    print(f"  Snapshot 2 copied: {copied} segment (Incremental!)")
