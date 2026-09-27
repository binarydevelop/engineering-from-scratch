#!/usr/bin/env python3

class PITSimulator:
    def __init__(self, current_data):
        # Freezes references to segments at this instant
        self.frozen_data = list(current_data)

    def search(self, query):
        return [d for d in self.frozen_data if query in d["text"]]

if __name__ == "__main__":
    live_database = [{"id": 1, "text": "initial item 1"}, {"id": 2, "text": "initial item 2"}]
    print("Opening Point In Time (PIT)...")
    pit = PITSimulator(live_database)

    print("Concurrent Write: Appending item 3 to live database...")
    live_database.append({"id": 3, "text": "newly added item 3"})

    print(f"Live database now has: {len(live_database)} items.")
    print(f"PIT frozen search sees: {len(pit.search('item'))} items! (Completely isolated from concurrent writes)")
