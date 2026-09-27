# Capstone 3: Production-Like Resilient Kafka Laboratory

A full 3-node KRaft Apache Kafka cluster with automated chaos injection, leader failover measurement, and In-Sync Replica (ISR) tracking.

---

## 1. Cluster Topology

* **Broker 1:** `localhost:9092` (Controller voter 1)
* **Broker 2:** `localhost:9094` (Controller voter 2)
* **Broker 3:** `localhost:9096` (Controller voter 3)
* **Quorum:** KRaft native Raft metadata log (`@metadata-0`)
* **Default Topic Settings:** `replication.factor=3`, `min.insync.replicas=2`

---

## 2. Launching the Lab

```bash
make up-cluster
```

## 3. Running Chaos Verification

```bash
python3 projects/capstone-3-production-lab/chaos_runner.py
```
