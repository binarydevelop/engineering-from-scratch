"""
Benchmark: JSON Serialization & Parsing Throughput.
Measures parsing and serialization throughput for standard API DTO payloads.
"""

import time
import json
from typing import Dict, Any

def benchmark() -> Dict[str, Any]:
    payload = {
        "id": "ord_99812",
        "customer": {"id": "usr_42", "name": "Alice Developer", "tier": "ENTERPRISE"},
        "items": [
            {"sku": f"SKU-{i}", "qty": i, "price": 19.99} for i in range(1, 20)
        ],
        "metadata": {"source": "mobile_app", "ip": "192.168.1.1", "flags": ["gift", "express"]}
    }

    iterations = 2000

    # Serialization
    start_ser = time.perf_counter()
    serialized_bytes = ""
    for _ in range(iterations):
        serialized_bytes = json.dumps(payload)
    ser_time = time.perf_counter() - start_ser

    # Deserialization
    start_de = time.perf_counter()
    for _ in range(iterations):
        _ = json.loads(serialized_bytes)
    de_time = time.perf_counter() - start_de

    total_ops = iterations * 2
    total_time = ser_time + de_time
    throughput_ops = total_ops / total_time if total_time > 0 else 0

    return {
        "name": "JSON Serialization / Deserialization Throughput",
        "iterations": iterations,
        "serialize_sec": round(ser_time, 4),
        "deserialize_sec": round(de_time, 4),
        "throughput_ops_per_sec": int(throughput_ops),
        "payload_bytes": len(serialized_bytes)
    }

if __name__ == "__main__":
    res = benchmark()
    print(f"[{res['name']}]")
    print(f"  Serialize:   {res['serialize_sec']}s")
    print(f"  Deserialize: {res['deserialize_sec']}s")
    print(f"  Throughput:  {res['throughput_ops_per_sec']} ops/sec")
