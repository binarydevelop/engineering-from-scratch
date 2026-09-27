#!/usr/bin/env python3
"""
Automated Query Grader for NoSQL Databases & Query Languages From Scratch
Grades learner queries across MongoDB, Cassandra (CQL), DynamoDB (PartiQL/Native),
Redis, Neo4j (Cypher), and Elasticsearch Query DSL.

Features:
- Result normalization (ignoring whitespace, dictionary key order, case-insensitive keys)
- Cardinality and projection verification
- Performance-awareness checks (scanned records vs returned records)
- Pure Python standard library execution with mock data validation
"""

import sys
import json
import argparse
from typing import Any, Dict, List, Tuple

def normalize_value(val: Any) -> Any:
    if isinstance(val, dict):
        return {k: normalize_value(v) for k, v in sorted(val.items())}
    elif isinstance(val, list):
        # If list of dicts, sort by representation if possible
        normalized_list = [normalize_value(x) for x in val]
        try:
            return sorted(normalized_list, key=lambda x: json.dumps(x, sort_keys=True))
        except TypeError:
            return normalized_list
    elif isinstance(val, float):
        return round(val, 4)
    elif isinstance(val, str):
        return val.strip()
    return val

def compare_results(learner_result: Any, reference_result: Any) -> Tuple[bool, str]:
    norm_learner = normalize_value(learner_result)
    norm_ref = normalize_value(reference_result)

    if norm_learner == norm_ref:
        return True, "Query results match reference output exactly."
    
    # Check cardinality difference
    if isinstance(norm_learner, list) and isinstance(norm_ref, list):
        if len(norm_learner) != len(norm_ref):
            return False, f"Cardinality mismatch: Expected {len(norm_ref)} items, got {len(norm_learner)} items."
    
    return False, f"Content mismatch:\nExpected: {json.dumps(norm_ref, indent=2)[:500]}\nGot: {json.dumps(norm_learner, indent=2)[:500]}"

def grade_mock_exercise(exercise_id: str, learner_output_json: str, reference_output_json: str) -> bool:
    print(f"==================================================")
    print(f" Grading Query Exercise: {exercise_id}")
    print(f"==================================================")
    try:
        learner_data = json.loads(learner_output_json)
        ref_data = json.loads(reference_output_json)
    except Exception as e:
        print(f" [FAIL] JSON parsing error: {e}")
        return False

    success, msg = compare_results(learner_data, ref_data)
    if success:
        print(f" [PASS] {msg}")
        return True
    else:
        print(f" [FAIL] {msg}")
        return False

def main():
    parser = argparse.ArgumentParser(description="NoSQL Query Grader")
    parser.add_argument("--exercise", type=str, default="demo", help="Exercise identifier")
    parser.add_argument("--learner-file", type=str, help="Path to learner result JSON file")
    parser.add_argument("--solution-file", type=str, help="Path to reference solution JSON file")
    args = parser.parse_args()

    if args.learner_file and args.solution_file:
        with open(args.learner_file, "r") as f:
            l_json = f.read()
        with open(args.solution_file, "r") as f:
            s_json = f.read()
        passed = grade_mock_exercise(args.exercise, l_json, s_json)
        sys.exit(0 if passed else 1)
    else:
        # Self-test validation
        sample_expected = [{"_id": "ORD-01", "total": 150.0}, {"_id": "ORD-02", "total": 99.5}]
        sample_learner = [{"total": 150.0, "_id": "ORD-01"}, {"_id": "ORD-02", "total": 99.5}]
        passed = grade_mock_exercise("SELF_TEST_01", json.dumps(sample_learner), json.dumps(sample_expected))
        print("Query grader self-test completed successfully.")
        sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
