# Contributing to computer-networking-from-scratch

Thank you for your interest in contributing to `computer-networking-from-scratch`!

This repository teaches computer networking deeply from first principles through:
**Understand it. Build it. Send it. Capture it. Break it. Trace it. Debug it. Scale it.**

Every contribution must maintain this rigorous standard.

---

## Guiding Principles

1. **No Magic Incantations**: Every command, script, or configuration flag must be explained from first principles.
2. **Predict Before Capture**: Labs must guide the learner to predict what packets will look like before inspecting `tcpdump`.
3. **Isolate and Protect**: Destructive network mutations must be contained inside Linux network namespaces or Docker containers. Never ask learners to modify host routing or firewalls unsafely.
4. **Pure Python for Simulations**: Protocol simulations in `simulations/` must rely strictly on Python standard library modules (`socket`, `struct`, `time`, `select`, `threading`, `urllib`).
5. **Specification Discipline**: Distinguish standard protocol specs (RFCs), kernel implementation quirks, and operational conventions.

---

## Lesson Structure Requirements

Every lesson added or modified must conform exactly to `LESSON_TEMPLATE.md`:

```text
# Lesson <Number>: <Title>
## Motto
## Problem
## Prediction
## Why this matters
## First principles
## Mental model
## Build / simulate it
## Configure the network
## Send traffic
## Capture it
## Measure it
## Break it
## Trace it
## Debug it
## Modify it
## Evidence
## Questions for mastery
## Production connection
## What comes next
```

---

## Testing & Verification Checklist

Before submitting a Pull Request, run all automated checks:

```bash
# 1. Check environment
./scripts/check-environment.sh

# 2. Run simulation and socket test suites
python3 -m unittest discover -s simulations -p "*_test.py"
python3 -m unittest discover -s projects -p "*_test.py"

# 3. Test compilation of C socket programs
make -C socket-programs/c all
make -C socket-programs/c test
make -C socket-programs/c clean

# 4. Run global test suite
./scripts/run-all-tests.sh
```

---

## Code of Conduct

Maintain an inclusive, technically disciplined, and respectful learning environment.
