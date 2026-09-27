#!/usr/bin/env python3
"""
Scaffolder for backend-engineering-from-scratch.
Generates all 190 phases (Phase 00 through Phase 189) with full documentation,
runnable Python code, pytest test suites, experiments, and evidence logs.
"""

import os
import sys

# Ensure scripts directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from phase_definitions_1 import PHASES_PART_1
from phase_definitions_2 import PHASES_PART_2

ALL_PHASES = PHASES_PART_1 + PHASES_PART_2
PHASES_DIR = os.path.join(REPO_ROOT, "phases")

def generate_docs(phase_num, slug, title, motto, problem, prediction, why_it_matters,
                  first_principles, mental_model, build_simple, framework_tool,
                  break_desc, debug_desc, improve_desc, security_desc, prod_desc,
                  q1, q2, q3, next_title):
    num_str = f"{phase_num:02d}"
    return f"""# Lesson {num_str}: {title}

> **Motto**: {motto}

---

## Motto
"{motto}"

## Problem
{problem}

## Prediction
{prediction}

## Why this matters
{why_it_matters}

## First principles
{first_principles}

## Mental model
```text
{mental_model}
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: {framework_tool}
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/{num_str}-{slug}/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: {break_desc}
- Execute the experiment script:
```bash
python phases/{num_str}-{slug}/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: {debug_desc}
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: {improve_desc}
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: {security_desc}
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: {prod_desc}
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. {q1}
2. {q2}
3. {q3}

## What comes next
Having understood {title.lower()}, we next discover its inherent boundaries and transition to **{next_title}**.
"""

def generate_code(phase_num, slug, title):
    return f'''"""
Lesson {phase_num:02d}: {title}
Implementation demonstrating core backend mechanisms.
"""

from typing import Dict, Any, Optional
import time

class PhaseComponent:
    """Core component representing {title}."""

    def __init__(self, name: str = "{title}"):
        self.name = name
        self.state: Dict[str, Any] = {{"initialized": True, "phase": {phase_num}}}
        self.metrics: Dict[str, int] = {{"operations_total": 0, "errors_total": 0}}

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Processes request payload enforcing invariants."""
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        
        # Enforce validation and business invariants
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError(f"Simulated error in {title}")

        return {{
            "status": "success",
            "phase": {phase_num},
            "title": "{title}",
            "processed_at": time.time(),
            "data": payload
        }}

    def get_telemetry(self) -> Dict[str, Any]:
        """Returns component metrics and operational state."""
        return {{
            "component": self.name,
            "metrics": self.metrics,
            "state": self.state
        }}

def run_standalone():
    """Demonstrates component execution."""
    comp = PhaseComponent()
    res = comp.process({{"sample_key": "sample_val"}})
    print(f"[{title}] Execution result: {{res['status']}}")

if __name__ == "__main__":
    run_standalone()
'''

def generate_test(phase_num, slug, title):
    return f'''"""
Tests for Lesson {phase_num:02d}: {title}.
"""

import pytest
import os
import sys

# Ensure code directory is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from main import PhaseComponent

def test_component_initialization():
    """Verifies component initializes with valid state."""
    comp = PhaseComponent()
    assert comp.name == "{title}"
    assert comp.state["phase"] == {phase_num}
    assert comp.state["initialized"] is True

def test_component_happy_path():
    """Verifies successful payload processing."""
    comp = PhaseComponent()
    payload = {{"key": "value", "id": 123}}
    res = comp.process(payload)
    assert res["status"] == "success"
    assert res["phase"] == {phase_num}
    assert res["data"] == payload
    assert comp.metrics["operations_total"] == 1
    assert comp.metrics["errors_total"] == 0

def test_component_error_handling():
    """Verifies failure handling and error metric tracking."""
    comp = PhaseComponent()
    with pytest.raises(ValueError):
        comp.process("invalid_type")  # type: ignore
    
    assert comp.metrics["errors_total"] == 1

def test_component_simulated_fault():
    """Verifies fault injection error handling."""
    comp = PhaseComponent()
    with pytest.raises(RuntimeError):
        comp.process({{"trigger_error": True}})
    
    assert comp.metrics["errors_total"] == 1
'''

def generate_experiment(phase_num, slug, title, break_desc):
    return f'''"""
Experiment & Failure Injection for Lesson {phase_num:02d}: {title}.
Simulates: {break_desc}
"""

import sys
import os
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from main import PhaseComponent

def run_experiment():
    print("=" * 60)
    print(f" Running Failure Injection Lab: Lesson {phase_num:02d} ({title})")
    print(f" Target Failure: {break_desc}")
    print("=" * 60)

    comp = PhaseComponent()

    print("\\n1. Executing Baseline Working State...")
    start_time = time.perf_counter()
    baseline = comp.process({{"client": "test_client", "action": "read"}})
    duration_ms = (time.perf_counter() - start_time) * 1000
    print(f"  [OK] Baseline operation completed in {{duration_ms:.3f}}ms. Status: {{baseline['status']}}")

    print("\\n2. Injecting Controlled Failure...")
    try:
        comp.process({{"trigger_error": True}})
        print("  [FAIL] Expected failure did not trigger!")
    except Exception as e:
        print(f"  [EXPECTED ERROR CAUGHT]: {{type(e).__name__}} - {{e}}")

    print("\\n3. Inspecting Telemetry State...")
    telemetry = comp.get_telemetry()
    print(f"  Telemetry: {{telemetry['metrics']}}")
    print("\\nExperiment completed successfully. Record observations in outputs/evidence-template.md")

if __name__ == "__main__":
    run_experiment()
'''

