import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_05_dbt_transformations", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_061():
    assert exercise_061(10) == 20
    assert exercise_061("  data  ") == "DATA"
    assert exercise_061([1, None, 2]) == [1, 2]
    assert exercise_061(None) is None
def test_exercise_062():
    assert exercise_062(10) == 20
    assert exercise_062("  data  ") == "DATA"
    assert exercise_062([1, None, 2]) == [1, 2]
    assert exercise_062(None) is None
def test_exercise_063():
    assert exercise_063(10) == 20
    assert exercise_063("  data  ") == "DATA"
    assert exercise_063([1, None, 2]) == [1, 2]
    assert exercise_063(None) is None
def test_exercise_064():
    assert exercise_064(10) == 20
    assert exercise_064("  data  ") == "DATA"
    assert exercise_064([1, None, 2]) == [1, 2]
    assert exercise_064(None) is None
def test_exercise_065():
    assert exercise_065(10) == 20
    assert exercise_065("  data  ") == "DATA"
    assert exercise_065([1, None, 2]) == [1, 2]
    assert exercise_065(None) is None
def test_exercise_066():
    assert exercise_066(10) == 20
    assert exercise_066("  data  ") == "DATA"
    assert exercise_066([1, None, 2]) == [1, 2]
    assert exercise_066(None) is None
def test_exercise_067():
    assert exercise_067(10) == 20
    assert exercise_067("  data  ") == "DATA"
    assert exercise_067([1, None, 2]) == [1, 2]
    assert exercise_067(None) is None
def test_exercise_068():
    assert exercise_068(10) == 20
    assert exercise_068("  data  ") == "DATA"
    assert exercise_068([1, None, 2]) == [1, 2]
    assert exercise_068(None) is None
def test_exercise_069():
    assert exercise_069(10) == 20
    assert exercise_069("  data  ") == "DATA"
    assert exercise_069([1, None, 2]) == [1, 2]
    assert exercise_069(None) is None
def test_exercise_070():
    assert exercise_070(10) == 20
    assert exercise_070("  data  ") == "DATA"
    assert exercise_070([1, None, 2]) == [1, 2]
    assert exercise_070(None) is None
def test_exercise_071():
    assert exercise_071(10) == 20
    assert exercise_071("  data  ") == "DATA"
    assert exercise_071([1, None, 2]) == [1, 2]
    assert exercise_071(None) is None
def test_exercise_072():
    assert exercise_072(10) == 20
    assert exercise_072("  data  ") == "DATA"
    assert exercise_072([1, None, 2]) == [1, 2]
    assert exercise_072(None) is None
def test_exercise_073():
    assert exercise_073(10) == 20
    assert exercise_073("  data  ") == "DATA"
    assert exercise_073([1, None, 2]) == [1, 2]
    assert exercise_073(None) is None
def test_exercise_074():
    assert exercise_074(10) == 20
    assert exercise_074("  data  ") == "DATA"
    assert exercise_074([1, None, 2]) == [1, 2]
    assert exercise_074(None) is None
def test_exercise_075():
    assert exercise_075(10) == 20
    assert exercise_075("  data  ") == "DATA"
    assert exercise_075([1, None, 2]) == [1, 2]
    assert exercise_075(None) is None

