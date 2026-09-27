# Lab 04: lab-04-high-cardinality-user-id

## Domain: Prometheus
## Symptom: Prometheus TSDB memory explodes to OOM after adding user_id label

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Prometheus TSDB memory explodes to OOM after adding user_id label**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
