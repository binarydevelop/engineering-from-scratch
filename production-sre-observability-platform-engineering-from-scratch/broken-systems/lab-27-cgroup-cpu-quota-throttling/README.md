# Lab 27: lab-27-cgroup-cpu-quota-throttling

## Domain: Kubernetes
## Symptom: 100m CPU quota causes 800ms CFS latency spikes

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **100m CPU quota causes 800ms CFS latency spikes**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
