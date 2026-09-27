#!/usr/bin/env python3

def naive_term_count(doc, term):
    return doc.lower().split().count(term)

def length_normalized_score(doc, term):
    words = doc.lower().split()
    tf = words.count(term)
    doc_len = len(words)
    return tf / doc_len if doc_len > 0 else 0.0

if __name__ == "__main__":
    corpus = {
        "Doc A (Short Title)": "Database systems and database design",
        "Doc B (Long Article)": "This article discusses computer hardware, networking protocols, operating systems, and a database briefly mentioned at the end of the chapter.",
        "Doc C (Keyword Stuffed)": "database database database database database"
    }

    print("Ranking for query 'database':\n")
    print(f"{'Document':25s} | {'Raw Count':10s} | {'Length Norm Score':15s}")
    print("-" * 60)
    for title, text in corpus.items():
        raw = naive_term_count(text, "database")
        norm = length_normalized_score(text, "database")
        print(f"{title:25s} | {raw:10d} | {norm:15.4f}")
