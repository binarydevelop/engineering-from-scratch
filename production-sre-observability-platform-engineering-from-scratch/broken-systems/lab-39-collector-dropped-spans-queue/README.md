# Lab 39: lab-39-collector-dropped-spans-queue

## Domain: OpenTelemetry
## Symptom: Collector buffer queue exhausted during network glitch

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Collector buffer queue exhausted during network glitch**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
