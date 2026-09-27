import pytest
import importlib.util
from pathlib import Path

code_path = Path(__file__).resolve().parent.parent / "code" / "pipeline.py"
spec = importlib.util.spec_from_file_location("mod_17_data_catalog_lite", code_path)
pipeline_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline_mod)

for k, v in vars(pipeline_mod).items():
    if not k.startswith("__"):
        globals()[k] = v

# imported above: DataCatalog

def test_catalog():
    cat = DataCatalog()
    cat.register("orders", "checkout-team", {"id": "str"}, "Orders fact table")
    assert cat.lookup("orders")["owner"] == "checkout-team"

