#!/usr/bin/env python3

def recommend_technology(requirements):
    recs = []
    if requirements.get("strict_acid"):
        recs.append("PostgreSQL (Strict ACID relational transactions)")
    if requirements.get("sub_ms_cache"):
        recs.append("Redis (Sub-millisecond in-memory caching)")
    if requirements.get("event_stream"):
        recs.append("Apache Kafka (High-throughput durable event log)")
    if requirements.get("full_text_facets"):
        recs.append("Elasticsearch (Distributed BM25 search & analytics)")
    return recs

if __name__ == "__main__":
    app_needs = {
        "strict_acid": True,
        "sub_ms_cache": True,
        "event_stream": True,
        "full_text_facets": True
    }
    print("Multi-Engine System Design Recommendation:")
    technologies = recommend_technology(app_needs)
    for t in technologies:
        print("  -", t)
    print("\nEach tool serves its specialized strength; none replaces the others!")
