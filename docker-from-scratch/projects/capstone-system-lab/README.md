# Capstone System Design Lab

A production-grade, multi-service architecture deconstructing how containerized backends, persistence stores, message brokers, and telemetry systems interconnect through Docker primitives.

```
       [Host Browser: localhost:3000]
                      |
                      v
             +-----------------+
             |     Grafana     |
             +--------+--------+
                      | (PromQL)
                      v
             +-----------------+
             |   Prometheus    |
             +--------+--------+
                      | (Scrape /metrics)
                      v
[Host: :8000] ----> [   Python App    ] (frontend-tier & backend-tier)
                         |   |   |
          +--------------+   |   +--------------+
          |                  |                  |
          v                  v                  v
+------------------+ +---------------+ +------------------+
|    PostgreSQL    | |     Redis     | |       NATS       |
| (postgres_data)  | | (redis_data)  | | (Event / PubSub) |
+------------------+ +---------------+ +------------------+
```

## System Components

| Service | Technology | Port (Internal) | Port (Host) | Network Tier | Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`app`** | Python 3.11 | `8000` | `8000` | `frontend-tier`, `backend-tier` | Core business logic, health aggregation, `/metrics` |
| **`postgres`** | PostgreSQL 16 Alpine | `5432` | None | `backend-tier` | Relational storage with durable named volume (`postgres_data`) |
| **`redis`** | Redis 7 Alpine | `6379` | None | `backend-tier` | In-memory key-value cache and session store (`redis_data`) |
| **`nats`** | NATS 2.10 Alpine | `4222`, `8222` | None | `backend-tier` | High-throughput pub/sub messaging engine |
| **`prometheus`** | Prometheus v2.51.0 | `9090` | `9090` | `frontend-tier` | Time-series metrics scraper pulling `/metrics` |
| **`grafana`** | Grafana 10.4.0 | `3000` | `3000` | `frontend-tier` | Visual observability dashboards for telemetry |

## Network Segmentation Architecture

* **`frontend-tier`**: Contains `app`, `prometheus`, and `grafana`. Telemetry collectors can scrape the application and users can access visualization interfaces, but Prometheus and Grafana have zero route to internal databases.
* **`backend-tier`**: Contains `app`, `postgres`, `redis`, and `nats`. Storage engines and brokers communicate with `app` in complete isolation from the external telemetry network.

## Quickstart

```bash
# Start the entire system in the background
docker compose up -d

# Check live health states
curl http://localhost:8000/health

# Scrape raw telemetry metrics
curl http://localhost:8000/metrics

# Open Grafana
open http://localhost:3000  # Default credentials: admin / admin
```
