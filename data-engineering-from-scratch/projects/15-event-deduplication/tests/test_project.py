import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_15_event_deduplication", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: EventDeduplicator

def test_dedup():
    dedup = EventDeduplicator()
    assert not dedup.is_duplicate("e1")
    assert dedup.is_duplicate("e1")

