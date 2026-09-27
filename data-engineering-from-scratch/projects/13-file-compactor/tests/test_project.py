import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_13_file_compactor", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: compact_records

def test_compaction():
    chunks = [[{"id": 1}], [{"id": 2}], [{"id": 3}]]
    assert len(compact_records(chunks)) == 3

