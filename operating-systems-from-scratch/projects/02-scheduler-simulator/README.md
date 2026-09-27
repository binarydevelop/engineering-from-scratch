# Capstone 2: User-Space Thread & Process Scheduler Simulator

> **Motto:** The scheduler makes the impossible possible: giving the illusion of infinite processors while optimizing fairness, turnaround, and interactive latency.

---

## 1. Architectural Overview

This capstone implements an end-to-end process scheduler simulator in Python:
* **Multi-Level Feedback Queue (MLFQ):**
  * Multiple priority levels (Queue 0: $Q=2$, Queue 1: $Q=4$, Queue 2: $Q=8$).
  * Interactive jobs stay at high priority; CPU-intensive jobs are progressively demoted.
  * Starvation prevention: Periodic priority boost restores all tasks to Queue 0.
* **Gantt Chart Visualization:** Visual text-based timeline of CPU occupancy.
* **Metrics Engine:**
  * Turnaround Time: $T_{\text{turnaround}} = T_{\text{completion}} - T_{\text{arrival}}$
  * Waiting Time: $T_{\text{waiting}} = T_{\text{turnaround}} - T_{\text{burst}}$
  * Response Time: $T_{\text{response}} = T_{\text{first\_run}} - T_{\text{arrival}}$

---

## 2. Usage

```bash
python3 scheduler_sim.py
```
