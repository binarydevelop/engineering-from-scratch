import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_09_cdc_replication", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_121():
    assert exercise_121(10) == 20
    assert exercise_121("  data  ") == "DATA"
    assert exercise_121([1, None, 2]) == [1, 2]
    assert exercise_121(None) is None
def test_exercise_122():
    assert exercise_122(10) == 20
    assert exercise_122("  data  ") == "DATA"
    assert exercise_122([1, None, 2]) == [1, 2]
    assert exercise_122(None) is None
def test_exercise_123():
    assert exercise_123(10) == 20
    assert exercise_123("  data  ") == "DATA"
    assert exercise_123([1, None, 2]) == [1, 2]
    assert exercise_123(None) is None
def test_exercise_124():
    assert exercise_124(10) == 20
    assert exercise_124("  data  ") == "DATA"
    assert exercise_124([1, None, 2]) == [1, 2]
    assert exercise_124(None) is None
def test_exercise_125():
    assert exercise_125(10) == 20
    assert exercise_125("  data  ") == "DATA"
    assert exercise_125([1, None, 2]) == [1, 2]
    assert exercise_125(None) is None
def test_exercise_126():
    assert exercise_126(10) == 20
    assert exercise_126("  data  ") == "DATA"
    assert exercise_126([1, None, 2]) == [1, 2]
    assert exercise_126(None) is None
def test_exercise_127():
    assert exercise_127(10) == 20
    assert exercise_127("  data  ") == "DATA"
    assert exercise_127([1, None, 2]) == [1, 2]
    assert exercise_127(None) is None
def test_exercise_128():
    assert exercise_128(10) == 20
    assert exercise_128("  data  ") == "DATA"
    assert exercise_128([1, None, 2]) == [1, 2]
    assert exercise_128(None) is None
def test_exercise_129():
    assert exercise_129(10) == 20
    assert exercise_129("  data  ") == "DATA"
    assert exercise_129([1, None, 2]) == [1, 2]
    assert exercise_129(None) is None
def test_exercise_130():
    assert exercise_130(10) == 20
    assert exercise_130("  data  ") == "DATA"
    assert exercise_130([1, None, 2]) == [1, 2]
    assert exercise_130(None) is None
def test_exercise_131():
    assert exercise_131(10) == 20
    assert exercise_131("  data  ") == "DATA"
    assert exercise_131([1, None, 2]) == [1, 2]
    assert exercise_131(None) is None
def test_exercise_132():
    assert exercise_132(10) == 20
    assert exercise_132("  data  ") == "DATA"
    assert exercise_132([1, None, 2]) == [1, 2]
    assert exercise_132(None) is None
def test_exercise_133():
    assert exercise_133(10) == 20
    assert exercise_133("  data  ") == "DATA"
    assert exercise_133([1, None, 2]) == [1, 2]
    assert exercise_133(None) is None
def test_exercise_134():
    assert exercise_134(10) == 20
    assert exercise_134("  data  ") == "DATA"
    assert exercise_134([1, None, 2]) == [1, 2]
    assert exercise_134(None) is None
def test_exercise_135():
    assert exercise_135(10) == 20
    assert exercise_135("  data  ") == "DATA"
    assert exercise_135([1, None, 2]) == [1, 2]
    assert exercise_135(None) is None

