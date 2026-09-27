import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_10_data_quality_framework", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: QualityEngine

def test_quality_engine():
    data = [{"id": 1}, {"id": 2}]
    assert QualityEngine.check_not_null(data, "id")
    assert QualityEngine.check_unique(data, "id")
    assert not QualityEngine.check_unique([{"id": 1}, {"id": 1}], "id")

