import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_12_lineage_and_metadata", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_166():
    assert exercise_166(10) == 20
    assert exercise_166("  data  ") == "DATA"
    assert exercise_166([1, None, 2]) == [1, 2]
    assert exercise_166(None) is None
def test_exercise_167():
    assert exercise_167(10) == 20
    assert exercise_167("  data  ") == "DATA"
    assert exercise_167([1, None, 2]) == [1, 2]
    assert exercise_167(None) is None
def test_exercise_168():
    assert exercise_168(10) == 20
    assert exercise_168("  data  ") == "DATA"
    assert exercise_168([1, None, 2]) == [1, 2]
    assert exercise_168(None) is None
def test_exercise_169():
    assert exercise_169(10) == 20
    assert exercise_169("  data  ") == "DATA"
    assert exercise_169([1, None, 2]) == [1, 2]
    assert exercise_169(None) is None
def test_exercise_170():
    assert exercise_170(10) == 20
    assert exercise_170("  data  ") == "DATA"
    assert exercise_170([1, None, 2]) == [1, 2]
    assert exercise_170(None) is None
def test_exercise_171():
    assert exercise_171(10) == 20
    assert exercise_171("  data  ") == "DATA"
    assert exercise_171([1, None, 2]) == [1, 2]
    assert exercise_171(None) is None
def test_exercise_172():
    assert exercise_172(10) == 20
    assert exercise_172("  data  ") == "DATA"
    assert exercise_172([1, None, 2]) == [1, 2]
    assert exercise_172(None) is None
def test_exercise_173():
    assert exercise_173(10) == 20
    assert exercise_173("  data  ") == "DATA"
    assert exercise_173([1, None, 2]) == [1, 2]
    assert exercise_173(None) is None
def test_exercise_174():
    assert exercise_174(10) == 20
    assert exercise_174("  data  ") == "DATA"
    assert exercise_174([1, None, 2]) == [1, 2]
    assert exercise_174(None) is None
def test_exercise_175():
    assert exercise_175(10) == 20
    assert exercise_175("  data  ") == "DATA"
    assert exercise_175([1, None, 2]) == [1, 2]
    assert exercise_175(None) is None

