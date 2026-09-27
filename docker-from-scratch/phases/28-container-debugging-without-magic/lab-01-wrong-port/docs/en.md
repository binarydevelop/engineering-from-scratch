# Lesson 28.1: Debugging Lab 01 — The Wrong Port Mismatch

## Motto
"Inspect what port the process actually listens on before trusting what the compose file forwards."

## Problem
**Symptom:**
A developer runs `docker compose up -d`. The container status reports `Up (healthy)`.
The developer runs `curl http://localhost:8080` from the host terminal and receives:
`curl: (7) Failed to connect to localhost port 8080: Connection refused`
The developer checks `docker compose logs` and sees:
`[APP] Starting web server listening internally on 0.0.0.0:8000...`
Why does connecting to port 8080 fail when the container is running and healthy?

## Prediction
1. Does `ports: ["8080:3000"]` forward host 8080 to container 3000 or container 8080?
2. If nothing is listening on port 3000 inside the container, what response does the host kernel receive when connecting to host port 8080?

## Why this matters
Port mapping typos are among the most frequent onboarding and configuration bugs in microservice development. Understanding how host ports bind to container destination ports eliminates guessing.

## First principles
In Compose syntax:
```yaml
ports:
  - "<HOST_PORT>:<CONTAINER_PORT>"
```
If your application process binds internal port `8000`, but your Compose file forwards host `8080` to container `3000`, the kernel NAT rule forwards packets into a black hole where no socket is listening, returning `RST` (Connection refused).

## Mental model

```text
HOST MACHINE: $ curl localhost:8080
      │
      ▼
HOST PORT 8080 (Docker Forwarder)
      │
      │ Forwards to CONTAINER PORT 3000 (as specified in compose)
      ▼
CONTAINER NAMESPACE:
      ├── Port 3000: [EMPTY - Nothing listening!] ──► CONNECTION REFUSED!
      └── Port 8000: [Python Server listening] ◄── Completely bypassed!
```

## Build it
Review `code/docker-compose.yml` and `code/app.py`.
Notice that `app.py` binds port 8000, while `docker-compose.yml` maps `"8080:3000"`.

## Run it
Execute the lab runner:

```bash
./phases/28-container-debugging-without-magic/lab-01-wrong-port/experiments/run_experiment.sh
```

## Inspect it
1. Observe Step 1: `curl http://localhost:8080` returns exit code 7.
2. Check logs: `docker compose logs web` -> `listening internally on 0.0.0.0:8000`.
3. Check mapped port: `docker compose port web 3000` -> `0.0.0.0:8080`.
The mismatch between container destination port 3000 and actual listening port 8000 is obvious.

## Break it
Change the host port mapping to an invalid port range like `"8080:99999"` and observe Compose validate port bounds (must be between 1 and 65535).

## Debug it
1. Formulate Hypothesis: *Host port 8080 is forwarded to the wrong container internal port.*
2. Check listening socket inside container:
   ```bash
   docker compose exec web netstat -tuln (or check application startup logs)
   ```
3. Fix mapping: Update `ports:` to `"8080:8000"`.

## Modify it
Change the host published port to `9090:8000`. Test `curl localhost:9090` and verify.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Symptoms observed.
- Diagnostic reasoning and log clues.
- Verification after applying `docker-compose.fixed.yml`.

## Questions for mastery
1. Why does `docker ps` show the port mapping even when the containerized application has completely crashed?
2. If an application listens on port 8080, can you map it to host port 80?
3. What is the difference between container-to-container port reachability and host-to-container port reachability?

## What comes next
In the next lab, we investigate a container that exits immediately on boot without logging anything. Proceed to **Lab 02: Immediate Exit**.
