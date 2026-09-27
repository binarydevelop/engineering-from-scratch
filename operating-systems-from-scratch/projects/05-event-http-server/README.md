# Capstone 5: High-Performance HTTP Server

> **Motto:** Concurrency is not about running many threads; it is about keeping CPU cores saturated while waiting on asynchronous I/O readiness.

---

## 1. Architectural Comparison

This capstone implements and benchmarks three classic web server concurrency architectures:

```text
1. Sequential (Blocking):
   Client 1 ──► [ Accept ] ──► [ Read ] ──► [ Write ] ──► [ Close ]
   Client 2 ──► [ WAITING IN KERNEL LISTEN QUEUE UNTIL CLIENT 1 FINISHES ]

2. Multi-Threaded Worker Pool:
   Listening Thread ──► [ Accept ] ──► [ Bounded Work Queue ]
                                              ├── Worker 1 ──► [ Read / Write ]
                                              ├── Worker 2 ──► [ Read / Write ]
                                              └── Worker 3 ──► [ Read / Write ]

3. Non-Blocking Event-Driven (select / poll / epoll):
   Single Thread ──► [ select() / epoll_wait() ]
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
      [ Listening Socket Ready ]   [ Client Socket Has Data ]
             accept()                     read() & write()
```

---

## 2. Compiling and Running

```bash
make
```

### Run Mode 1: Sequential Blocking
```bash
./http-server --seq 8080
```

### Run Mode 2: Multi-Threaded Worker Pool
```bash
./http-server --pool 8080
```

### Run Mode 3: Non-Blocking Event Loop
```bash
./http-server --event 8080
```

---

## 3. Benchmarking

In a second terminal, execute the benchmark suite:
```bash
python3 benchmark_client.py 8080
```
