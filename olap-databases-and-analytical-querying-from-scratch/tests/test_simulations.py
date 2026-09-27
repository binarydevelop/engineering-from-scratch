import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_script(script_rel_path: str):
    script_path = REPO_ROOT / script_rel_path
    assert script_path.exists(), f"{script_path} does not exist"
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    assert res.returncode == 0, f"Script {script_rel_path} failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"

def test_simulation_row_vs_column():
    run_script("simulations/row_vs_column_sim.py")

def test_simulation_compression():
    run_script("simulations/compression_sim.py")

def test_simulation_vectorized_exec():
    run_script("simulations/vectorized_exec_sim.py")

def test_simulation_zonemap_skipping():
    run_script("simulations/zonemap_skipping_sim.py")

def test_simulation_bloom_filter():
    run_script("simulations/bloom_filter_sim.py")

def test_simulation_hyperloglog():
    run_script("simulations/hyperloglog_sim.py")

def test_simulation_tdigest():
    run_script("simulations/tdigest_percentiles_sim.py")

def test_simulation_distributed_shuffle():
    run_script("simulations/distributed_shuffle_sim.py")
