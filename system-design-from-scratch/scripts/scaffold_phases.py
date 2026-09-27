#!/usr/bin/env python3
"""
Scaffolds all 201 curriculum phases in `phases/` (Phase 00 through Phase 200).
Generates:
- docs/en.md (Comprehensive lesson based on LESSON_TEMPLATE.md)
- code/main.py (Runnable system component)
- experiments/run_experiment.py (Runnable failure injection & benchmark)
- diagrams/architecture.ascii (ASCII architecture diagrams)
- tests/test_phase.py (Isolated pytest test suite)
- outputs/evidence-template.md (Empirical observation log)
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
PHASES_DIR = os.path.join(REPO_ROOT, "phases")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from phase_definitions_part1 import PHASES_PART_1
from phase_definitions_part2 import PHASES_PART_2

ALL_PHASES = PHASES_PART_1 + PHASES_PART_2

def generate_docs(phase_num, slug, title, problem, first_principles, simple_design, scaled_design, break_desc, tradeoffs):
    next_phase = phase_num + 1 if phase_num < 200 else 200
    return f"""# Phase {phase_num:02d}: {title}

> **Motto**: Understand it. Derive it. Build it. Measure it. Break it. Scale it. Recover it. Ship it.

---

## 1. Problem
{problem}

## 2. Requirements

### Functional Requirements
- Accept client requests and execute core domain processing.
- Maintain consistent state transitions and report execution telemetry.
- Expose clear operational status and failure metrics.

### Non-Functional Requirements
- **Availability**: 99.9% baseline SLA.
- **Latency**: Sub-millisecond local in-memory simulation latency; p99 < 50ms under scaled architecture.
- **Resilience**: Survive simulated dependency failures without unhandled process crashes.

### Out of Scope
- Vendor-specific cloud managed service APIs and external infrastructure billing.

---

## 3. Prediction
Before executing experiments, hypothesize:
> *Under peak load or failure injection, what component will saturate or crash first?*

## 4. Estimates & Numbers
- **Target QPS**: 5,000 requests/sec.
- **Peak Factor**: 2.5x (12,500 peak requests/sec).
- **Network Inbound Bandwidth**: 12,500 req/s * 500 bytes = 6.25 MB/s (50 Mbps).
- **Storage Growth**: 25 GB / day; ~45.6 TB / 5 years with 3x replication.

---

## 5. Why This Matters
In production systems, architectural decisions dictate how systems degrade under stress. Understanding this phase ensures you can design systems that survive real-world constraints without premature over-engineering.

---

## 6. First Principles
{first_principles}

---

## 7. Simplest Design
Start with the minimal working architecture:

```text
[Client] ──▶ [App Server] ──▶ [Primary Datastore]
```
Description: {simple_design}

---

## 8. Build & Simulate It
The accompanying code in `code/main.py` models this subsystem:
- Enforces payload validation and domain constraints.
- Tracks operational metrics (throughput, error count, latency).
- Exposes chaos injection switches.

---

## 9. Measure It
Run baseline performance measurements using `python experiments/run_experiment.py`.
Observe baseline latency, throughput, and error rates.

---

## 10. Break It (Failure Injection)
{break_desc}
Simulate this failure using the chaos switch in `experiments/run_experiment.py`.

---

## 11. Bottleneck Observation
Where does saturation manifest?
- CPU, memory exhaustion, connection starvation, or lock contention.

---

## 12. Evolve the Architecture
To relieve the observed bottleneck, evolve the system:

```text
                               ┌──▶ [Worker Instance 1] ──┬──▶ [Cache]
[Client] ──▶ [Load Balancer] ──┼──▶ [Worker Instance 2] ──┤
                               └──▶ [Worker Instance 3] ──┴──▶ [Primary DB] ──▶ [Replicas]
```
Evolution applied: {scaled_design}

---

## 13. Failure Modes
- New failure mode introduced by the evolved component.
- Mitigation: timeouts, retries with backoff, circuit breaking, or fallbacks.

## 14. Consistency Model
- Guarantees provided (Strong vs Eventual consistency).
- Tradeoffs between immediate consistency and high availability.

## 15. Observability
- **RED Metrics**: Rate (req/s), Errors (count), Duration (p50, p95, p99).
- **Structured Logs**: JSON logs tagged with correlation IDs.

