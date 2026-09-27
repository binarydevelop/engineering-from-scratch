"""
Tests for 05_global_multi_region_deployment
"""
import importlib.util
from pathlib import Path


def load_module():
    target_path = Path(__file__).resolve().parent.parent / "main.py"
    spec = importlib.util.spec_from_file_location("arch_05_global_multi_region_deployment", target_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_baseline_and_evolved_architecture():
    mod = load_module()
    benchmark_data = mod.run_benchmark()

    assert benchmark_data["baseline_queries"] == 150
    assert benchmark_data["baseline_failures"] > 0
    assert benchmark_data["evolved_queries"] == 150
    assert benchmark_data["evolved_failures"] == 0
