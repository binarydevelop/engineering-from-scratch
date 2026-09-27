#!/usr/bin/env python3

def simulate_reindex(v1_docs, transform_fn):
    v2_docs = {}
    for doc_id, doc in v1_docs.items():
        v2_docs[doc_id] = transform_fn(dict(doc))
    return v2_docs

if __name__ == "__main__":
    v1_store = {
        1: {"title": "Keyboard", "price": "149.99"}, # stored as string
        2: {"title": "Mouse", "price": "49.99"}
    }
    print("V1 Data (price is string):", v1_store)
    def cast_price_to_float(d):
        d["price"] = float(d["price"])
        return d
    v2_store = simulate_reindex(v1_store, cast_price_to_float)
    print("V2 Data (price cast to float):", v2_store)
    print("Reindex successfully updated schema data types!")