## 16. Security
- Authentication boundaries, input validation, and least privilege access.

## 17. Cost Analysis
- Hardware and cloud resource impact of adding redundancy or caching.

## 18. Architectural Tradeoffs
{tradeoffs}

---

## 19. Alternative Design
What simpler or alternative approach could be used, and why was it not selected?

---

## 20. Evidence
Record your empirical findings in `outputs/evidence-template.md`.

---

## 21. Questions for Mastery
1. What exact metric indicates that this component has reached saturation?
2. How does this architecture behave when a network partition isolates primary nodes?
3. What would you remove if the scale was reduced by 100x?

---

## 22. What Comes Next
Proceed to Phase {next_phase:02d} to build upon these principles.
"""

def generate_code(phase_num, slug, title):
    return f'''"""
Phase {phase_num:02d}: {title}
Core simulation model representing the architectural subsystem.
"""

import time
from typing import Dict, Any, Optional

class PhaseSystem:
    def __init__(self, name: str = "{title}"):
        self.name = name
        self.phase_num = {phase_num}
        self.metrics: Dict[str, Any] = {{
            "requests_total": 0,
            "errors_total": 0,
            "latency_history_ms": []
        }}
        self.chaos_active = False

    def process_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        start = time.perf_counter()
        self.metrics["requests_total"] += 1

        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")

        if self.chaos_active or payload.get("induce_failure", False):
            self.metrics["errors_total"] += 1
            raise RuntimeError(f"Chaos failure triggered in Phase {phase_num:02d}: {title}")

        # Core domain processing
        duration_ms = (time.perf_counter() - start) * 1000.0
        self.metrics["latency_history_ms"].append(duration_ms)

        return {{
            "status": "SUCCESS",
            "phase": self.phase_num,
            "system": self.name,
            "latency_ms": round(duration_ms, 3),
            "data": payload
        }}

    def get_telemetry(self) -> Dict[str, Any]:
        latencies = self.metrics["latency_history_ms"]
        avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
        return {{
            "system": self.name,
            "phase": self.phase_num,
            "requests_total": self.metrics["requests_total"],
            "errors_total": self.metrics["errors_total"],
            "avg_latency_ms": round(avg_lat, 3)
        }}
'''

def generate_experiment(phase_num, slug, title, break_desc):
    return f'''"""
Failure injection and benchmark experiment for Phase {phase_num:02d}: {title}.
Target failure: {break_desc}
"""

import sys
import os
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from main import PhaseSystem

def run_experiment():
    print("=" * 70)
    print(f" Executing Experiment: Phase {phase_num:02d} ({title})")
    print(f" Target Failure: {break_desc}")
    print("=" * 70)

    system = PhaseSystem()

    print("\\n1. Running Baseline Workload...")
    for i in range(10):
        res = system.process_request({{"request_id": f"req_{{i}}", "action": "read"}})
    print(f"  [OK] 10 requests completed. Telemetry: {{system.get_telemetry()}}")

    print("\\n2. Injecting Controlled Failure...")
    system.chaos_active = True
    try:
        system.process_request({{"request_id": "req_fault"}})
        print("  [FAIL] Expected chaos error did not trigger!")
    except RuntimeError as exc:
        print(f"  [OK] Expected fault caught: {{exc}}")

    system.chaos_active = False
    print("\\n3. Verified Recovery After Healing:")
    res_heal = system.process_request({{"request_id": "req_post_heal"}})
    print(f"  [OK] System recovered successfully. Status: {{res_heal['status']}}")
    print("\\nExperiment complete. Record findings in outputs/evidence-template.md")

if __name__ == "__main__":
    run_experiment()
'''

def generate_diagram(phase_num, title, simple_design, scaled_design):
    return f"""======================================================================
  Architecture Diagram: Phase {phase_num:02d} - {title}
======================================================================

1. Simplest Baseline Architecture:
----------------------------------------------------------------------
   {simple_design}

   [Client] ──▶ [Application Server] ──▶ [Primary Datastore]


2. Scaled / Resilient Architecture:
----------------------------------------------------------------------
   {scaled_design}

                               ┌──▶ [Worker Node A] ──┬──▶ [Cache]
[Client] ──▶ [Load Balancer] ──┼──▶ [Worker Node B] ──┤
                               └──▶ [Worker Node C] ──┴──▶ [Primary DB] ──▶ [Replicas]
                                         │
                                         ▼
                                   [Event Queue] ──▶ [Async Workers]

