import os
import sys
import pytest
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(__file__))

from deterministic_evals import exact_match, token_f1_score, validate_json_schema, validate_python_syntax
from llm_as_judge import LLMPairwiseJudge
from regression_suite import TestCase, RegressionSuiteRunner
from slice_evaluator import SliceEvaluator
from statistical_significance import wilson_score_interval, compare_evaluation_claims

class OrderSchema(BaseModel):
    order_id: int
    item: str
    price: float

def test_deterministic_evals():
    assert exact_match("  hello WORLD! ", "hello world!") is True
    
    f1 = token_f1_score("the quick brown fox", "the fast brown fox")
    assert f1["f1"] == 0.75

    valid_json = '{"order_id": 123, "item": "laptop", "price": 999.50}'
    res = validate_json_schema(valid_json, OrderSchema)
    assert res["valid"] is True

    invalid_json = '{"order_id": "not_an_int"}'
    res_bad = validate_json_schema(invalid_json, OrderSchema)
    assert res_bad["valid"] is False

    assert validate_python_syntax("def add(a, b): return a + b")["valid"] is True
    assert validate_python_syntax("def broken(:")["valid"] is False

def test_llm_judge_debiasing():
    # Simulate a judge that always favors choice A (position bias)
    judge = LLMPairwiseJudge(judge_fn=lambda p, a, b: "[[A]]")
    res = judge.evaluate_pairwise("Which is better?", "Candidate 1", "Candidate 2")
    assert res["position_bias_detected"] is True
    assert res["consensus_winner"] == "TIE_OR_BIASED"

def test_regression_suite():
    cases = [
        TestCase("c1", "What is capital of France?", "Paris"),
        TestCase("c2", "What is 2+2?", "4")
    ]
    runner = RegressionSuiteRunner(cases)
    # Dummy model answering correctly
    model = lambda q: "Paris is France capital" if "France" in q else "4"
    res = runner.run_suite(model)
    assert res["pass_rate"] == 1.0

def test_slice_evaluator():
    records = [
        {"prompt": "Short query", "domain": "math"},
        {"prompt": "A " * 60, "domain": "math"}, # medium
    ]
    report = SliceEvaluator.evaluate_slices(records, eval_fn=lambda r: True)
    assert report["length"]["short"] == 1.0
    assert report["domain"]["math"] == 1.0

def test_statistical_significance():
    # 70 successes out of 100
    p, low, high = wilson_score_interval(70, 100)
    assert 0.60 < low < 0.70
    assert 0.70 < high < 0.80

    # 70/100 vs 72/100 -> intervals overlap!
    comp = compare_evaluation_claims(70, 72, 100)
    assert comp["statistically_significant"] is False
