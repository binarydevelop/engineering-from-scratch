# Phase 00: Production Laboratory

> **Motto**: The production system is not an abstract cloud; it is operating system processes, network sockets, kernel buffers, and state stores that can be directly inspected.

---

## Motto
"The production system is not an abstract cloud; it is operating system processes, network sockets, kernel buffers, and state stores that can be directly inspected."

## Production Problem
Engineers frequently attempt to debug outages by staring at high-level SaaS dashboards without knowing how to inspect the underlying OS process, TCP listen queues, file descriptors, or database connections. When the dashboard agent itself crashes or network drops occur, the engineer is completely blinded.

## Prediction
Running the baseline lab stack (`client` -> `API` -> `PostgreSQL`) via Docker Compose will reveal active TCP listening sockets, memory allocations, and connection pool states directly via standard Linux inspection tools.

## User Impact
If you cannot inspect the raw process and network layer, transient socket timeouts or half-open connections will look like mysterious, unreproducible bugs, leaving users with hanging requests and delayed checkouts.

## Why This Matters
All high-level observability frameworks (OpenTelemetry, Prometheus, Grafana) are abstractions built on top of operating system primitives. To debug when the telemetry pipeline itself fails, you must understand the substrate beneath it.

## First Principles
A web service is fundamentally an operating system process holding an open file descriptor bound to a network socket via the BSD socket API (`socket()`, `bind()`, `listen()`, `accept()`). Concurrency is bounded by operating system thread pools, file descriptor rlimits (`ulimit -n`), and TCP listen backlog queues (`somaxconn`).

## Mental Model
```text
Client Request
      │
      ▼
OS Network Interface (eth0 / lo)
      │
      ▼
TCP Socket Listen Backlog (somaxconn)
      │
      ▼
Python / Uvicorn Process (PID 1042)
      │
      ├── Open File Descriptors (Sockets, Logs)
      ├── Memory Pages (RSS / Heap)
      │
      ▼
Database Connection Pool (PostgreSQL Socket :5432)
```

## Build the Simple Version
In this foundational phase, observe the minimal stack using Docker Compose without any telemetry agents or third-party monitoring stacks:
```bash
# Start the baseline laboratory
make start-lab
```

## Instrument It
Before installing OpenTelemetry or Prometheus, inspect the running processes and sockets directly from the host terminal:
```bash
# 1. View running container processes
docker compose ps

# 2. Inspect active network listening sockets inside container
docker compose exec api-gateway netstat -tlpn 2>/dev/null || docker compose exec api-gateway ss -tlpn

# 3. Inspect open file descriptors
docker compose exec api-gateway ls -l /proc/1/fd
```

## Observe It
Generate a single manual request and observe the standard output:
```bash
curl -i http://localhost:8000/healthz
```
Expected output:
```http
HTTP/1.1 200 OK
content-length: 37
content-type: application/json

{"status":"alive","service":"api-gateway"}
```

## Measure It
Measure the baseline CPU and Memory consumption of the cold processes:
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
```

## Break It
Terminate the backend database without stopping the API Gateway:
```bash
docker compose stop postgres
```

## Detect It
Execute a checkout request through the gateway:
```bash
curl -i -X POST http://localhost:8000/api/v1/checkout \
  -H "Content-Type: application/json" \
  -d '{"user_id":"u1","items":[{"product_id":"item_101","quantity":1,"unit_price":20.0}],"payment_token":"tok","total_amount":20.0}'
```
Observe the failure:
```http
HTTP/1.1 502 Bad Gateway
content-type: application/json

{"error":"Bad Gateway calling checkout-service"}
```

## Debug It
Inspect the container logs to find the exact TCP connection refusal:
```bash
docker compose logs --tail=20 checkout-service
```
You will observe: `psycopg2.OperationalError: could not connect to server: Connection refused`.

## Mitigate It
Restart the database container:
```bash
docker compose start postgres
```

## Recover It
Verify that database connections recover and subsequent requests succeed with HTTP 200.

## Automate It
Automate this verification using `scripts/check-environment.sh` and `make health-check`.

## Reliability Implication
Services must handle dependency connection drops gracefully without crashing the main process event loop.

## Platform Implication
The platform must provide automated container restart policies (`restart: unless-stopped`) and readiness probes so that traffic is not routed to instances before database handshakes are complete.

## Evidence
Record your raw terminal outputs, process IDs, and memory stats in `outputs/phase-00-evidence.md`.

## Questions for Mastery
1. What is the difference between a process listening on `0.0.0.0:8000` versus `127.0.0.1:8000` inside a container?
2. If `ulimit -n` is set to 1024, what happens when concurrent HTTP connections reach 1050?
3. Why does the API Gateway return HTTP 502 instead of HTTP 500 when downstream services are unreachable?

## When Not to Use This
Do not attempt to operate production environments with manual `docker stats` inspection; this phase exists to ground your mental model in raw operating system reality before we build automated telemetry pipelines.

## What Comes Next
In **Phase 01: What Does Production Mean?**, we define the operational differences between code running in development versus systems handling real customer traffic and financial state.