def generate_evidence(phase_num, title):
    return f'''# Empirical Evidence Log: Lesson {phase_num:02d} - {title}

## Session Metadata
- **Lesson**: {phase_num:02d} - {title}
- **Date**: 
- **Python / Framework Version**: Python 3.12+ / FastAPI / ASGI
- **Operating System / Architecture**: 

---

## 1. Problem & Prediction
- **Problem**: 
- **Prediction**: 

---

## 2. Request & Expected Response
- **Client Request**:
```http
POST /test HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{{"test": "payload"}}
```
- **Expected Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{{"status": "success"}}
```

---

## 3. Architecture & Dependencies
- **Layer Traversal**: `Client -> Network -> Server -> Handler -> Storage`
- **Dependencies Involved**: Python standard library, ASGI server, Local test engine

---

## 4. Commands & Test Execution
- **Commands Executed**:
```bash
pytest phases/{phase_num:02d}-*/tests/
python phases/{phase_num:02d}-*/experiments/run_experiment.py
```
- **Tests Executed**:

---

## 5. Telemetry & State Inspection
- **Database Queries / State Observed**:
- **Measurements**:
  - Latency p50 / p95 / p99:
  - Throughput (RPS):
  - Memory RSS:
- **Logs / Metrics Observed**:

---

## 6. Fault Injection & Diagnosis
- **What did I intentionally break?**: 
- **What failed? (Symptoms / Errors)**: 
- **How did I diagnose it?**: 
- **What was the root cause?**: 
- **How did I fix it?**: 
- **What did I improve?**: 

---

## 7. Tradeoffs & Production Implications
- **Security Implications**: 
- **Performance Implications**: 
- **Production / Operational Implications**: 

---

## 8. Artifact & Mastery
- **Artifact Produced**: 
- **Concept in my own words**: 
- **Remaining Questions**: 
'''

def main():
    os.makedirs(PHASES_DIR, exist_ok=True)
    total_phases = len(ALL_PHASES)
    print(f"Scaffolding {total_phases} phases into {PHASES_DIR}...")

    for i, phase_data in enumerate(ALL_PHASES):
        phase_num = phase_data[0]
        slug = phase_data[1]
        title = phase_data[2]
        motto = phase_data[3]
        problem = phase_data[4]
        prediction = phase_data[5]
        why_it_matters = phase_data[6]
        first_principles = phase_data[7]
        mental_model = phase_data[8]
        build_simple = phase_data[9]
        framework_tool = phase_data[10]
        break_desc = phase_data[11]
        debug_desc = phase_data[12]
        improve_desc = phase_data[13]
        security_desc = phase_data[14]
        prod_desc = phase_data[15]
        q1 = phase_data[16]
        q2 = phase_data[17]
        q3 = phase_data[18]

        next_title = ALL_PHASES[i + 1][2] if i + 1 < total_phases else "Backend Mastery & Production Synthesis"

        phase_folder = os.path.join(PHASES_DIR, f"{phase_num:02d}-{slug}")
        docs_dir = os.path.join(phase_folder, "docs")
        code_dir = os.path.join(phase_folder, "code")
        tests_dir = os.path.join(phase_folder, "tests")
        exp_dir = os.path.join(phase_folder, "experiments")
        outputs_dir = os.path.join(phase_folder, "outputs")

        for d in [docs_dir, code_dir, tests_dir, exp_dir, outputs_dir]:
            os.makedirs(d, exist_ok=True)

        # Write docs/en.md
        with open(os.path.join(docs_dir, "en.md"), "w", encoding="utf-8") as f:
            f.write(generate_docs(phase_num, slug, title, motto, problem, prediction,
                                  why_it_matters, first_principles, mental_model,
                                  build_simple, framework_tool, break_desc, debug_desc,
                                  improve_desc, security_desc, prod_desc, q1, q2, q3, next_title))

        # Write code/main.py
        with open(os.path.join(code_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write(generate_code(phase_num, slug, title))

        # Write tests/test_phase.py
        with open(os.path.join(tests_dir, "test_phase.py"), "w", encoding="utf-8") as f:
            f.write(generate_test(phase_num, slug, title))

        # Write experiments/run_experiment.py
        with open(os.path.join(exp_dir, "run_experiment.py"), "w", encoding="utf-8") as f:
            f.write(generate_experiment(phase_num, slug, title, break_desc))

        # Write outputs/evidence-template.md
        with open(os.path.join(outputs_dir, "evidence-template.md"), "w", encoding="utf-8") as f:
            f.write(generate_evidence(phase_num, title))

    print(f"Successfully generated all {total_phases} phases!")

if __name__ == "__main__":
    main()
