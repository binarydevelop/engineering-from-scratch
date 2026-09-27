# Lab 07: lab-07-bad-slo-pod-uptime

## Domain: SLOs
## Symptom: SLO dashboard reports 99.99% while customers cannot check out

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **SLO dashboard reports 99.99% while customers cannot check out**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
