# Lesson: Progressive Rebuilding of the Multi-Service Capstone Architecture

## Motto
"Orchestration without first principles is fragility; build the system piece by piece from the raw process up to declarative Compose."

## Problem
Engineers frequently inherit complex `docker-compose.yml` or Kubernetes manifests running multi-tier applications (web APIs, relational databases, caching layers, message brokers, and telemetry stacks). When the system fails during boot or under degraded network conditions, engineers treat the entire stack as an indivisible, opaque monolith. Without understanding how each service connects to the host, how filesystems are mounted, and how DNS queries route across bridge networks, debugging becomes trial-and-error guesswork.

## Prediction
By deconstructing the entire system design lab into 14 progressive steps—starting with a raw host process, containerizing it, manually adding Redis, wiring custom bridge networks, attaching PostgreSQL with persistent volumes, integrating NATS pub/sub, layering Prometheus and Grafana telemetry, and finally consolidating into declarative Docker Compose with health gating—every layer of the Docker abstraction becomes transparent and predictable.

## Why this matters
A real-world production system is not just one web server. It is a distributed network of cooperating stateful and stateless processes. Mastering Docker means understanding how state persistence, cross-container DNS, port isolation, security hardening, and health reconciliation interact across diverse technologies (Python, PostgreSQL, Redis, NATS, Prometheus, Grafana).

## First principles
1. **Separation of Concerns across Virtual Bridges:**
   - Database and cache instances should never expose ports directly to the host unless explicitly necessary for debugging.
   - Dual-homed containers (like our `app`) bridge the gap between ingress/telemetry tiers (`frontend-tier`) and internal data stores (`backend-tier`).
2. **Persistence vs Ephemerality:**
   - Containers are disposable execution units. Stateful engines (Postgres, Redis, Prometheus) must mount named volumes to ensure data survives container death, rebuilds, and updates.
3. **Application Protocol Readiness vs Process Spawn:**
   - Orchestration platforms must distinguish between process creation and service readiness. Declarative healthchecks (`pg_isready`, `redis-cli ping`) prevent dependency race conditions.
4. **Telemetry and Metric Pull Semantics:**
   - Prometheus uses internal DNS to pull metrics periodically from `/metrics` endpoints. The target container does not need to know where Prometheus lives—it only exposes a standard HTTP interface.

## Mental model
```
                    [Host Ingress: localhost:3000]
                                  |
                                  v
                      +-----------------------+
                      |        Grafana        |
                      +-----------+-----------+
                                  | (PromQL Queries)
                                  v
                      +-----------------------+
                      |      Prometheus       |
                      +-----------+-----------+
                                  | (Scrapes /metrics)
                                  v
[Host: :8000] ------> +-----------------------+
                      |      Python App       |
                      +---+-------+-------+---+
                          |       |       |
            +-------------+       |       +-------------+
            | (TCP 5432)          | (TCP 6379)          | (TCP 4222)
            v                     v                     v
+-----------------------+ +---------------+ +-----------------------+
|      PostgreSQL       | |     Redis     | |         NATS          |
|    (postgres_data)    | | (redis_data)  | |      (Pub / Sub)      |
+-----------------------+ +---------------+ +-----------------------+
```

## Build it
The complete project workspace is located in `projects/capstone-system-lab/`:
1. `app/app.py`: A Python service handling HTTP routing, readiness probes across all backends, and Prometheus metrics generation.
2. `app/Dockerfile`: A hardened container image running as a non-root user (UID 10001) with built-in health probes.
3. `monitoring/prometheus/prometheus.yml`: Metric scraping configuration targeting `app:8000`.
4. `monitoring/grafana/`: Datasource and dashboard provisioning files.
5. `docker-compose.yml`: Multi-service Compose specification orchestrating all 6 components.
6. `phases/29-rebuild-the-system-design-lab/01-progressive-capstone/code/run_progressive_steps.sh`: The 14-step automation driver.

## Run it
Execute the entire 14-step progressive rebuild:
```bash
./phases/29-rebuild-the-system-design-lab/01-progressive-capstone/experiments/run_experiment.sh
```

## Inspect it
Inspect the live multi-tier network topology:
```bash
docker network inspect projects_backend-tier
docker network inspect projects_frontend-tier
```
Notice that `app` has an IP on both networks, whereas `postgres` only exists on `backend-tier` and `grafana` only exists on `frontend-tier`.

## Break it
Simulate a backend dependency crash while the application is live:
```bash
docker compose -f projects/capstone-system-lab/docker-compose.yml stop redis
curl -i http://localhost:8000/health
```
Observe that the application immediately reports `503 Service Unavailable` with `"redis": {"status": "down"}` without crashing.

## Debug it
Apply the systematic triage protocol:
1. `docker compose ps`: Redis shows as `Exited (0)`.
2. Inspect application logs: `docker compose logs app`.
3. Restart the failed service: `docker compose start redis`.
4. Poll `curl http://localhost:8000/health` until status returns to `200 OK`.

## Modify it
Add a synthetic write endpoint `/api/record` to `app/app.py` that inserts an entry into a PostgreSQL table and invalidates a cache key in Redis. Verify data persistence across `docker compose restart postgres`.

## Evidence
Running `run_experiment.sh` traces all 14 progressive milestones:
```
[Step 1/14] Running app directly on host...
[+] Step 1 SUCCESS: App is running directly on host (PID: 12345).
[Step 2/14] Containerizing app with Dockerfile...
[+] Step 2 SUCCESS: Built image 'capstone-app:v1'.
[Step 3/14] Adding Redis manually via docker run...
[+] Step 3 SUCCESS: Redis container started.
[Step 4/14] Creating user-defined bridge network 'capstone-manual-net'...
[+] Step 4 SUCCESS: Network created.
[Step 5/14] Connecting Redis to network and running app container...
[+] Step 5 SUCCESS: Containerized app resolved and communicated with Redis!
[Step 6/14] Adding PostgreSQL manually on capstone-manual-net...
[+] Step 6 SUCCESS: Postgres container started.
[Step 7/14] Creating persistent named volume for Postgres...
[+] Step 7 SUCCESS: Created named volume 'capstone-step-pgdata'.
[Step 8/14] Adding NATS message broker on capstone-manual-net...
[+] Step 8 SUCCESS: NATS container started.
[Step 9/14] Adding Prometheus metrics collector...
[+] Step 9 SUCCESS: Prometheus container started.
[Step 10/14] Adding Grafana visualization engine...
[+] Step 10 SUCCESS: All 6 components running manually!
[Step 11/14] Transitioning to Docker Compose specification...
[+] Step 11 SUCCESS: Stack launched declaratively via Docker Compose.
[Step 12/14] Verifying health checks and dependency gating...
[+] Both postgres and redis are HEALTHY!
[Step 13/14] Intentionally breaking dependencies (stopping Redis)...
[+] Step 13 CONFIRMED: Dependency failure cleanly detected.
[Step 14/14] Debugging and restoring the failed service...
[+] Step 14 SUCCESS: System automatically reconciled and returned to healthy state!
```

## Questions for mastery
1. Why does running Prometheus in a separate network tier increase database security?
2. If the PostgreSQL container is recreated (`docker compose up --force-recreate db`), why is no data lost?
3. How does Docker's internal DNS allow Prometheus to find `app:8000` without static IP addresses?

## What comes next
In Phase 30, we assemble the complete, unbroken end-to-end mental model: tracing a single `docker compose up` command all the way down to kernel namespaces, cgroups, veth pairs, iptables, and storage snapshotters.
