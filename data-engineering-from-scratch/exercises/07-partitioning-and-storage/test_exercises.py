import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_07_partitioning_and_storage", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_091():
    assert exercise_091(10) == 20
    assert exercise_091("  data  ") == "DATA"
    assert exercise_091([1, None, 2]) == [1, 2]
    assert exercise_091(None) is None
def test_exercise_092():
    assert exercise_092(10) == 20
    assert exercise_092("  data  ") == "DATA"
    assert exercise_092([1, None, 2]) == [1, 2]
    assert exercise_092(None) is None
def test_exercise_093():
    assert exercise_093(10) == 20
    assert exercise_093("  data  ") == "DATA"
    assert exercise_093([1, None, 2]) == [1, 2]
    assert exercise_093(None) is None
def test_exercise_094():
    assert exercise_094(10) == 20
    assert exercise_094("  data  ") == "DATA"
    assert exercise_094([1, None, 2]) == [1, 2]
    assert exercise_094(None) is None
def test_exercise_095():
    assert exercise_095(10) == 20
    assert exercise_095("  data  ") == "DATA"
    assert exercise_095([1, None, 2]) == [1, 2]
    assert exercise_095(None) is None
def test_exercise_096():
    assert exercise_096(10) == 20
    assert exercise_096("  data  ") == "DATA"
    assert exercise_096([1, None, 2]) == [1, 2]
    assert exercise_096(None) is None
def test_exercise_097():
    assert exercise_097(10) == 20
    assert exercise_097("  data  ") == "DATA"
    assert exercise_097([1, None, 2]) == [1, 2]
    assert exercise_097(None) is None
def test_exercise_098():
    assert exercise_098(10) == 20
    assert exercise_098("  data  ") == "DATA"
    assert exercise_098([1, None, 2]) == [1, 2]
    assert exercise_098(None) is None
def test_exercise_099():
    assert exercise_099(10) == 20
    assert exercise_099("  data  ") == "DATA"
    assert exercise_099([1, None, 2]) == [1, 2]
    assert exercise_099(None) is None
def test_exercise_100():
    assert exercise_100(10) == 20
    assert exercise_100("  data  ") == "DATA"
    assert exercise_100([1, None, 2]) == [1, 2]
    assert exercise_100(None) is None
def test_exercise_101():
    assert exercise_101(10) == 20
    assert exercise_101("  data  ") == "DATA"
    assert exercise_101([1, None, 2]) == [1, 2]
    assert exercise_101(None) is None
def test_exercise_102():
    assert exercise_102(10) == 20
    assert exercise_102("  data  ") == "DATA"
    assert exercise_102([1, None, 2]) == [1, 2]
    assert exercise_102(None) is None
def test_exercise_103():
    assert exercise_103(10) == 20
    assert exercise_103("  data  ") == "DATA"
    assert exercise_103([1, None, 2]) == [1, 2]
    assert exercise_103(None) is None
def test_exercise_104():
    assert exercise_104(10) == 20
    assert exercise_104("  data  ") == "DATA"
    assert exercise_104([1, None, 2]) == [1, 2]
    assert exercise_104(None) is None
def test_exercise_105():
    assert exercise_105(10) == 20
    assert exercise_105("  data  ") == "DATA"
    assert exercise_105([1, None, 2]) == [1, 2]
    assert exercise_105(None) is None

