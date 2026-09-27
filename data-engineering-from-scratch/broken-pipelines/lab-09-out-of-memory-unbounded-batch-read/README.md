# Out of Memory (OOM) from Unbounded In-Memory Load

> **Category**: `performance`
> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. Problem Description
Using json.load() on a 20 GB file loads the entire syntax tree into RAM, crashing with OOM Killer.

## 2. Failure Symptoms
- Downstream metrics drift, silent row multiplication, or unhandled process termination.
- Pipeline execution exit code may erroneously report `SUCCESS` while data is mathematically corrupt.

## 3. Investigation & Diagnosis
1. Inspect the broken script in `broken_pipeline.py`.
2. Observe how the failure occurs under real input.
3. Compare with the resilient architecture in `solution/fixed_pipeline.py`.

## 4. How to Verify
Run the lab test suite:
```bash
pytest broken-pipelines/lab-09-out-of-memory-unbounded-batch-read/test_lab.py
```
