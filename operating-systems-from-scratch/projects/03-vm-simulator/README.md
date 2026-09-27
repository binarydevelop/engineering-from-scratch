# Capstone 3: Virtual Memory & Page Eviction Simulator

> **Motto:** Virtual memory is the greatest illusion in computer science: making programs believe they have contiguous, exclusive, infinite RAM while physical memory is fragmented, shared, and backed by disk.

---

## 1. Architectural Overview

* **Two-Level Address Translation:** Deconstructs Virtual Addresses into Virtual Page Numbers (VPN) and byte offsets.
* **Translation Lookaside Buffer (TLB):** Fast-path cache avoiding full page table traversals.
* **Demand Paging:** Lazy loading of physical frames upon first access exception.
* **Clock Eviction Algorithm (Second Chance):** Practical $O(1)$ approximation of Least Recently Used (LRU).
* **Dirty Page Writeback:** Tracks page mutations (`is_write`) and persists modified pages to backing storage before discarding physical frames.

---

## 2. Running the Simulation

```bash
python3 vm_sim.py
```
