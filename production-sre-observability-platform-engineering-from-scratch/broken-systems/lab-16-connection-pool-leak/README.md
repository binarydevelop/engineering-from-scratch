# Lab 16: lab-16-connection-pool-leak

## Domain: Database
## Symptom: Worker fails to return connection on error, exhausting pool

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Worker fails to return connection on error, exhausting pool**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
