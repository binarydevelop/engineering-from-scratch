#!/usr/bin/env python3

def trade_off_analysis(workload_type):
    if workload_type == "bank_transactions":
        return "PostgreSQL", "Requires strict multi-row ACID transactions and balance rollbacks."
    elif workload_type == "e_commerce_catalog":
        return "Elasticsearch", "Requires fuzzy search, facets, BM25 ranking, and sub-15ms response."
    elif workload_type == "user_profile_crud":
        return "PostgreSQL", "Primary key lookup, foreign key relational integrity."
    elif workload_type == "server_log_analytics":
        return "Elasticsearch", "High-throughput append-only time-series with date histogram aggs."
    return "Unknown", "Evaluate access patterns."

if __name__ == "__main__":
    workloads = ["bank_transactions", "e_commerce_catalog", "user_profile_crud", "server_log_analytics"]
    print("Workload Architectural Decision Engine:")
    for w in workloads:
        winner, reason = trade_off_analysis(w)
        print(f"  [{w:22s}] ──► Choose: {winner:14s} ({reason})")
