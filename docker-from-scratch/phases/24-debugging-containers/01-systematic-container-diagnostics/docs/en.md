# Lesson 24.1: Systematic Container Diagnostics

## Motto
"Never guess; formulate a hypothesis, inspect the state machine, and let the evidence isolate the failure."

## Problem
When a container fails in production, many developers enter panic mode:
They restart the container, prune images, edit Dockerfiles at random, add print statements, and repeatedly run `docker run` hoping it fixes itself.
This cargo-cult debugging wastes hours and masks intermittent failure modes.
Container failures are deterministic state transitions. How do you triage any broken container in under 60 seconds using a structured protocol?

## Prediction
1. If a container exits with code 137, how can you definitively tell whether it was killed by an OOM limit or stopped by a human running `docker kill`?
2. If `curl localhost:8080` fails, what are the three distinct points of potential failure along the network path?
3. Where does Docker store the exit code of an exited container?

## Why this matters
High-availability systems engineering requires rapid Mean Time To Detection (MTTD) and Mean Time To Resolution (MTTR). Following an orderly decision tree prevents you from wasting time diagnosing application code when the issue is a missing environment variable, or debugging network routing when the issue is a port collision.

## First principles
1. **Container State Telemetry:** The container runtime records the exact termination status in kernel data structures and stores it in the container metadata: `ExitCode`, `OOMKilled`, `StartedAt`, and `FinishedAt`.
2. **Deterministic Triage Order:** When diagnosing any failure, work from the outside inward: container status -> exit code -> log streams -> process state -> listening ports -> network routes -> mount permissions.
3. **Decoupled Telemetry:** Because Docker persists container metadata and stdstream ring buffers after process death, you can inspect an exited container's autopsy without needing to keep it running.

## Mental model
The **10-Step Container Diagnostic Protocol**:

```text
               SYMPTOM OBSERVED (Error / Hang / Crash)
                                  │
    ┌─────────────────────────────┴─────────────────────────────┐
    ▼                                                           ▼
Is container running? (docker ps -a)         Inspect exit status (docker inspect)
    │                                            ├── ExitCode 0: Finished task
    ├── NO: Check ExitCode & OOMKilled           ├── ExitCode 1: App crash (check logs)
    │       (137 + OOMKilled: true = RAM limit!) ├── ExitCode 127: Binary not found
    │                                            └── ExitCode 137: SIGKILL or OOM
    │
    ▼ YES: Container is running
Inspect Process State (docker top <c>)
    │
    ├── Is the expected daemon process running?
    └── Is PID 1 stuck in a loop or deadlocked?
    │
    ▼
Inspect Listening Ports (docker exec <c> netstat -tuln)
    │
    ├── Is socket listening on 0.0.0.0 (all interfaces)?
    └── Or is it trapped on 127.0.0.1 (local only)?
    │
    ▼
Inspect Port Forwarding (docker port <c>)
    │
    └── Is host port mapped correctly to internal container port?
    │
    ▼
Inspect Network & DNS (docker network inspect / nslookup)
    │
    ├── Are both containers on the same user-defined network?
    └── Can embedded DNS (127.0.0.11) resolve the service name?
    │
    ▼
Inspect Volumes & Permissions (docker inspect --format '{{.Mounts}}')
    │
    └── Are UID/GID permissions matched on mounted host directories?
```

## Build it
Review [diagnose.sh](../code/diagnose.sh).
It extracts all 10 diagnostic vectors from Docker Engine's JSON inspection API into a single clean report.

## Run it
Execute the experiment runner:

```bash
./phases/24-debugging-containers/01-systematic-container-diagnostics/experiments/run_experiment.sh
```

## Inspect it
1. Observe Case 1: The diagnostic report pinpoints `ExitCode: 2` and extracts the exact fatal error message from `docker logs`.
2. Observe Case 2: The report flags `OOMKilled: true` and identifies that the kernel Out-Of-Memory killer terminated the process.

## Break it
Launch a container with an invalid entrypoint path:
```bash
docker run -d --name dfs-bad-bin alpine:latest /bin/nonexistent_tool
./phases/24-debugging-containers/01-systematic-container-diagnostics/code/diagnose.sh dfs-bad-bin
docker rm -f dfs-bad-bin
```
Notice the diagnostic report immediately reveals:
`ExitCode: 127` (Command not found)!

## Debug it
When troubleshooting an unresponsive running container:
1. Attach to container logs interactively: `docker logs --tail 20 -f <container>`.
2. Open an emergency debug shell inside the live container:
   ```bash
   docker exec -it <container> /bin/sh
   ```
3. Inspect network connectivity from inside:
   ```bash
   docker exec -it <container> ping <peer-service>
   ```

## Modify it
Extend [diagnose.sh](../code/diagnose.sh) to check if `State.Health` is present, and if so, print the current health check status (`healthy`, `unhealthy`, or `starting`).

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The diagnostic report for the immediately exited container.
- The diagnostic report for the OOM killed container.
- The 10-step triage protocol summarized in your own words.

## Questions for mastery
1. What does exit code 126 mean in Unix/Docker? (Command found but not executable due to permissions or missing dynamic linker).
2. Why is `docker exec` preferred over SSH for debugging containers?
3. How can you debug a container that crashes so quickly that `docker exec` cannot attach? (Hint: override entrypoint with `sleep 300` or inspect `docker logs`).

## What comes next
Now that we have diagnostic mastery, we explore security: **What permissions does a container have, why is root dangerous, and why is mounting the Docker socket a critical vulnerability?** Proceed to **Phase 25: Docker Security Foundations**.
