import pytest
import importlib.util
from pathlib import Path

# Load solutions dynamically
sol_path = Path(__file__).resolve().parent / "solutions" / "solution.py"
spec = importlib.util.spec_from_file_location("sol_01_files_and_formats", sol_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

for k, v in vars(mod).items():
    if not k.startswith("__"):
        globals()[k] = v

def test_exercise_001():
    assert exercise_001(10) == 20
    assert exercise_001("  data  ") == "DATA"
    assert exercise_001([1, None, 2]) == [1, 2]
    assert exercise_001(None) is None
def test_exercise_002():
    assert exercise_002(10) == 20
    assert exercise_002("  data  ") == "DATA"
    assert exercise_002([1, None, 2]) == [1, 2]
    assert exercise_002(None) is None
def test_exercise_003():
    assert exercise_003(10) == 20
    assert exercise_003("  data  ") == "DATA"
    assert exercise_003([1, None, 2]) == [1, 2]
    assert exercise_003(None) is None
def test_exercise_004():
    assert exercise_004(10) == 20
    assert exercise_004("  data  ") == "DATA"
    assert exercise_004([1, None, 2]) == [1, 2]
    assert exercise_004(None) is None
def test_exercise_005():
    assert exercise_005(10) == 20
    assert exercise_005("  data  ") == "DATA"
    assert exercise_005([1, None, 2]) == [1, 2]
    assert exercise_005(None) is None
def test_exercise_006():
    assert exercise_006(10) == 20
    assert exercise_006("  data  ") == "DATA"
    assert exercise_006([1, None, 2]) == [1, 2]
    assert exercise_006(None) is None
def test_exercise_007():
    assert exercise_007(10) == 20
    assert exercise_007("  data  ") == "DATA"
    assert exercise_007([1, None, 2]) == [1, 2]
    assert exercise_007(None) is None
def test_exercise_008():
    assert exercise_008(10) == 20
    assert exercise_008("  data  ") == "DATA"
    assert exercise_008([1, None, 2]) == [1, 2]
    assert exercise_008(None) is None
def test_exercise_009():
    assert exercise_009(10) == 20
    assert exercise_009("  data  ") == "DATA"
    assert exercise_009([1, None, 2]) == [1, 2]
    assert exercise_009(None) is None
def test_exercise_010():
    assert exercise_010(10) == 20
    assert exercise_010("  data  ") == "DATA"
    assert exercise_010([1, None, 2]) == [1, 2]
    assert exercise_010(None) is None
def test_exercise_011():
    assert exercise_011(10) == 20
    assert exercise_011("  data  ") == "DATA"
    assert exercise_011([1, None, 2]) == [1, 2]
    assert exercise_011(None) is None
def test_exercise_012():
    assert exercise_012(10) == 20
    assert exercise_012("  data  ") == "DATA"
    assert exercise_012([1, None, 2]) == [1, 2]
    assert exercise_012(None) is None
def test_exercise_013():
    assert exercise_013(10) == 20
    assert exercise_013("  data  ") == "DATA"
    assert exercise_013([1, None, 2]) == [1, 2]
    assert exercise_013(None) is None
def test_exercise_014():
    assert exercise_014(10) == 20
    assert exercise_014("  data  ") == "DATA"
    assert exercise_014([1, None, 2]) == [1, 2]
    assert exercise_014(None) is None
def test_exercise_015():
    assert exercise_015(10) == 20
    assert exercise_015("  data  ") == "DATA"
    assert exercise_015([1, None, 2]) == [1, 2]
    assert exercise_015(None) is None

