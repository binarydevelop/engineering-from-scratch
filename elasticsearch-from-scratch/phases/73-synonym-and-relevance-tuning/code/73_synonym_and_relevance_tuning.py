#!/usr/bin/env python3

def score_product(query_tokens, doc, boosts):
    score = 0.0
    for t in query_tokens:
        if t in doc.get("title", "").lower():
            score += 1.0 * boosts.get("title", 1.0)
        if t in doc.get("brand", "").lower():
            score += 1.0 * boosts.get("brand", 1.0)
        if t in doc.get("category", "").lower():
            score += 1.0 * boosts.get("category", 1.0)
    return score

if __name__ == "__main__":
    doc = {"title": "MacBook Pro M3", "brand": "Apple", "category": "laptop"}
    query = ["apple", "laptop"]

    default_score = score_product(query, doc, boosts={"title": 1.0, "brand": 1.0, "category": 1.0})
    tuned_score = score_product(query, doc, boosts={"title": 3.0, "brand": 2.0, "category": 1.5})

    print("Document:", doc)
    print("Query:", query)
    print(f"Default Score (1x): {default_score}")
    print(f"Tuned Score (Boosted): {tuned_score}")
