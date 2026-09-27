#!/usr/bin/env python3

def parse_profile_sample(sample_profile):
    queries = sample_profile.get("shards", [])[0].get("searches", [])[0].get("query", [])
    report = []
    for q in queries:
        report.append({
            "type": q.get("type"),
            "description": q.get("description"),
            "time_ms": round(q.get("time_in_nanos", 0) / 1_000_000, 3)
        })
    return report

if __name__ == "__main__":
    mock_profile = {
        "shards": [{
            "searches": [{
                "query": [
                    {"type": "TermQuery", "description": "title:keyboard", "time_in_nanos": 4200000},
                    {"type": "PointRangeQuery", "description": "price:[50 TO 150]", "time_in_nanos": 800000}
                ]
            }]
        }]
    }
    parsed = parse_profile_sample(mock_profile)
    print("Parsed Lucene Query Profile:")
    for p in parsed:
        print(f"  {p['type']:20s} | {p['description']:25s} | Time: {p['time_ms']} ms")
