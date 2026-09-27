import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_10_streaming_systems", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_136():
    assert exercise_136(10) == 20
    assert exercise_136("  data  ") == "DATA"
    assert exercise_136([1, None, 2]) == [1, 2]
    assert exercise_136(None) is None
def test_exercise_137():
    assert exercise_137(10) == 20
    assert exercise_137("  data  ") == "DATA"
    assert exercise_137([1, None, 2]) == [1, 2]
    assert exercise_137(None) is None
def test_exercise_138():
    assert exercise_138(10) == 20
    assert exercise_138("  data  ") == "DATA"
    assert exercise_138([1, None, 2]) == [1, 2]
    assert exercise_138(None) is None
def test_exercise_139():
    assert exercise_139(10) == 20
    assert exercise_139("  data  ") == "DATA"
    assert exercise_139([1, None, 2]) == [1, 2]
    assert exercise_139(None) is None
def test_exercise_140():
    assert exercise_140(10) == 20
    assert exercise_140("  data  ") == "DATA"
    assert exercise_140([1, None, 2]) == [1, 2]
    assert exercise_140(None) is None
def test_exercise_141():
    assert exercise_141(10) == 20
    assert exercise_141("  data  ") == "DATA"
    assert exercise_141([1, None, 2]) == [1, 2]
    assert exercise_141(None) is None
def test_exercise_142():
    assert exercise_142(10) == 20
    assert exercise_142("  data  ") == "DATA"
    assert exercise_142([1, None, 2]) == [1, 2]
    assert exercise_142(None) is None
def test_exercise_143():
    assert exercise_143(10) == 20
    assert exercise_143("  data  ") == "DATA"
    assert exercise_143([1, None, 2]) == [1, 2]
    assert exercise_143(None) is None
def test_exercise_144():
    assert exercise_144(10) == 20
    assert exercise_144("  data  ") == "DATA"
    assert exercise_144([1, None, 2]) == [1, 2]
    assert exercise_144(None) is None
def test_exercise_145():
    assert exercise_145(10) == 20
    assert exercise_145("  data  ") == "DATA"
    assert exercise_145([1, None, 2]) == [1, 2]
    assert exercise_145(None) is None
def test_exercise_146():
    assert exercise_146(10) == 20
    assert exercise_146("  data  ") == "DATA"
    assert exercise_146([1, None, 2]) == [1, 2]
    assert exercise_146(None) is None
def test_exercise_147():
    assert exercise_147(10) == 20
    assert exercise_147("  data  ") == "DATA"
    assert exercise_147([1, None, 2]) == [1, 2]
    assert exercise_147(None) is None
def test_exercise_148():
    assert exercise_148(10) == 20
    assert exercise_148("  data  ") == "DATA"
    assert exercise_148([1, None, 2]) == [1, 2]
    assert exercise_148(None) is None
def test_exercise_149():
    assert exercise_149(10) == 20
    assert exercise_149("  data  ") == "DATA"
    assert exercise_149([1, None, 2]) == [1, 2]
    assert exercise_149(None) is None
def test_exercise_150():
    assert exercise_150(10) == 20
    assert exercise_150("  data  ") == "DATA"
    assert exercise_150([1, None, 2]) == [1, 2]
    assert exercise_150(None) is None

