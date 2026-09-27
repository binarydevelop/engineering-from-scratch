#!/usr/bin/env python3

def infer_type(val):
    if isinstance(val, bool):
        return "boolean"
    if isinstance(val, int):
        return "long"
    if isinstance(val, float):
        return "double"
    if isinstance(val, str):
        if val.isdigit() and not val.startswith("0"):
            return "long (inferred)"
        return "text + keyword"
    return "object"

if __name__ == "__main__":
    cases = ["00123", "123", "2026-09-23", "true", 42.5]
    print("Simulating Dynamic Field Type Inference:")
    for c in cases:
        print(f"  Input: {repr(c):15s} -> Inferred Type: {infer_type(c)}")
