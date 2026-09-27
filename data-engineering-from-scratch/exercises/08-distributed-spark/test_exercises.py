import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_08_distributed_spark", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_106():
    assert exercise_106(10) == 20
    assert exercise_106("  data  ") == "DATA"
    assert exercise_106([1, None, 2]) == [1, 2]
    assert exercise_106(None) is None
def test_exercise_107():
    assert exercise_107(10) == 20
    assert exercise_107("  data  ") == "DATA"
    assert exercise_107([1, None, 2]) == [1, 2]
    assert exercise_107(None) is None
def test_exercise_108():
    assert exercise_108(10) == 20
    assert exercise_108("  data  ") == "DATA"
    assert exercise_108([1, None, 2]) == [1, 2]
    assert exercise_108(None) is None
def test_exercise_109():
    assert exercise_109(10) == 20
    assert exercise_109("  data  ") == "DATA"
    assert exercise_109([1, None, 2]) == [1, 2]
    assert exercise_109(None) is None
def test_exercise_110():
    assert exercise_110(10) == 20
    assert exercise_110("  data  ") == "DATA"
    assert exercise_110([1, None, 2]) == [1, 2]
    assert exercise_110(None) is None
def test_exercise_111():
    assert exercise_111(10) == 20
    assert exercise_111("  data  ") == "DATA"
    assert exercise_111([1, None, 2]) == [1, 2]
    assert exercise_111(None) is None
def test_exercise_112():
    assert exercise_112(10) == 20
    assert exercise_112("  data  ") == "DATA"
    assert exercise_112([1, None, 2]) == [1, 2]
    assert exercise_112(None) is None
def test_exercise_113():
    assert exercise_113(10) == 20
    assert exercise_113("  data  ") == "DATA"
    assert exercise_113([1, None, 2]) == [1, 2]
    assert exercise_113(None) is None
def test_exercise_114():
    assert exercise_114(10) == 20
    assert exercise_114("  data  ") == "DATA"
    assert exercise_114([1, None, 2]) == [1, 2]
    assert exercise_114(None) is None
def test_exercise_115():
    assert exercise_115(10) == 20
    assert exercise_115("  data  ") == "DATA"
    assert exercise_115([1, None, 2]) == [1, 2]
    assert exercise_115(None) is None
def test_exercise_116():
    assert exercise_116(10) == 20
    assert exercise_116("  data  ") == "DATA"
    assert exercise_116([1, None, 2]) == [1, 2]
    assert exercise_116(None) is None
def test_exercise_117():
    assert exercise_117(10) == 20
    assert exercise_117("  data  ") == "DATA"
    assert exercise_117([1, None, 2]) == [1, 2]
    assert exercise_117(None) is None
def test_exercise_118():
    assert exercise_118(10) == 20
    assert exercise_118("  data  ") == "DATA"
    assert exercise_118([1, None, 2]) == [1, 2]
    assert exercise_118(None) is None
def test_exercise_119():
    assert exercise_119(10) == 20
    assert exercise_119("  data  ") == "DATA"
    assert exercise_119([1, None, 2]) == [1, 2]
    assert exercise_119(None) is None
def test_exercise_120():
    assert exercise_120(10) == 20
    assert exercise_120("  data  ") == "DATA"
    assert exercise_120([1, None, 2]) == [1, 2]
    assert exercise_120(None) is None