======================================================================
"""

def generate_test(phase_num, slug, title):
    mod_name = f"phase_{phase_num:02d}_{slug.replace('-', '_')}"
    return f'''"""
Pytest verification test for Phase {phase_num:02d}: {title}.
"""

import pytest
import os
import importlib.util

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_FILE = os.path.join(os.path.dirname(TEST_DIR), "code", "main.py")

spec = importlib.util.spec_from_file_location("{mod_name}", CODE_FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
globals().update({{k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")}})

def test_phase_initialization():
    sys = PhaseSystem()
    assert sys.phase_num == {phase_num}
    assert sys.metrics["requests_total"] == 0

def test_phase_happy_path():
    sys = PhaseSystem()
    res = sys.process_request({{"key": "test_value"}})
    assert res["status"] == "SUCCESS"
    assert res["phase"] == {phase_num}
    assert sys.metrics["requests_total"] == 1
    assert sys.metrics["errors_total"] == 0

def test_phase_invalid_payload():
    sys = PhaseSystem()
    with pytest.raises(ValueError):
        sys.process_request("not_a_dictionary")  # type: ignore
    assert sys.metrics["errors_total"] == 1

def test_phase_chaos_failure():
    sys = PhaseSystem()
    sys.chaos_active = True
    with pytest.raises(RuntimeError):
        sys.process_request({{"key": "val"}})
    assert sys.metrics["errors_total"] == 1
'''

def generate_evidence_template(phase_num, title):
    return f"""# Evidence Log: Phase {phase_num:02d} - {title}

## Session Metadata
- **Phase**: {phase_num:02d} - {title}
- **Date**: 
- **Environment**: Python 3.12+

---

## 1. Problem & Hypothesis
- **Problem**: 
- **Hypothesis**: 

---

## 2. Quantitative Measurements
- **Baseline Latency (p50 / p95 / p99)**:
- **Throughput (req/s)**:
- **Error Rate**:

---

## 3. Failure Injection Observations
- **Injected Fault**:
- **Observed Behavior**:
- **Root Cause Analysis**:

---

## 4. Architectural Tradeoffs & Conclusions
- **Component Added**:
- **Benefits**:
- **Downsides / Operational Costs**:
"""

def scaffold_all_phases():
    os.makedirs(PHASES_DIR, exist_ok=True)
    print(f"Scaffolding {len(ALL_PHASES)} phases into {PHASES_DIR}...")
    for phase_num, slug, title, problem, first_principles, simple_design, scaled_design, break_desc, tradeoffs in ALL_PHASES:
        phase_dir = os.path.join(PHASES_DIR, slug)
        docs_dir = os.path.join(phase_dir, "docs")
        code_dir = os.path.join(phase_dir, "code")
        exp_dir = os.path.join(phase_dir, "experiments")
        diag_dir = os.path.join(phase_dir, "diagrams")
        tests_dir = os.path.join(phase_dir, "tests")
        out_dir = os.path.join(phase_dir, "outputs")

        for d in (docs_dir, code_dir, exp_dir, diag_dir, tests_dir, out_dir):
            os.makedirs(d, exist_ok=True)

        with open(os.path.join(docs_dir, "en.md"), "w", encoding="utf-8") as f:
            f.write(generate_docs(phase_num, slug, title, problem, first_principles, simple_design, scaled_design, break_desc, tradeoffs))

        with open(os.path.join(code_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write(generate_code(phase_num, slug, title))

        with open(os.path.join(exp_dir, "run_experiment.py"), "w", encoding="utf-8") as f:
            f.write(generate_experiment(phase_num, slug, title, break_desc))

        with open(os.path.join(diag_dir, "architecture.ascii"), "w", encoding="utf-8") as f:
            f.write(generate_diagram(phase_num, title, simple_design, scaled_design))

        with open(os.path.join(tests_dir, "test_phase.py"), "w", encoding="utf-8") as f:
            f.write(generate_test(phase_num, slug, title))

        with open(os.path.join(out_dir, "evidence-template.md"), "w", encoding="utf-8") as f:
            f.write(generate_evidence_template(phase_num, title))

    print(f"Successfully scaffolded all {len(ALL_PHASES)} phases!")

if __name__ == "__main__":
    scaffold_all_phases()
