# Lab 31: lab-31-async-event-loop-blocked

## Domain: Reliability
## Symptom: Synchronous file read inside async route blocks entire server

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Synchronous file read inside async route blocks entire server**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
