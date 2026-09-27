import sys
import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PHASES_DIR = BASE_DIR / "phases"

def test_phase_count():
    phases = list(PHASES_DIR.glob("*"))
    assert len(phases) == 68, f"Expected 68 phases, found {len(phases)}"

def test_phase_structure():
    for p in sorted(list(PHASES_DIR.glob("*"))):
        assert (p / "docs" / "en.md").exists(), f"{p.name} missing docs/en.md"
        assert (p / "experiments" / "run_experiment.sh").exists(), f"{p.name} missing experiments/run_experiment.sh"
        assert (p / "outputs" / "evidence-template.md").exists(), f"{p.name} missing outputs/evidence-template.md"
        assert (p / "code").exists(), f"{p.name} missing code/"

def test_capstone_1_mini_kafka():
    res = subprocess.run([sys.executable, str(BASE_DIR / "projects/capstone-1-mini-kafka/test_mini_kafka.py")],
                         capture_output=True, text=True)
    assert res.returncode == 0, f"MiniKafka test failed: {res.stderr}"

def test_capstone_2_event_driven_app():
    res = subprocess.run([sys.executable, str(BASE_DIR / "projects/capstone-2-event-driven-app/run_app.py")],
                         capture_output=True, text=True)
    assert res.returncode == 0, f"Capstone 2 failed: {res.stderr}"

def test_docker_compose_validity():
    for compose_file in ["docker-compose.yml", "docker-compose.cluster.yml"]:
        res = subprocess.run(["docker", "compose", "-f", str(BASE_DIR / compose_file), "config"],
                             capture_output=True, text=True)
        assert res.returncode == 0, f"{compose_file} invalid: {res.stderr}"
