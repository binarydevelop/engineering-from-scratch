import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_09_streaming_aggregation_engine", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: StreamAggregator

def test_stream_agg():
    agg = StreamAggregator()
    agg.add_event("w1", 10)
    agg.add_event("w1", 20)
    assert agg.get_window("w1") == 30

