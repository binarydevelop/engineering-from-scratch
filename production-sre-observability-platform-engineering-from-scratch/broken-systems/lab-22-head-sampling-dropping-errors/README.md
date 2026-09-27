# Lab 22: lab-22-head-sampling-dropping-errors

## Domain: OpenTelemetry
## Symptom: 1% head sampling misses 100% of rare 500 error traces

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **1% head sampling misses 100% of rare 500 error traces**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
