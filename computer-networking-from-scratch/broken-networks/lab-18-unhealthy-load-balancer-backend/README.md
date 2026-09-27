# LAB-18: Unhealthy Load Balancer Backend

> **Motto**: Never guess when troubleshooting a network failure. Start from the symptom, hypothesize which layer is broken, collect empirical proof, and verify.

---

## 1. Observed Symptom
A developer or monitoring system reports the following alert:
```text
50% of client requests randomly fail
```

## 2. Investigation Protocol
Do **NOT** consult `solution.md` yet. Use the command line to answer these questions:
1. What layer does this error message originate from?
2. Which tool provides direct visibility into this state? (Hint: `lb metrics / access log`)
3. Did any packet leave the sender? Did a reply arrive?
4. What does the kernel state table show?

## 3. Evidence Checklist
Record your observations in `outputs/evidence-template.md`:
- [ ] Command executed and raw output
- [ ] Layer identified: `L7 (Load Balancing)`
- [ ] Packet capture or kernel state proof
- [ ] Surgical fix applied and post-fix verification
