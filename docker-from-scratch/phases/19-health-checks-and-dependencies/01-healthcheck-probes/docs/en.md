# Lesson 19.1: Health Checks and Dependencies

## Motto
"`process == running` does not mean `service == ready`; health checks tell load balancers and orchestrators whether your app can actually serve traffic."

## Problem
A backend service connects to PostgreSQL, loads ML embeddings into memory, and verifies database migrations during boot.
This startup sequence takes 15 seconds.
During those 15 seconds:
- The container process is alive and visible in `docker ps`.
- A reverse proxy or Kubernetes ingress sees the container as `running` and immediately routes user HTTP requests to it.
- Every single user request fails with `502 Bad Gateway` or `Connection refused`.
Conversely, if an active worker thread deadlocks or crashes while the main process stays alive, the container remains `Up` indefinitely while silently dropping jobs.
How does Docker distinguish between a process that merely exists and a service that is genuinely healthy?

## Prediction
1. What are the three possible health states of a container in Docker?
2. If a health check probe fails 3 times, does Docker automatically restart the container by default?
3. What is the purpose of `--start-period`?

## Why this matters
Zero-downtime rolling updates and automated failover depend entirely on health probes. If you don't define health checks, orchestrators will route live traffic to uninitialized containers, causing intermittent 502/503 errors during every deployment.

## First principles
1. **The Three Tiers of Health**:
   - **Process Health**: Is PID 1 alive in the process table? (Managed by kernel/Docker daemon).
   - **Application Health**: Is the application responsive, unblocked, and ready to serve HTTP/RPC traffic? (Probed by `HEALTHCHECK`).
   - **Dependency Health**: Are external databases, Redis caches, and message brokers reachable?
2. **The `HEALTHCHECK` Directive**:
   Executes a command *inside* the container periodically:
   ```dockerfile
   HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
       CMD curl -f http://localhost:8080/healthz || exit 1
   ```
   - Exit code `0`: Probe succeeded -> `healthy`.
   - Exit code `1`: Probe failed -> increments failure counter. If counter >= `retries`, status becomes `unhealthy`.
3. **The State Machine**:
   ```text
   [Container Starts] ──► [Health: starting] (Within start-period)
                               │
               ┌───────────────┴───────────────┐
               │ Probe returns 0               │ Retries exhausted
               ▼                               ▼
       [Health: healthy]              [Health: unhealthy]
   ```

## Mental model

```text
ORCHESTRATOR / DOCKER ENGINE
┌────────────────────────────────────────────────────────┐
│  Periodic Probe Execution (Every 2s via execve)        │
│       │                                                │
│       ▼                                                │
│  CONTAINER NAMESPACE: "dfs-hc-test"                    │
│  ┌──────────────────────────────────────────────────┐  │
│  │ HTTP Request: GET /healthz (Urllib / curl)       │  │
│  │                                                  │  │
│  │ Response: 200 OK  ──► Returncode 0  (HEALTHY)    │  │
│  │ Response: 500 ERR ──► Returncode 1  (UNHEALTHY)  │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

## Build it
Review `app_with_health.py` and `Dockerfile` in `code/`.
The app exposes `/healthz` (which returns 503 during a 2s warmup, then 200 OK, and 500 if `/break` is called).

## Run it
Execute the experiment runner:

```bash
./phases/19-health-checks-and-dependencies/01-healthcheck-probes/experiments/run_experiment.sh
```

## Inspect it
1. Observe the immediate status: `Status: running, Health: starting`.
2. After 4 seconds, observe transition to `Health: healthy`.
3. In `docker ps`, notice the status label: `Up 4 seconds (healthy)`.
4. After calling `/break`, observe the probe failures and transition to `(unhealthy)`.

## Break it
Simulate an unresponsive probe by running a health check command that exceeds the timeout:
```bash
docker run --rm -d --name dfs-slow-probe \
    --health-cmd "sleep 5" \
    --health-interval 2s \
    --health-timeout 1s \
    --health-retries 1 \
    alpine:latest sleep 30
sleep 4
docker inspect dfs-slow-probe --format '{{.State.Health.Status}}'
docker rm -f dfs-slow-probe
```
Notice that exceeding `--health-timeout 1s` triggers an immediate probe failure and marks the container `unhealthy`.

## Debug it
When a container is flagged `(unhealthy)`:
1. Inspect the last 5 probe executions and their raw stdout/stderr outputs:
   ```bash
   docker inspect <container> --format '{{range .State.Health.Log}}{{println .Output}}{{end}}'
   ```
2. Run the health probe command manually inside the container to observe errors:
   ```bash
   docker exec -it <container> curl -v http://127.0.0.1:8080/healthz
   ```

## Modify it
Add a health check directly on the command line using `--health-cmd` to an image that has no Dockerfile `HEALTHCHECK`:
```bash
docker run -d --name dfs-cli-hc --health-cmd "ls /tmp" --health-interval 2s alpine:latest sleep 30
docker inspect dfs-cli-hc --format '{{.State.Health.Status}}'
docker rm -f dfs-cli-hc
```

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The transition from `starting` to `healthy`.
- The transition from `healthy` to `unhealthy`.
- The probe logs recorded in `.State.Health.Log`.

## Questions for mastery
1. Does Docker Engine automatically terminate or restart an `unhealthy` container on its own? (Hint: Compose and Swarm differ).
2. Why is using `curl` in a `HEALTHCHECK` risky in minimal distroless images that lack curl?
3. How does `--start-period` prevent premature failure alerts during slow initialization?

## What comes next
We now understand every single primitive of an individual container: processes, layers, filesystems, ports, networks, DNS, volumes, environment variables, resource limits, namespaces, signals, logs, and health checks.
Now we ask: **What if we have 5 containers that must all coordinate together?**
Proceed to **Phase 20: Docker Compose From First Principles**.
