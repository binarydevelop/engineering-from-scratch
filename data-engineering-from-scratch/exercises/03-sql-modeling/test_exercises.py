import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_03_sql_modeling", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_031():
    assert exercise_031(10) == 20
    assert exercise_031("  data  ") == "DATA"
    assert exercise_031([1, None, 2]) == [1, 2]
    assert exercise_031(None) is None
def test_exercise_032():
    assert exercise_032(10) == 20
    assert exercise_032("  data  ") == "DATA"
    assert exercise_032([1, None, 2]) == [1, 2]
    assert exercise_032(None) is None
def test_exercise_033():
    assert exercise_033(10) == 20
    assert exercise_033("  data  ") == "DATA"
    assert exercise_033([1, None, 2]) == [1, 2]
    assert exercise_033(None) is None
def test_exercise_034():
    assert exercise_034(10) == 20
    assert exercise_034("  data  ") == "DATA"
    assert exercise_034([1, None, 2]) == [1, 2]
    assert exercise_034(None) is None
def test_exercise_035():
    assert exercise_035(10) == 20
    assert exercise_035("  data  ") == "DATA"
    assert exercise_035([1, None, 2]) == [1, 2]
    assert exercise_035(None) is None
def test_exercise_036():
    assert exercise_036(10) == 20
    assert exercise_036("  data  ") == "DATA"
    assert exercise_036([1, None, 2]) == [1, 2]
    assert exercise_036(None) is None
def test_exercise_037():
    assert exercise_037(10) == 20
    assert exercise_037("  data  ") == "DATA"
    assert exercise_037([1, None, 2]) == [1, 2]
    assert exercise_037(None) is None
def test_exercise_038():
    assert exercise_038(10) == 20
    assert exercise_038("  data  ") == "DATA"
    assert exercise_038([1, None, 2]) == [1, 2]
    assert exercise_038(None) is None
def test_exercise_039():
    assert exercise_039(10) == 20
    assert exercise_039("  data  ") == "DATA"
    assert exercise_039([1, None, 2]) == [1, 2]
    assert exercise_039(None) is None
def test_exercise_040():
    assert exercise_040(10) == 20
    assert exercise_040("  data  ") == "DATA"
    assert exercise_040([1, None, 2]) == [1, 2]
    assert exercise_040(None) is None
def test_exercise_041():
    assert exercise_041(10) == 20
    assert exercise_041("  data  ") == "DATA"
    assert exercise_041([1, None, 2]) == [1, 2]
    assert exercise_041(None) is None
def test_exercise_042():
    assert exercise_042(10) == 20
    assert exercise_042("  data  ") == "DATA"
    assert exercise_042([1, None, 2]) == [1, 2]
    assert exercise_042(None) is None
def test_exercise_043():
    assert exercise_043(10) == 20
    assert exercise_043("  data  ") == "DATA"
    assert exercise_043([1, None, 2]) == [1, 2]
    assert exercise_043(None) is None
def test_exercise_044():
    assert exercise_044(10) == 20
    assert exercise_044("  data  ") == "DATA"
    assert exercise_044([1, None, 2]) == [1, 2]
    assert exercise_044(None) is None
def test_exercise_045():
    assert exercise_045(10) == 20
    assert exercise_045("  data  ") == "DATA"
    assert exercise_045([1, None, 2]) == [1, 2]
    assert exercise_045(None) is None

