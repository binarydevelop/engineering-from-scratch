#!/usr/bin/env python3

class SearchAsYouTypeSim:
    def __init__(self, catalog):
        self.catalog = catalog

    def query(self, prefix_input):
        terms = prefix_input.lower().split()
        if not terms:
            return []
        complete_terms = terms[:-1]
        last_prefix = terms[-1]

        hits = []
        for item in self.catalog:
            title_lower = item["title"].lower()
            # Must match all complete terms
            if complete_terms and not all(ct in title_lower for ct in complete_terms):
                continue
            # Must match prefix on last term
            words = title_lower.split()
            if any(w.startswith(last_prefix) for w in words):
                # Score = popularity + bonus for exact word match
                score = item["popularity"]
                if any(w == last_prefix for w in words):
                    score += 50
                hits.append((item["title"], score))

        hits.sort(key=lambda x: x[1], reverse=True)
        return hits

if __name__ == "__main__":
    products = [
        {"title": "Wireless Mechanical Keyboard", "popularity": 1200},
        {"title": "Wireless Mouse", "popularity": 2500},
        {"title": "Wired Gaming Keyboard", "popularity": 800},
        {"title": "Wireless Ergonomic Trackball", "popularity": 300}
    ]
    engine = SearchAsYouTypeSim(products)
    print("User types 'wirel':")
    for title, s in engine.query("wirel"):
        print(f"  - {title} (score: {s})")
    print("\nUser types 'wirel mech':")
    for title, s in engine.query("wirel mech"):
        print(f"  - {title} (score: {s})")
