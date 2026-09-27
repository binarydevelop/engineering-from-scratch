# Lab 10: lab-10-cascading-retry-storm

## Domain: Reliability
## Symptom: Client retries without backoff multiply load 10x during recovery

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Client retries without backoff multiply load 10x during recovery**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
