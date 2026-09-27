# Lesson 18.1: Logs and Standard Streams (`stdout`/`stderr`)

## Motto
"Treat logs as unbuffered event streams emitted to `stdout` and `stderr`; never write logs to arbitrary files inside a container."

## Problem
In legacy monolithic systems, applications wrote logs to `/var/log/my-app/app.log` and used cron jobs to rotate them.
When developers apply this pattern inside containers:
1. When the container crashes or is deleted, all log files inside the ephemeral writable layer vanish forever!
2. Writing unrotated logs inside a container silently fills the root filesystem until the disk runs out of inodes.
3. Centralized observability tools (Datadog, Fluentbit, Vector, CloudWatch) cannot read logs hidden inside arbitrary container filesystem paths.
How does Docker expect applications to log?

## Prediction
1. Does `docker logs` combine `stdout` and `stderr` or keep them separate?
2. Where does Docker physically store container logs on disk?
3. What happens if a long-running container writes 50GB of logs to `stdout`?

## Why this matters
The Twelve-Factor App methodology (Factor XI: Logs) states: *An application should never concern itself with routing or storage of its output stream. It should write its event stream directly to `stdout`.*
Docker captures standard streams automatically and multiplexes them with 8-byte binary headers.

## First principles
1. **File Descriptors 1 and 2**:
   Every process inherits standard file descriptors:
   - `FD 1`: `stdout` (normal operational events)
   - `FD 2`: `stderr` (errors, warnings, diagnostic stack traces)
2. **The Logging Driver Pipeline**:
   ```text
   Container Process (writes to FD 1 & FD 2)
       │
       ▼
   containerd-shim (captures pipes via pseudo-terminal or raw FIFO)
       │
       ▼
   Docker Logging Driver (default: json-file)
       │
       ├── Appends JSON record to /var/lib/docker/containers/<id>/<id>-json.log
       │   {"log":"[INFO] event\n","stream":"stdout","time":"2026-09-21T..."}
       │
       ▼
   docker logs CLI (reconstructs streams or filters by stream type)
   ```
3. **Log Rotation**:
   By default, `json-file` grows indefinitely without rotation! In production, you must configure `--log-opt max-size=10m --log-opt max-file=3` in `daemon.json` to prevent disk exhaustion.

## Mental model

```text
CONTAINER NAMESPACE
┌────────────────────────────────────────────────────────┐
│  Python Process                                        │
│  ├── sys.stdout.write()  ──► FD 1                      │
│  └── sys.stderr.write()  ──► FD 2                      │
└──────────────────────────┬─────────────────────────────┘
                           │ Intercepted by Docker Engine
                           ▼
HOST DOCKER ENGINE (Logging Driver)
┌────────────────────────────────────────────────────────┐
│  /var/lib/docker/containers/<id>/<id>-json.log         │
│  {"log":"[INFO] ...","stream":"stdout","time":...}     │
│  {"log":"[WARN] ...","stream":"stderr","time":...}     │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             │ docker logs               │ docker logs 2> errors.log
             ▼                           ▼
┌──────────────────────────┐ ┌──────────────────────────┐
│ Combined unified stream  │ │ Filtered stderr only     │
└──────────────────────────┘ └──────────────────────────┘
```

## Build it
Review [logger_app.py](../code/logger_app.py).
It writes info messages to `stdout` and warnings to `stderr`.

## Run it
Execute the experiment runner:

```bash
./phases/18-logs-and-stdstreams/01-stdout-stderr-json-logging/experiments/run_experiment.sh
```

## Inspect it
1. Run `docker logs <container>`. Notice how Docker presents a unified stream.
2. In Step 3, inspect how redirecting `> stdout.txt 2> stderr.txt` separates standard output from standard error.
3. Inspect `docker inspect <container> --format '{{.LogPath}}'`. This shows the host log file path.

## Break it
Launch a container that buffers output without flushing:
```bash
docker run --rm -d --name dfs-buffer python:3.11-slim python3 -c "import time; print('Buffered message'); time.sleep(30)"
docker logs dfs-buffer
```
Notice that `docker logs` might show nothing initially!
Python buffers `stdout` by default when not connected to an interactive TTY.
To fix this, pass `PYTHONUNBUFFERED=1` or `ENV PYTHONUNBUFFERED=1` in your Dockerfile.
Clean up: `docker rm -f dfs-buffer`.

## Debug it
When troubleshooting container logs:
1. Follow logs in real-time: `docker logs -f <container>`.
2. Inspect only recent entries: `docker logs --tail 100 <container>`.
3. Add ISO timestamps to diagnose event ordering: `docker logs -t <container>`.
4. Inspect only since a relative time: `docker logs --since 5m <container>`.

## Modify it
Run a container configured with strict log rotation limits:
```bash
docker run --rm -d --name dfs-rotate --log-opt max-size=1k --log-opt max-file=2 alpine:latest sh -c "while true; do echo 'flooding logs' ; sleep 0.01; done"
sleep 2
docker inspect dfs-rotate --format '{{json .HostConfig.LogConfig}}'
docker rm -f dfs-rotate
```
Verify the log configuration options.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Output of `docker logs` showing stdout and stderr.
- Verification of stream separation via `2>` redirection.
- The `.LogPath` JSON location.

## Questions for mastery
1. Why does Python's standard output buffering cause issues in container logs if `PYTHONUNBUFFERED=1` is omitted?
2. What are the dangers of leaving Docker's default logging driver unconstrained on a production server?
3. How do production aggregators (Fluentbit/Vector) read logs without executing `docker logs`?

## What comes next
We know the container process is running and logging. But does "process exists" mean "application is ready to receive user requests"? Proceed to **Phase 19: Health Checks and Dependencies**.
