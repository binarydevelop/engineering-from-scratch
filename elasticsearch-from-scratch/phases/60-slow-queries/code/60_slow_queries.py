#!/usr/bin/env python3

def analyze_query_risk(query_json):
    risks = []
    q_str = str(query_json)
    if ".*" in q_str or "*?" in q_str:
        risks.append("CRITICAL: Leading wildcard or broad regex detected (Dictionary scan).")
    if query_json.get("from", 0) > 5000:
        risks.append("WARNING: Deep pagination detected (Coordinator sorting penalty).")
    if "script" in q_str:
        risks.append("WARNING: Scripting query detected (Bypasses Lucene inverted index).")
    return risks

if __name__ == "__main__":
    sample_query = {
        "from": 8000,
        "size": 10,
        "query": {"wildcard": {"title": "*phone*"}}
    }
    print("Analyzing Query for Performance Risks:")
    detected = analyze_query_risk(sample_query)
    for d in detected:
        print("  -", d)
