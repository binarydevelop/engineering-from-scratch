#!/usr/bin/env python3
"""
projects/log_search/analyzer.py - Queries, aggregates, and diagnoses log telemetry.
"""

import json
import os
import sys
import urllib.request

ES_HOST = os.environ.get("ES_URL", "http://localhost:9200")
INDEX_NAME = "microservice_logs"

def query_error_report():
    dsl = {
        "size": 0,
        "query": {
            "bool": {
                "filter": [
                    {"term": {"level": "ERROR"}}
                ]
            }
        },
        "aggs": {
            "by_service": {
                "terms": {"field": "service", "size": 10},
                "aggs": {
                    "top_errors": {
                        "terms": {"field": "message.keyword", "size": 3}
                    },
                    "p95_latency": {
                        "percentiles": {"field": "duration_ms", "percents": [95]}
                    }
                }
            }
        }
    }

    req = urllib.request.Request(f"{ES_HOST}/{INDEX_NAME}/_search", data=json.dumps(dsl).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())

    buckets = res.get("aggregations", {}).get("by_service", {}).get("buckets", [])
    print("=== Microservice Incident & Error Telemetry Report ===")
    for b in buckets:
        svc = b["key"]
        count = b["doc_count"]
        p95 = b.get("p95_latency", {}).get("values", {}).get("95.0", 0)
        print(f"\n[Service: {svc.upper()}] - Total Errors: {count} | p95 Latency: {p95:.1f} ms")
        print("  Top Recurring Root Causes:")
        for err_bucket in b.get("top_errors", {}).get("buckets", []):
            print(f"    * ({err_bucket['doc_count']:2d}x): {err_bucket['key']}")

if __name__ == "__main__":
    query_error_report()
