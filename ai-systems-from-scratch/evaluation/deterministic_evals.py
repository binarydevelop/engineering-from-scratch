"""
Deterministic Evaluation Suite (Phase 113).
High-precision, zero-variance evaluations:
1. Exact Match (normalized string equality).
2. Token F1 Score (precision, recall, and harmonic mean of tokens).
3. Pydantic JSON Schema Validation.
4. Python Syntax / AST Validity.
"""

from typing import Dict, Any, List, Set
import ast
import json
import re
from pydantic import BaseModel, ValidationError

def exact_match(prediction: str, ground_truth: str) -> bool:
    norm_p = " ".join(prediction.strip().lower().split())
    norm_g = " ".join(ground_truth.strip().lower().split())
    return norm_p == norm_g

def token_f1_score(prediction: str, ground_truth: str) -> Dict[str, float]:
    pred_tokens = re.findall(r"\w+", prediction.lower())
    gold_tokens = re.findall(r"\w+", ground_truth.lower())

    if not pred_tokens or not gold_tokens:
        match = float(pred_tokens == gold_tokens)
        return {"precision": match, "recall": match, "f1": match}

    common = set(pred_tokens).intersection(set(gold_tokens))
    num_same = sum(min(pred_tokens.count(tok), gold_tokens.count(tok)) for tok in common)

    if num_same == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    precision = num_same / len(pred_tokens)
    recall = num_same / len(gold_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return {"precision": precision, "recall": recall, "f1": f1}

def validate_json_schema(payload_str: str, schema_class: type[BaseModel]) -> Dict[str, Any]:
    try:
        data = json.loads(payload_str)
        instance = schema_class.model_validate(data)
        return {"valid": True, "data": instance.model_dump(), "error": None}
    except (json.JSONDecodeError, ValidationError) as e:
        return {"valid": False, "data": None, "error": str(e)}

def validate_python_syntax(code_str: str) -> Dict[str, Any]:
    try:
        ast.parse(code_str)
        return {"valid": True, "error": None}
    except SyntaxError as e:
        return {"valid": False, "error": f"SyntaxError at line {e.lineno}: {e.msg}"}
