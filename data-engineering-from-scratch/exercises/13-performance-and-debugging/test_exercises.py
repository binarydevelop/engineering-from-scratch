import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_13_performance_and_debugging", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_176():
    assert exercise_176(10) == 20
    assert exercise_176("  data  ") == "DATA"
    assert exercise_176([1, None, 2]) == [1, 2]
    assert exercise_176(None) is None
def test_exercise_177():
    assert exercise_177(10) == 20
    assert exercise_177("  data  ") == "DATA"
    assert exercise_177([1, None, 2]) == [1, 2]
    assert exercise_177(None) is None
def test_exercise_178():
    assert exercise_178(10) == 20
    assert exercise_178("  data  ") == "DATA"
    assert exercise_178([1, None, 2]) == [1, 2]
    assert exercise_178(None) is None
def test_exercise_179():
    assert exercise_179(10) == 20
    assert exercise_179("  data  ") == "DATA"
    assert exercise_179([1, None, 2]) == [1, 2]
    assert exercise_179(None) is None
def test_exercise_180():
    assert exercise_180(10) == 20
    assert exercise_180("  data  ") == "DATA"
    assert exercise_180([1, None, 2]) == [1, 2]
    assert exercise_180(None) is None
def test_exercise_181():
    assert exercise_181(10) == 20
    assert exercise_181("  data  ") == "DATA"
    assert exercise_181([1, None, 2]) == [1, 2]
    assert exercise_181(None) is None
def test_exercise_182():
    assert exercise_182(10) == 20
    assert exercise_182("  data  ") == "DATA"
    assert exercise_182([1, None, 2]) == [1, 2]
    assert exercise_182(None) is None
def test_exercise_183():
    assert exercise_183(10) == 20
    assert exercise_183("  data  ") == "DATA"
    assert exercise_183([1, None, 2]) == [1, 2]
    assert exercise_183(None) is None
def test_exercise_184():
    assert exercise_184(10) == 20
    assert exercise_184("  data  ") == "DATA"
    assert exercise_184([1, None, 2]) == [1, 2]
    assert exercise_184(None) is None
def test_exercise_185():
    assert exercise_185(10) == 20
    assert exercise_185("  data  ") == "DATA"
    assert exercise_185([1, None, 2]) == [1, 2]
    assert exercise_185(None) is None

