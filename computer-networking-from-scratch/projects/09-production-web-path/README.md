# Project 09: Production Web Path & Full-Stack Incident Tracer

> **Motto**: A single HTTP request traverses DNS resolvers, edge firewalls, reverse proxy terminators, load balancer schedulers, application processes, and database connection pools; a true network engineer traces each boundary without guessing.

---

## 1. Overview
In this capstone integration project, you simulate and trace an end-to-end multi-tier microservice architecture:
`Client` -> `DNS` -> `Edge Reverse Proxy` -> `Load Balancer` -> `App Workers` -> `Datastore`

## 2. Integrated Architecture
```text
Client (curl)
  │
  ├─ 1. DNS Resolution: Query api.company.internal -> 10.0.0.100
  │
  ├─ 2. TCP Handshake: Connect to Edge Reverse Proxy :80
  │
  ├─ 3. Load Balancing: Steer request to healthy worker (app-worker-1 or app-worker-2)
  │
  ├─ 4. Application Processing: App worker queries Datastore
  │
  └─ 5. Response Pipeline: JSON payload streamed back up the reverse proxy chain
```

## 3. Failure Scenarios Simulated
1. **DNS Failure**: Authoritative zone missing domain -> `NXDOMAIN` (HTTP request never even leaves client socket!).
2. **Worker Crash**: Application process crashes -> Load balancer detects `TCP Connection Refused` and fails over to surviving worker.
3. **Database Timeout**: Datastore hangs -> Worker returns `HTTP 504 Gateway Timeout`.

## 4. Running & Testing
```bash
python3 production_topology.py
python3 test_production_path.py
```
