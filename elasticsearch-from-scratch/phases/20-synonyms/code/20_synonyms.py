#!/usr/bin/env python3

class SynonymExpander:
    def __init__(self, rules):
        self.synonyms = {}
        for rule in rules:
            words = [w.strip().lower() for w in rule.split(",")]
            for w in words:
                self.synonyms[w] = words

    def expand_query(self, query):
        tokens = query.lower().split()
        expanded = []
        for t in tokens:
            if t in self.synonyms:
                expanded.append(f"({' OR '.join(self.synonyms[t])})")
            else:
                expanded.append(t)
        return " AND ".join(expanded)

if __name__ == "__main__":
    rules = [
        "laptop, notebook, portable computer",
        "wireless, cordless",
        "screen, monitor, display"
    ]
    exp = SynonymExpander(rules)
    user_query = "wireless laptop screen"
    print("User Query:     ", user_query)
    print("Expanded Query: ", exp.expand_query(user_query))
