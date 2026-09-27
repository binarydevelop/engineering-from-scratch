# Lesson: Debugging Service Startup Dependency Race Conditions

## Motto
"`depends_on` waits for a process to be born; your application needs the service to be ready to serve."

## Problem
In a multi-service application, an API or web service crashes on startup with an error such as:
```
ConnectionRefusedError: [Errno 111] Connection refused
```
The developer checks `docker-compose.yml` and sees:
```yaml
services:
  app:
    depends_on:
      - db
```
The developer is baffled: "I explicitly told Compose that `app` depends on `db`! Why is it attempting to connect before the database is ready?"

## Prediction
Default `depends_on` only checks container lifecycle state (`running`), which occurs within milliseconds after the Docker daemon forks the initial process. The database inside the container takes several seconds to run initialization scripts, start listening sockets, and accept connections. Without a healthcheck probe and `condition: service_healthy`, the dependent application will race ahead and crash.

## Why this matters
This is arguably the #1 most common issue encountered by teams adopting Docker Compose. In production and continuous integration pipelines, intermittent boot crashes lead developers to insert dirty hacks like `sleep 10` in entrypoint scripts. Understanding the difference between process startup and protocol readiness enables robust, deterministic deployments.

## First principles
1. **Container State vs Application State:**
   - The Docker Engine lifecycle has states: `created`, `running`, `paused`, `restarting`, `removing`, `dead`.
   - A container enters the `running` state the microsecond `clone()` or `execve()` succeeds for PID 1.
   - Heavy services (PostgreSQL, MySQL, Kafka, Elasticsearch) perform extensive initialization (replaying WAL logs, running schema migrations, initializing memory buffers) before binding to a network port and accepting connections.
2. **`depends_on` Semantics:**
   - Short syntax: `depends_on: [db]` is syntactic sugar for `condition: service_started`.
   - Long syntax: `depends_on: { db: { condition: service_healthy } }` gates container startup until the target service passes its configured `healthcheck` probe.
3. **Healthcheck Mechanics:**
   - Docker executes the test command inside the target container at configured intervals.
   - Only when the test command exits `0` consistently does the Engine mark the container as `healthy`.

## Mental model
```
Naive depends_on:
db  : [forked: RUNNING] -------------(initdb / replay WAL)-------------> [Ready :5432]
app :                  \
                        \--> [RUNNING] -> Connect(:5432) -> CRASH! Connection Refused

With Healthcheck + condition: service_healthy:
db  : [RUNNING] -> [pg_isready: fail] -> [pg_isready: ok: HEALTHY]
app : (BLOCKED WAITING)......................................\-> [RUNNING] -> Connect(:5432) -> SUCCESS!
```

## Build it
1. `code/app.py`: A Python client that attempts an immediate TCP socket connection to `db:5432` without retries.
2. `code/docker-compose.yml`: A broken Compose file using naive `depends_on: [db]`.
3. `code/docker-compose.fixed.yml`: A fixed Compose file configuring a healthcheck probe with `pg_isready -U postgres` and `condition: service_healthy`.

## Run it
Run the automated experiment:
```bash
./phases/28-container-debugging-without-magic/lab-07-dependency-race/experiments/run_experiment.sh
```

## Inspect it
Observe container states during startup:
```bash
docker compose ps
```
Notice the `(health: starting)` transition to `(healthy)` before the `app` container is spawned.

## Break it
Remove the `condition: service_healthy` block from `docker-compose.fixed.yml` and restart the stack from a cold state. The app crashes immediately.

## Debug it
1. Check container exit code: `docker inspect <app> --format '{{.State.ExitCode}}'`.
2. Inspect target service readiness: Run the target readiness command manually (`docker exec -it <db> pg_isready -U postgres`).
3. Check `healthcheck` status on the target:
```bash
docker inspect <db> --format '{{json .State.Health}}' | jq .
```

## Modify it
Implement application-level resilience by adding an exponential backoff retry loop in `code/app.py` in addition to Compose-level health gating. This creates defense-in-depth against transient network hiccups.

## Evidence
Running `run_experiment.sh` yields:
```
[+] Step 1: Reproduce startup race condition with naive depends_on...
[-] ERROR: Connection failed: [Errno 111] Connection refused
[-] First Principles Diagnostic: 'depends_on' only waits for container creation, not TCP readiness.
[+] CONFIRMED: App failed because db was not yet accepting TCP connections.

[+] Step 2: Run fixed compose with healthcheck and condition: service_healthy...
 ✔ Container lab07-fixed-db   Healthy
 ✔ Container lab07-fixed-app  Started
[*] App starting... attempting immediate TCP connection to db:5432...
[+] SUCCESS: Connected to db:5432! Service is ready.
```

## Questions for mastery
1. Why does Compose not automatically inspect open ports on containers to determine readiness?
2. What are the trade-offs between Compose-level health gating and application-level retry loops?
3. How does `start_period` in a healthcheck prevent false-positive failures during slow database migrations?

## What comes next
In Lab 08, we explore PID 1 zombie reaping and signal handling: why containers hang for 10 seconds on `docker stop` and accumulate `<defunct>` zombie processes.
