# Lesson 20.1: Docker Compose From First Principles

## Motto
"Docker Compose is not a container runtime; it is a declarative DAG compiler that makes API calls to the Docker daemon."

## Problem
In earlier lessons, whenever we needed two or three containers to communicate, we had to:
1. Manually run `docker network create`.
2. Manually run `docker volume create`.
3. Run `docker run -d --network ... -v ... -e ...` for container 1.
4. Run another long command for container 2.
5. Remember to start dependencies in the correct order.
6. Write custom shell scripts to stop and delete them in reverse order.
As systems grow to 5, 10, or 20 microservices, manual `docker run` scripts become unmaintainable spaghetti that easily drift out of sync.
How do we declare an entire multi-service topology in a single, version-controlled file?

## Prediction
1. Does `docker compose` introduce a new daemon or kernel runtime to your machine?
2. How does a directive in Compose like `services.db.image: postgres:16-alpine` translate into Docker primitives?
3. If you run `docker compose up`, does Compose create containers in parallel or in a dependency order?

## Why this matters
Docker Compose is the universal lingua franca for local multi-service development, integration testing, and CI environments. Misunderstanding Compose leads to treating it as an opaque black box, causing confusion over project naming prefixes, network aliases, and volume persistence.

## First principles
1. **The Orchestration Layer**:
   ```text
   docker-compose.yml (Declarative YAML Topology)
            │
            ▼
   docker compose CLI (Parses YAML, calculates dependency Directed Acyclic Graph)
            │
            │ Sequential REST API Calls (/networks, /volumes, /containers)
            ▼
   Docker Daemon Engine (dockerd)
            │
            ▼
   containerd -> runc -> Linux Kernel
   ```
2. **The 1:1 Primitive Mapping**:
   Every Compose YAML key maps directly to a Docker CLI flag and Engine API parameter:
   - `services.<name>.image` ──► `docker run <image>`
   - `services.<name>.ports` ──► `docker run -p <host>:<container>`
   - `services.<name>.environment` ──► `docker run -e <key>=<val>`
   - `services.<name>.volumes` ──► `docker run -v <vol>:<path>`
   - `services.<name>.networks` ──► `docker run --network <net>`
   - `networks:` top-level ──► `docker network create`
   - `volumes:` top-level ──► `docker volume create`
3. **Project Namespace Prefixing**:
   To prevent naming collisions between different projects, Compose automatically prefixes resources with the directory name (e.g. `code_app-net`, `code-web-1`).

## Mental model

```text
DECLARATIVE SPECIFICATION (docker-compose.yml):
┌────────────────────────────────────────────────────────┐
│  services:                                             │
│    web:                                                │
│      image: alpine                                     │
│      depends_on: [db, cache]                           │
│    db:                                                 │
│      image: postgres:16-alpine                         │
│    cache:                                              │
│      image: redis:7-alpine                             │
└──────────────────────────┬─────────────────────────────┘
                           │
                           │ docker compose up
                           ▼
DIRECTED ACYCLIC GRAPH (DAG) RESOLUTION:
Step 1: Create Networks & Volumes (code_app-net, code_db-data)
Step 2: Create & Start Dependencies (code-db-1, code-cache-1)
Step 3: Create & Start Dependents (code-web-1)
```

## Build it
Review `manual_deploy.sh` and `docker-compose.yml` in `code/`.
Notice how the 35-line procedural bash script compresses into clean, declarative YAML.

## Run it
Execute the experiment runner:

```bash
./phases/20-docker-compose-from-first-principles/01-manual-orchestration-to-spec/experiments/run_experiment.sh
```

## Inspect it
1. Observe Part 1: All 5 manual commands required to establish the network, volume, DB, cache, and web containers.
2. Observe Part 2: `docker compose up -d` executes the exact same steps automatically.
3. Verify that `code-web-1` can ping `cache` and `db` directly using service names!

## Break it
Add a circular dependency in `docker-compose.yml`:
Make `web` depend on `db`, and `db` depend on `web`.
Run `docker compose up`:
Compose detects the cycle immediately and aborts:
`dependency cycle detected: db -> web -> db`
This proves that Compose compiles your topology into a mathematical Directed Acyclic Graph (DAG) before executing any actions.

## Debug it
When `docker compose up` fails:
1. Validate syntax: `docker compose config`.
   This parses and validates the YAML file, expands environment variables, and prints the resolved canonical specification without starting containers.
2. Check which containers failed: `docker compose ps -a`.
3. Check logs of a specific service: `docker compose logs <service-name>`.

## Modify it
Add a restart policy to the database service in `docker-compose.yml`:
```yaml
restart: unless-stopped
```
Run `docker compose config` and verify that Compose accepts the configuration.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Comparison between manual script output and Compose up output.
- Verification of service name DNS resolution (`ping cache`, `ping db`).
- The output of `docker compose ps`.

## Questions for mastery
1. Why is Docker Compose considered client-side orchestration rather than server-side clustering?
2. How does Compose determine the prefix for container and network names?
3. What is the difference between `docker compose stop` and `docker compose down`?

## What comes next
We saw Compose create networks, volumes, and containers. Now: **What is the exact millisecond-by-millisecond execution sequence when you run `docker compose up`?** Proceed to **Phase 21: What Actually Happens During docker compose up**.
