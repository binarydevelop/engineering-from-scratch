import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_04_warehousing", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_046():
    assert exercise_046(10) == 20
    assert exercise_046("  data  ") == "DATA"
    assert exercise_046([1, None, 2]) == [1, 2]
    assert exercise_046(None) is None
def test_exercise_047():
    assert exercise_047(10) == 20
    assert exercise_047("  data  ") == "DATA"
    assert exercise_047([1, None, 2]) == [1, 2]
    assert exercise_047(None) is None
def test_exercise_048():
    assert exercise_048(10) == 20
    assert exercise_048("  data  ") == "DATA"
    assert exercise_048([1, None, 2]) == [1, 2]
    assert exercise_048(None) is None
def test_exercise_049():
    assert exercise_049(10) == 20
    assert exercise_049("  data  ") == "DATA"
    assert exercise_049([1, None, 2]) == [1, 2]
    assert exercise_049(None) is None
def test_exercise_050():
    assert exercise_050(10) == 20
    assert exercise_050("  data  ") == "DATA"
    assert exercise_050([1, None, 2]) == [1, 2]
    assert exercise_050(None) is None
def test_exercise_051():
    assert exercise_051(10) == 20
    assert exercise_051("  data  ") == "DATA"
    assert exercise_051([1, None, 2]) == [1, 2]
    assert exercise_051(None) is None
def test_exercise_052():
    assert exercise_052(10) == 20
    assert exercise_052("  data  ") == "DATA"
    assert exercise_052([1, None, 2]) == [1, 2]
    assert exercise_052(None) is None
def test_exercise_053():
    assert exercise_053(10) == 20
    assert exercise_053("  data  ") == "DATA"
    assert exercise_053([1, None, 2]) == [1, 2]
    assert exercise_053(None) is None
def test_exercise_054():
    assert exercise_054(10) == 20
    assert exercise_054("  data  ") == "DATA"
    assert exercise_054([1, None, 2]) == [1, 2]
    assert exercise_054(None) is None
def test_exercise_055():
    assert exercise_055(10) == 20
    assert exercise_055("  data  ") == "DATA"
    assert exercise_055([1, None, 2]) == [1, 2]
    assert exercise_055(None) is None
def test_exercise_056():
    assert exercise_056(10) == 20
    assert exercise_056("  data  ") == "DATA"
    assert exercise_056([1, None, 2]) == [1, 2]
    assert exercise_056(None) is None
def test_exercise_057():
    assert exercise_057(10) == 20
    assert exercise_057("  data  ") == "DATA"
    assert exercise_057([1, None, 2]) == [1, 2]
    assert exercise_057(None) is None
def test_exercise_058():
    assert exercise_058(10) == 20
    assert exercise_058("  data  ") == "DATA"
    assert exercise_058([1, None, 2]) == [1, 2]
    assert exercise_058(None) is None
def test_exercise_059():
    assert exercise_059(10) == 20
    assert exercise_059("  data  ") == "DATA"
    assert exercise_059([1, None, 2]) == [1, 2]
    assert exercise_059(None) is None
def test_exercise_060():
    assert exercise_060(10) == 20
    assert exercise_060("  data  ") == "DATA"
    assert exercise_060([1, None, 2]) == [1, 2]
    assert exercise_060(None) is None

