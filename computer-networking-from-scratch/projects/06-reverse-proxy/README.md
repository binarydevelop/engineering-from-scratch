# Project 06: HTTP Reverse Proxy & Active Health Prober

> **Motto**: A reverse proxy decouples external clients from internal service topology, providing TLS termination, header injection, request routing, and failover resilience.

---

## 1. Overview
In this project, you build an HTTP reverse proxy that balances traffic across backend servers, enriches requests with client metadata (`X-Forwarded-For`), and runs active background health checks to prune failing backends.

## 2. Request Architecture
```text
Client ──► [ Reverse Proxy :8000 ] ──► Round-Robin Pool
                                         ├─ Backend 1 (:8081) [Healthy]
                                         └─ Backend 2 (:8082) [Healthy]
```

## 3. Running & Testing
```bash
python3 reverse_proxy.py 8000
python3 test_proxy.py
```
