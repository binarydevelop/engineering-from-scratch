# Lab 18: lab-18-proxy-timeout-mismatch

## Domain: Networking
## Symptom: Gateway times out in 2s while backend runs for 30s

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Gateway times out in 2s while backend runs for 30s**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
