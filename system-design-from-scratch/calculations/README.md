# Back-of-the-Envelope Estimation Drills

This directory contains **105 back-of-the-envelope estimation drills** designed to build rapid mathematical fluency for system design.

---

## 1. Categories Covered (105 Drills)

1. **Traffic & RPS Estimation** (Drills 1–15): DAU to RPS conversions, peak factors, read/write ratios.
2. **Storage Growth & Retention** (Drills 16–30): Per-record storage, index overhead, 1-year and 5-year growth, replication factors.
3. **Bandwidth & Networking** (Drills 31–45): Ingress vs egress, bytes to bits/sec, NIC link saturation.
4. **Cache & Memory Sizing** (Drills 46–60): Pareto 80/20 rule, working set estimation, eviction headroom.
5. **Little's Law & Concurrency** (Drills 61–75): $L = \lambda \times W$, database connection pool sizing, worker threads.
6. **Queue Capacity & Lag** (Drills 76–85): Producer-consumer imbalance, backlog growth, catch-up time calculations.
7. **Availability & Downtime** (Drills 86–95): Calculating "nines", annual downtime seconds, serial vs parallel availability.
8. **Infrastructure Cost Modeling** (Drills 96–105): Compute instance sizing, egress bandwidth charges, storage costs.

---

## 2. Directory Structure
- `exercises.md`: The 105 problem statements without spoilers.
- `solutions.py`: Mathematical solution functions for all 105 drills.
- `test_calculations.py`: Pytest test suite asserting the mathematical correctness of each calculation.

---

## 3. Running Verification
```bash
python calculations/solutions.py
pytest calculations/test_calculations.py -v
```
