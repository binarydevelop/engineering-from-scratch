# LAB-27: Bufferbloat Latency Inflation

> **Motto**: Never guess when troubleshooting a network failure. Start from the symptom, hypothesize which layer is broken, collect empirical proof, and verify.

---

## 1. Observed Symptom
A developer or monitoring system reports the following alert:
```text
Interactive SSH lag and ping RTT spikes to 3000ms under load
```

## 2. Investigation Protocol
Do **NOT** consult `solution.md` yet. Use the command line to answer these questions:
1. What layer does this error message originate from?
2. Which tool provides direct visibility into this state? (Hint: `ping while saturating pipe`)
3. Did any packet leave the sender? Did a reply arrive?
4. What does the kernel state table show?

## 3. Evidence Checklist
Record your observations in `outputs/evidence-template.md`:
- [ ] Command executed and raw output
- [ ] Layer identified: `L3 / L4 (Queueing)`
- [ ] Packet capture or kernel state proof
- [ ] Surgical fix applied and post-fix verification
