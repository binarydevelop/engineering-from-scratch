#!/usr/bin/env python3

class ClusterMetadataCoordinator:
    def __init__(self):
        self.version = 1
        self.nodes = ["node-1", "node-2", "node-3"]
        self.indices = {}

    def update_mapping(self, index_name, new_field, field_type):
        self.version += 1
        self.indices.setdefault(index_name, {})[new_field] = field_type
        # Broadcast diff to all nodes
        diff = f"v{self.version}: Added {new_field}:{field_type} to {index_name}"
        return diff

if __name__ == "__main__":
    master = ClusterMetadataCoordinator()
    print("Master Node initialized. Cluster State Version:", master.version)
    diff1 = master.update_mapping("users", "email", "keyword")
    print("Broadcast:", diff1)
    diff2 = master.update_mapping("users", "age", "integer")
    print("Broadcast:", diff2)
    print("Current State Version:", master.version)
