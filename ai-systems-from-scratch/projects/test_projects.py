import os
import sys
import pytest
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from p01_mini_tensor_compiler import MiniTensorCompiler
from p04_mini_inference_scheduler import MiniInferenceScheduler, ScheduledRequest
from p08_evaluation_harness import ProductionEvalHarness, EvalSample
from p10_production_rag_system import ProductionRAGSystem
from p12_coding_agent_sandbox import CodingAgentSandbox

def test_p01_compiler():
    comp = MiniTensorCompiler()
    comp.add("const", [], "c1", value=np.array([[2.0]]))
    comp.add("const", [], "c2", value=np.array([[3.0]]))
    comp.add("add", ["c1", "c2"], "c3")
    comp.outputs = ["c3"]
    comp.optimize()
    res = comp.run({})
    assert res["c3"][0, 0] == 5.0

def test_p04_scheduler():
    sched = MiniInferenceScheduler(max_batch_slots=2, max_blocks=10)
    sched.submit(ScheduledRequest("req1", prompt_len=16, max_tokens=2, priority=2))
    sched.submit(ScheduledRequest("req2", prompt_len=16, max_tokens=2, priority=1))
    
    # Step 1: Pre-fill and 1 token decode
    state1 = sched.step()
    assert state1["active_count"] == 2
    assert state1["finished_count"] == 0

    # Step 2: 2nd token decode -> completion
    state2 = sched.step()
    assert state2["finished_count"] == 2

def test_p08_eval_harness():
    samples = [
        EvalSample("2+2", "4"),
        EvalSample("Capital of UK", "London")
    ]
    harness = ProductionEvalHarness(samples, grader_fn=lambda p, g: g.lower() in p.lower())
    res = harness.evaluate(lambda q: "London is capital" if "UK" in q else "4")
    assert res["accuracy_pct"] == 100.0

def test_p10_rag_system():
    rag = ProductionRAGSystem()
    rag.ingest_document("doc_refund", "Refunds must be requested within 30 days. Customers keep original packaging.")
    results = rag.retrieve("refund 30 days")
    assert len(results) >= 1
    assert results[0][0].doc_id == "doc_refund"
    prompt = rag.build_grounded_prompt("How many days for refund?", results)
    assert "<DOCUMENT id=\"doc_refund\">" in prompt

def test_p12_coding_sandbox():
    sandbox = CodingAgentSandbox()
    sandbox.write_code_file("solution.py", "def add(a, b): return a + b")
    
    test_code = "assert add(2, 3) == 5"
    res = sandbox.run_virtual_tests(test_code, sandbox.virtual_files["solution.py"])
    assert res["passed"] is True

    # Bad solution
    bad_solution = "def add(a, b): return a - b"
    bad_res = sandbox.run_virtual_tests(test_code, bad_solution)
    assert bad_res["passed"] is False
