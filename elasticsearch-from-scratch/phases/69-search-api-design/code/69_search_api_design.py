#!/usr/bin/env python3

def build_safe_search_dsl(user_q, category=None, max_price=None, page=1, page_size=20, tenant_id="acme"):
    # 1. Enforce pagination limits
    page_size = min(max(1, page_size), 50)
    page = max(1, min(page, 20))
    from_offset = (page - 1) * page_size

    # 2. Build bool query
    must_clauses = []
    if user_q:
        must_clauses.append({
            "multi_match": {
                "query": user_q.strip()[:100], # truncate long strings
                "fields": ["title^2", "description"]
            }
        })
    else:
        must_clauses.append({"match_all": {}})

    # 3. Mandatory filter context
    filter_clauses = [{"term": {"tenant_id": tenant_id}}]
    if category:
        filter_clauses.append({"term": {"category.keyword": category}})
    if max_price is not None:
        filter_clauses.append({"range": {"price": {"lte": float(max_price)}}})

    dsl = {
        "from": from_offset,
        "size": page_size,
        "query": {
            "bool": {
                "must": must_clauses,
                "filter": filter_clauses
            }
        }
    }
    return dsl

if __name__ == "__main__":
    query = build_safe_search_dsl("mechanical keyboard", category="electronics", max_price=150.0, page=2, page_size=10, tenant_id="tenant_88")
    import json
    print("Safely Generated Elasticsearch DSL:")
    print(json.dumps(query, indent=2))
