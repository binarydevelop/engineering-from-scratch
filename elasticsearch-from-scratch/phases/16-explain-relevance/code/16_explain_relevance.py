#!/usr/bin/env python3

def explain_bm25(term, tf, doc_len, avgdl, n_docs, doc_freq, k1=1.2, b=0.75):
    import math
    idf = math.log(1.0 + (n_docs - doc_freq + 0.5) / (doc_freq + 0.5))
    len_norm = 1.0 - b + b * (doc_len / avgdl)
    tf_norm = (tf * (k1 + 1)) / (tf + k1 * len_norm)
    total_score = idf * tf_norm

    explanation = {
        "term": term,
        "score": round(total_score, 4),
        "description": f"score({term}) = idf({idf:.4f}) * tfNorm({tf_norm:.4f})",
        "details": [
            {"description": f"idf(doc_freq={doc_freq}, n_docs={n_docs})", "value": round(idf, 4)},
            {"description": f"tfNorm(tf={tf}, doc_len={doc_len}, avgdl={avgdl:.1f})", "value": round(tf_norm, 4)}
        ]
    }
    return explanation

if __name__ == "__main__":
    tree = explain_bm25("keyboard", tf=2, doc_len=6, avgdl=8.5, n_docs=1000, doc_freq=50)
    print(f"Term: {tree['term']} | Total Score: {tree['score']}")
    print(f"Formula: {tree['description']}")
    for d in tree["details"]:
        print(f"  - {d['description']}: {d['value']}")
