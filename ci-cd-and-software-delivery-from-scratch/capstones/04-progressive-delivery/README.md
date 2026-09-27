# Capstone 4: Progressive Canary Delivery with Automated Abort

## 1. Challenge Prompt
> "Design a progressive delivery system that safely rolls out releases across 1% -> 10% -> 50% -> 100% traffic increments, actively monitoring error rates and latency, and automatically halting and reverting upon regression."

---

## 2. Architectural Requirements & Invariants
- [ ] Traffic progression across 4 defined stages
- [ ] Statistical health evaluation at each stage
- [ ] Automated abort condition triggered if 5xx errors exceed 0.5%
- [ ] Instant route cut to 0% with blast radius restricted to canary percentage
- [ ] Comprehensive post-mortem telemetry export

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/04-progressive-delivery/verify.py
```
