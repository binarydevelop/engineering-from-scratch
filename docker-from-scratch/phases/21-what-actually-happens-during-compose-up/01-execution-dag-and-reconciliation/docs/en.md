# Lesson 21.1: What Actually Happens During `docker compose up`

## Motto
"Compose does not boot a cluster; it executes an ordered series of HTTP REST calls against `/v1.xx` on the Docker daemon."

## Problem
Many engineers treat `docker compose up` as an indivisible magic incantation.
When a compose command hangs or fails halfway through, they run `docker compose down -v` and try again without understanding:
- Which resources were already committed to disk?
- Why did the API container start before the database was ready?
- How did variables like `${API_PORT}` get resolved?
We must trace the exact sequence of events that occurs between typing `docker compose up` and your services serving traffic.

## Prediction
1. What is created first: containers, networks, or volumes?
2. If service B specifies `depends_on: [service A]`, does Compose wait for service A's process to start or for service A to become healthy?
3. How does Docker Compose communicate with Docker Engine during `up`?

## Why this matters
Knowing the reconciliation sequence of `docker compose up` allows you to diagnose race conditions, resolve state reconciliation deadlocks, write bulletproof orchestration dependencies, and understand how modern Kubernetes controllers operate.

## First principles
The complete chronological execution pipeline of `docker compose up`:

```text
1. CLI Keystroke: $ docker compose up -d
     │
2. Configuration Compilation:
     ├── Reads compose.yaml / docker-compose.yml
     ├── Reads .env and merges host shell environment
     └── Resolves interpolation: ${API_PORT} -> 8095
     │
3. Dependency Graph Resolution (DAG):
     └── Builds execution tree based on depends_on and network links
     │
4. State Reconciliation (HTTP calls to /var/run/docker.sock):
     ├── Step 4a: Queries existing engine state (GET /networks, GET /containers)
     ├── Step 4b: POST /volumes/create (Creates dfs-trace-project_pg-storage)
     ├── Step 4c: POST /networks/create (Creates dfs-trace-project_backend)
     │
5. Ordered Container Provisioning:
     ├── Step 5a: POST /containers/create (Instantiates database container)
     ├── Step 5b: POST /networks/<id>/connect (Plugs database into backend)
     ├── Step 5c: POST /containers/<id>/start (Launches database PID 1)
     │
6. Health Condition Gate:
     ├── Periodic probes: POST /containers/<id>/exec (pg_isready)
     └── Blocks dependent services until: health_status == healthy!
     │
7. Dependent Container Launch:
     ├── Step 7a: POST /containers/create (Instantiates api container)
     ├── Step 7b: POST /networks/<id>/connect (Plugs api into backend)
     ├── Step 7c: POST /containers/<id>/start (Launches api PID 1)
     └── Port Forwarding: Binds 0.0.0.0:8095 -> 80/tcp via NAT
```

## Mental model

```text
DOCKER COMPOSE CLI (DAG Resolver)
┌────────────────────────────────────────────────────────┐
│  Parsed Graph: [pg-storage] & [backend-net]            │
│                       │                                │
│                       ▼                                │
│               [database: healthy]                      │
│                       │                                │
│                       ▼                                │
│                     [api]                              │
└───────────────────────┬────────────────────────────────┘
                        │ Synchronous HTTP REST API Calls
                        ▼
DOCKER ENGINE DAEMON (/var/run/docker.sock)
┌────────────────────────────────────────────────────────┐
│  1. EVENT: volume create -> pg-storage                 │
│  2. EVENT: network create -> backend                   │
│  3. EVENT: container create -> database                │
│  4. EVENT: container start -> database                 │
│  5. EVENT: health_status: healthy                      │
│  6. EVENT: container create -> api                     │
│  7. EVENT: container start -> api                      │
└────────────────────────────────────────────────────────┘
```

## Build it
Review `compose.yaml` and `.env` in `code/`.
Notice:
- Variable interpolation `${API_PORT:-8090}` and `${PG_TAG:-16-alpine}`.
- Explicit health dependency: `condition: service_healthy`.

## Run it
Execute the experiment runner:

```bash
./phases/21-what-actually-happens-during-compose-up/01-execution-dag-and-reconciliation/experiments/run_experiment.sh
```

## Inspect it
1. Observe Step 1: `docker compose config` resolves variables into concrete values (`image: postgres:16-alpine`, `8095:80`).
2. Examine Step 4: The real-time daemon event stream captures the exact chronological order of events.
3. Observe how the `api` container was held in `Waiting` state until `database` emitted `action=health_status: healthy`!

## Break it
Break the health check in `compose.yaml` by setting the test command to `["CMD-SHELL", "exit 1"]`.
Run `docker compose up`:
Notice that `database` starts, but Compose refuses to start `api`! It times out waiting for the database to become healthy.
This proves that Compose enforces application-level readiness gates.

## Debug it
When `docker compose up` hangs or behaves unexpectedly:
1. Preview the compiled DAG and variables:
   ```bash
   docker compose config
   ```
2. Trace live daemon events in a separate terminal:
   ```bash
   docker events --filter "label=com.docker.compose.project"
   ```
3. Inspect container dependency states:
   ```bash
   docker compose ps
   ```

## Modify it
Add a third service `worker` that depends on `api`. Run the tracer and observe where `worker` appears in the event log.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The compiled configuration from `docker compose config`.
- The captured event trace showing network, volume, container creation, and health check gate.
- The verified status of the running containers.

## Questions for mastery
1. Why does Compose create networks and volumes before creating containers?
2. What is the difference between `depends_on: [database]` and `depends_on: { database: { condition: service_healthy } }`?
3. What is idempotence in `docker compose up`? If you run `docker compose up -d` twice without changing anything, what happens?

## What comes next
We saw Compose wire services together. Now we inspect the network under Compose: **Why do services reach each other by service name, and how are multi-tier networks isolated?** Proceed to **Phase 22: Compose Networking and DNS**.
