import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_02_ingestion", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_016():
    assert exercise_016(10) == 20
    assert exercise_016("  data  ") == "DATA"
    assert exercise_016([1, None, 2]) == [1, 2]
    assert exercise_016(None) is None
def test_exercise_017():
    assert exercise_017(10) == 20
    assert exercise_017("  data  ") == "DATA"
    assert exercise_017([1, None, 2]) == [1, 2]
    assert exercise_017(None) is None
def test_exercise_018():
    assert exercise_018(10) == 20
    assert exercise_018("  data  ") == "DATA"
    assert exercise_018([1, None, 2]) == [1, 2]
    assert exercise_018(None) is None
def test_exercise_019():
    assert exercise_019(10) == 20
    assert exercise_019("  data  ") == "DATA"
    assert exercise_019([1, None, 2]) == [1, 2]
    assert exercise_019(None) is None
def test_exercise_020():
    assert exercise_020(10) == 20
    assert exercise_020("  data  ") == "DATA"
    assert exercise_020([1, None, 2]) == [1, 2]
    assert exercise_020(None) is None
def test_exercise_021():
    assert exercise_021(10) == 20
    assert exercise_021("  data  ") == "DATA"
    assert exercise_021([1, None, 2]) == [1, 2]
    assert exercise_021(None) is None
def test_exercise_022():
    assert exercise_022(10) == 20
    assert exercise_022("  data  ") == "DATA"
    assert exercise_022([1, None, 2]) == [1, 2]
    assert exercise_022(None) is None
def test_exercise_023():
    assert exercise_023(10) == 20
    assert exercise_023("  data  ") == "DATA"
    assert exercise_023([1, None, 2]) == [1, 2]
    assert exercise_023(None) is None
def test_exercise_024():
    assert exercise_024(10) == 20
    assert exercise_024("  data  ") == "DATA"
    assert exercise_024([1, None, 2]) == [1, 2]
    assert exercise_024(None) is None
def test_exercise_025():
    assert exercise_025(10) == 20
    assert exercise_025("  data  ") == "DATA"
    assert exercise_025([1, None, 2]) == [1, 2]
    assert exercise_025(None) is None
def test_exercise_026():
    assert exercise_026(10) == 20
    assert exercise_026("  data  ") == "DATA"
    assert exercise_026([1, None, 2]) == [1, 2]
    assert exercise_026(None) is None
def test_exercise_027():
    assert exercise_027(10) == 20
    assert exercise_027("  data  ") == "DATA"
    assert exercise_027([1, None, 2]) == [1, 2]
    assert exercise_027(None) is None
def test_exercise_028():
    assert exercise_028(10) == 20
    assert exercise_028("  data  ") == "DATA"
    assert exercise_028([1, None, 2]) == [1, 2]
    assert exercise_028(None) is None
def test_exercise_029():
    assert exercise_029(10) == 20
    assert exercise_029("  data  ") == "DATA"
    assert exercise_029([1, None, 2]) == [1, 2]
    assert exercise_029(None) is None
def test_exercise_030():
    assert exercise_030(10) == 20
    assert exercise_030("  data  ") == "DATA"
    assert exercise_030([1, None, 2]) == [1, 2]
    assert exercise_030(None) is None

