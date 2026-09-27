import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_11_data_quality_and_contracts", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_151():
    assert exercise_151(10) == 20
    assert exercise_151("  data  ") == "DATA"
    assert exercise_151([1, None, 2]) == [1, 2]
    assert exercise_151(None) is None
def test_exercise_152():
    assert exercise_152(10) == 20
    assert exercise_152("  data  ") == "DATA"
    assert exercise_152([1, None, 2]) == [1, 2]
    assert exercise_152(None) is None
def test_exercise_153():
    assert exercise_153(10) == 20
    assert exercise_153("  data  ") == "DATA"
    assert exercise_153([1, None, 2]) == [1, 2]
    assert exercise_153(None) is None
def test_exercise_154():
    assert exercise_154(10) == 20
    assert exercise_154("  data  ") == "DATA"
    assert exercise_154([1, None, 2]) == [1, 2]
    assert exercise_154(None) is None
def test_exercise_155():
    assert exercise_155(10) == 20
    assert exercise_155("  data  ") == "DATA"
    assert exercise_155([1, None, 2]) == [1, 2]
    assert exercise_155(None) is None
def test_exercise_156():
    assert exercise_156(10) == 20
    assert exercise_156("  data  ") == "DATA"
    assert exercise_156([1, None, 2]) == [1, 2]
    assert exercise_156(None) is None
def test_exercise_157():
    assert exercise_157(10) == 20
    assert exercise_157("  data  ") == "DATA"
    assert exercise_157([1, None, 2]) == [1, 2]
    assert exercise_157(None) is None
def test_exercise_158():
    assert exercise_158(10) == 20
    assert exercise_158("  data  ") == "DATA"
    assert exercise_158([1, None, 2]) == [1, 2]
    assert exercise_158(None) is None
def test_exercise_159():
    assert exercise_159(10) == 20
    assert exercise_159("  data  ") == "DATA"
    assert exercise_159([1, None, 2]) == [1, 2]
    assert exercise_159(None) is None
def test_exercise_160():
    assert exercise_160(10) == 20
    assert exercise_160("  data  ") == "DATA"
    assert exercise_160([1, None, 2]) == [1, 2]
    assert exercise_160(None) is None
def test_exercise_161():
    assert exercise_161(10) == 20
    assert exercise_161("  data  ") == "DATA"
    assert exercise_161([1, None, 2]) == [1, 2]
    assert exercise_161(None) is None
def test_exercise_162():
    assert exercise_162(10) == 20
    assert exercise_162("  data  ") == "DATA"
    assert exercise_162([1, None, 2]) == [1, 2]
    assert exercise_162(None) is None
def test_exercise_163():
    assert exercise_163(10) == 20
    assert exercise_163("  data  ") == "DATA"
    assert exercise_163([1, None, 2]) == [1, 2]
    assert exercise_163(None) is None
def test_exercise_164():
    assert exercise_164(10) == 20
    assert exercise_164("  data  ") == "DATA"
    assert exercise_164([1, None, 2]) == [1, 2]
    assert exercise_164(None) is None
def test_exercise_165():
    assert exercise_165(10) == 20
    assert exercise_165("  data  ") == "DATA"
    assert exercise_165([1, None, 2]) == [1, 2]
    assert exercise_165(None) is None

