import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_03_cdc_pipeline", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: CDCReplicator

def test_cdc_replication():
    cdc = CDCReplicator()
    cdc.apply_event({"lsn": 10, "op": "INSERT", "key": "k1", "payload": "v1"})
    cdc.apply_event({"lsn": 11, "op": "UPDATE", "key": "k1", "payload": "v2"})
    assert cdc.state["k1"] == "v2" and cdc.last_lsn == 11
    # Duplicate event
    assert not cdc.apply_event({"lsn": 11, "op": "UPDATE", "key": "k1", "payload": "v2"})

