import pytest
import importlib.util
from pathlib import Path

def test_fixed_implementation():
    mod_path = Path(__file__).resolve().parent / "solution" / "fixed_pipeline.py"
    spec = importlib.util.spec_from_file_location("sol_lab_08_streaming_watermark_premature_close", mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Inject solution symbols into globals
    for k, v in vars(mod).items():
        if not k.startswith("__"):
            globals()[k] = v

    assert not is_late_watermarked(95, 100, 10) and is_late_watermarked(80, 100, 10)
