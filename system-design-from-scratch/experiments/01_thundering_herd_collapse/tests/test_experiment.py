"""
Tests for 01_thundering_herd_collapse
"""
import importlib.util
from pathlib import Path


def load_module():
    target_path = Path(__file__).resolve().parent.parent / "experiment.py"
    spec = importlib.util.spec_from_file_location("exp_01_thundering_herd_collapse", target_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_experiment_defense_mechanism():
    mod = load_module()
    results = mod.execute_experiment()

    assert results["unprotected"]["degraded"] is True
    assert results["protected"]["degraded"] is False
    assert results["defense_effective"] is True
