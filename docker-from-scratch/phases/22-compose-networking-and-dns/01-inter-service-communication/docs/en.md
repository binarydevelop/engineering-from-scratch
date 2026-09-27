# Lesson 22.1: Compose Networking, Service DNS, and Isolation

## Motto
"Compose assigns each service an automatic DNS alias matching its service name; never replace a service name with `localhost`."

## Problem
In a Compose file with `web`, `redis`, and `postgres`:
A developer configures their web application with `REDIS_HOST=localhost` because on their laptop they're used to everything running on `localhost`.
The application immediately crashes with `Connection refused`.
They change `REDIS_HOST=redis` and suddenly it works!
Why did `redis` work, why did `localhost` fail, and how does Docker Compose isolate frontend services from backend databases?

## Prediction
1. Why does `web` fail to connect when pointed to `localhost:6379`?
2. What network does Docker Compose create by default if you don't define a `networks:` section?
3. If a container is attached to `frontend` and Postgres is on `backend`, can the frontend container reach Postgres?

## Why this matters
Multi-tier network segmentation is essential for securing distributed systems. By placing your database on an isolated internal network that only backend services can touch, you ensure that even if an attacker achieves Remote Code Execution (RCE) on a public-facing web server, they cannot trivially access or route traffic to private storage networks.

## First principles
1. **The Automatic Project Bridge**:
   When you run `docker compose up`, if no networks are declared, Compose automatically provisions a user-defined bridge network named `<project>_default`.
2. **Automatic Service DNS Registration**:
   For every service in the Compose file, Compose automatically registers its service name (`web`, `redis`, `postgres`) as a DNS alias with Docker's embedded DNS server (`127.0.0.11`).
3. **Multi-Tier Network Topologies**:
   Services can belong to multiple networks simultaneously:
   - `web`: Attached to `frontend` (public-facing) and `backend` (private).
   - `postgres`: Attached *only* to `backend`.
   - Any container attached solely to `frontend` has zero network route or DNS resolution to `postgres`.

## Mental model

```text
MULTI-TIER COMPOSE TOPOLOGY:

              ┌──────────────────────────────────────────────┐
              │               FRONTEND NETWORK               │
              └──────────────────────┬───────────────────────┘
                                     │
                                     ▼
                      ┌──────────────────────────────┐
                      │        SERVICE: "web"        │
                      │  (Dual-Homed on both nets!)  │
                      └──────────────┬───────────────┘
                                     │
              ┌──────────────────────┴───────────────────────┐
              │               BACKEND NETWORK                │
              ├──────────────────────────────┬───────────────┤
              ▼                              ▼               │
    ┌──────────────────┐           ┌──────────────────┐      │
    │ SERVICE: "redis" │           │SERVICE:"postgres"│      │
    │ IP: 172.19.0.3   │           │ IP: 172.19.0.2   │      │
    └──────────────────┘           └──────────────────┘      │
                                                             │
  Standalone Frontend Container ──X── CANNOT REACH POSTGRES! ┘
```

## Build it
Review `docker-compose.yml` and `test_connections.py` in `code/`.
Notice:
- `web` is dual-homed on `frontend` and `backend`.
- `redis` and `postgres` are strictly isolated on `backend`.

## Run it
Execute the experiment runner:

```bash
./phases/22-compose-networking-and-dns/01-inter-service-communication/experiments/run_experiment.sh
```

## Inspect it
1. Observe Step 2: `web` connects to `redis:6379` and `postgres:5432` by service name.
2. Observe Step 3 (Mandatory Experiment): Running `test_connections.py localhost 6379` inside `web` fails with `[Errno 111] Connection refused`!
3. Observe Step 4: A container attached only to `frontend` fails to resolve or connect to `postgres`.

## Break it
Edit `docker-compose.yml` and remove `backend` from `web.networks`.
Run `docker compose up -d`.
Now test connecting from `web` to `redis`:
It immediately fails with `getaddrinfo failed`! Because `web` is no longer on the same network bridge as Redis, embedded DNS refuses to resolve the name.

## Debug it
When a service cannot resolve another service name:
1. Run `docker compose exec <src> ping <target-service>`.
2. Inspect network memberships:
   ```bash
   docker network inspect <project>_<network>
   ```
   Verify that both containers appear under the `Containers` object.
3. If they are on different networks, add the missing network to `services.<name>.networks` in `compose.yaml`.

## Modify it
Add a custom container name to the redis service:
```yaml
container_name: my-custom-cache
```
Re-run `docker compose up -d`. Verify whether `web` can reach it by its service name `redis`, its container name `my-custom-cache`, or both!

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Output confirming TCP connection to `redis:6379` and `postgres:5432`.
- Output demonstrating the failure of `localhost:6379`.
- Verification of multi-tier network isolation.

## Questions for mastery
1. Why does Compose provide service discovery by service name rather than requiring you to specify container names?
2. If two services have multiple replicas (`deploy.replicas: 3`), how does Compose DNS resolve the service name? (Hint: DNS round-robin).
3. Under what circumstances should a backend database publish ports to the host in a Compose setup?

## What comes next
We mastered Compose networking. Now: **How does Docker Compose manage persistent storage, and what is the difference between `docker compose down` and `docker compose down -v`?** Proceed to **Phase 23: Compose Volumes and Persistent State**.
