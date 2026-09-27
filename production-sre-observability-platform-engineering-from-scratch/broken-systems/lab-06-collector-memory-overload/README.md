# Lab 06: lab-06-collector-memory-overload

## Domain: OpenTelemetry
## Symptom: Collector killed by Linux OOM killer due to missing memory_limiter

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **Collector killed by Linux OOM killer due to missing memory_limiter**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
