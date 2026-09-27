# LAB-32: HTTP Missing Host Header

> **Motto**: Never guess when troubleshooting a network failure. Start from the symptom, hypothesize which layer is broken, collect empirical proof, and verify.

---

## 1. Observed Symptom
A developer or monitoring system reports the following alert:
```text
HTTP 400 Bad Request: missing Host header
```

## 2. Investigation Protocol
Do **NOT** consult `solution.md` yet. Use the command line to answer these questions:
1. What layer does this error message originate from?
2. Which tool provides direct visibility into this state? (Hint: `nc / curl -v`)
3. Did any packet leave the sender? Did a reply arrive?
4. What does the kernel state table show?

## 3. Evidence Checklist
Record your observations in `outputs/evidence-template.md`:
- [ ] Command executed and raw output
- [ ] Layer identified: `L7 (HTTP/1.1)`
- [ ] Packet capture or kernel state proof
- [ ] Surgical fix applied and post-fix verification
