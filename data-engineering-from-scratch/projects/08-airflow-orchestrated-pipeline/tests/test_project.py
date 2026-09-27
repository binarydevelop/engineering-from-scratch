import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_08_airflow_orchestrated_pipeline", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: Task, DAGRunner

def test_dag_runner():
    t1 = Task("extract", lambda: None)
    t2 = Task("transform", lambda: None, deps=["extract"])
    runner = DAGRunner([t1, t2])
    executed = runner.run()
    assert executed == ["extract", "transform"] and t2.state == "SUCCESS"

