# Lab 26: lab-26-flapping-alert-hysteresis

## Domain: Alerting
## Symptom: Alert fires and resolves every 15s due to missing for: window

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Alert fires and resolves every 15s due to missing for: window**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
