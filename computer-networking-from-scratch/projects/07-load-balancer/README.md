# Project 07: Layer-7 Load Balancer With Adaptive Steering

> **Motto**: A naive round-robin load balancer treats all requests and servers as equal; an adaptive load balancer tracks concurrency and latency to route traffic away from degradations.

---

## 1. Overview
In this project, you construct an L7 load balancer that implements:
1. **Round-Robin**: Standard sequential round-robin distribution.
2. **Least-Connections**: Directs traffic to the server currently processing the fewest active in-flight requests.
3. **IP Hash**: Consistently hashes the client IPv4 address to the same backend node (session affinity).

## 2. Dynamic Algorithmic Steering
```text
                          [ Load Balancer ]
                                 │
           ┌─────────────────────┴─────────────────────┐
           ▼                                           ▼
      Backend A                                   Backend B
  Active Requests: 8                          Active Requests: 1
  (Slow database query)                       (Idle & healthy)
           │                                           ▲
           └───────── Least-Connections ───────────────┘
                     Steers traffic to B!
```

## 3. Running & Testing
```bash
python3 load_balancer.py ROUND_ROBIN 8080
python3 load_balancer.py LEAST_CONNECTIONS 8080
python3 test_lb.py
```
