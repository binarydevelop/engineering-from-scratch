# Lab 30: lab-30-slow-memory-leak-in-gc

## Domain: Capacity
## Symptom: In-memory cache dictionary never evicts keys

---

## 1. Scenario
An incident has been reported in production. Responders see:
> **In-memory cache dictionary never evicts keys**

## 2. Investigation Guide
1. Inspect the broken configuration / code in this directory.
2. Determine why the failure manifests under real production traffic.
3. Apply the correction according to SRE and observability principles.
4. Verify using `python test_lab.py`.
5. Compare your solution to `broken-systems/solutions/complete-solutions-guide.md`.
