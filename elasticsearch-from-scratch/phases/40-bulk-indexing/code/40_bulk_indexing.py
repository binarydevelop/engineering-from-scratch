#!/usr/bin/env python3
import time

def generate_ndjson_bulk(docs):
    lines = []
    for d in docs:
        lines.append(f'{{"index": {{"_index": "test", "_id": "{d["id"]}"}}}}')
        lines.append(f'{{"title": "{d["title"]}", "price": {d["price"]}}}')
    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    sample_docs = [{"id": i, "title": f"Item {i}", "price": i * 1.5} for i in range(5)]
    ndjson = generate_ndjson_bulk(sample_docs)
    print("Sample NDJSON Bulk Payload Format:")
    print(ndjson)
    print(f"Total payload bytes: {len(ndjson.encode())} bytes for {len(sample_docs)} docs")
