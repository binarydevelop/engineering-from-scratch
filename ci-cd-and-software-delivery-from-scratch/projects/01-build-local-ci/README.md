# Project 01: Build a Local CI Runner from Scratch (Phase 206)

## 1. Project Goal
Before relying on hosted CI platforms (GitHub Actions, GitLab CI), construct a standalone local CI runner engine in Python or Bash that executes a multi-job delivery pipeline locally.

```text
Source Revision ──► DAG Engine ──► Parallel Workers ──► Process Execution ($?) ──► Artifact Ledger
```

## 2. Architectural Requirements
Your local CI engine must:
1. **Parse Pipeline Definitions**: Read a structured JSON or YAML pipeline configuration describing jobs, steps, environment variables, and dependencies.
2. **DAG Dependency Resolution**: Build a Directed Acyclic Graph (DAG) of jobs and perform topological sorting to determine valid execution sequences.
3. **Process Execution & Exit Code Trapping**: Spawn child processes using POSIX primitives, capturing `stdout`, `stderr`, and the termination status `$?`.
4. **Strict Failure Propagation**: If any job fails (`exit != 0`), halt dependent downstream jobs immediately while allowing independent parallel jobs to finish diagnostic data collection.
5. **Simulated Artifact Upload**: Save generated build outputs into an isolated workspace directory with SHA-256 hashes.

## 3. Reference Implementation
The reference implementation is provided in:
[`pipelines/local_runner.py`](../../pipelines/local_runner.py)

## 4. Verification Command
To verify your implementation:
```bash
python3 projects/01-build-local-ci/verify.py
```
