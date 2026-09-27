# Lesson 17.1: Signals, PID 1, and Graceful Shutdown

## Motto
"Never use shell form for long-running servers; PID 1 must receive `SIGTERM` directly to shut down cleanly without hangs."

## Problem
In many companies, engineers notice that stopping a container with `docker stop` or deploying a rolling update in Kubernetes takes a mandatory 10 seconds per container.
During those 10 seconds:
- In-flight HTTP transactions are brutally terminated midway.
- Database connection pools are dropped unceremoniously without releasing locks.
- The container exits with code 137 instead of code 0.
Why does `docker stop` take 10 seconds, and why did the application ignore `SIGTERM`?

## Prediction
1. What signal does `docker stop` send first? What signal does it send after 10 seconds?
2. What process runs as PID 1 when you write `CMD python3 server.py` versus `CMD ["python3", "server.py"]`?
3. Does `/bin/sh` forward `SIGTERM` to child processes by default?

## Why this matters
In production, rolling deployments and zero-downtime updates require graceful draining. When a worker receives `SIGTERM`, it must stop accepting new jobs, finish in-flight requests, flush database writes, and exit within a few hundred milliseconds. If signal handling is broken, deployments take 10x longer and corrupt active user sessions.

## First principles
1. **The Unix PID 1 Rules**:
   In Unix systems, the process with Process ID 1 is the `init` process. The Linux kernel treats PID 1 differently from all other processes:
   - **No Default Signal Actions**: For ordinary processes, receiving `SIGTERM` causes immediate termination by default. For PID 1, the kernel does **not** apply default signal actions. If PID 1 does not install an explicit signal handler for `SIGTERM`, the signal is silently ignored!
   - **Zombie Reaping**: When child processes terminate, PID 1 must call `wait()` to collect their exit statuses; otherwise, dead processes linger in the process table as "zombies" (`<defunct>`).
2. **The Shell Form Trap**:
   - `CMD python3 server.py` (Shell form): Docker executes `/bin/sh -c "python3 server.py"`.
   - `/bin/sh` is PID 1.
   - `python3` is PID 2 (a child process).
   - When you run `docker stop`, Docker sends `SIGTERM` to PID 1 (`/bin/sh`).
   - Standard POSIX shells (`/bin/sh`, `dash`, `ash`) do **not** forward signals to child processes!
   - Python never receives `SIGTERM`. It continues running blissfully unaware.
   - After the 10-second grace period expires, Docker sends `SIGKILL` (signal 9), annihilating the process tree with exit code 137.
3. **The Exec Form Solution**:
   - `CMD ["python3", "server.py"]` (Exec form): Docker invokes `execve()` directly on `python3`.
   - `python3` is PID 1. It receives `SIGTERM` directly from the kernel and triggers your cleanup handler immediately!

## Mental model

```text
CASE A: Shell Form: CMD python3 server.py
┌────────────────────────────────────────────────────────┐
│  Container PID Namespace                               │
│                                                        │
│  PID 1: /bin/sh -c "python3 server.py"                 │
│         │ (Receives SIGTERM, SWALLOWS IT, does not fwd)│
│         ▼                                              │
│  PID 2: python3 server.py (Never hears SIGTERM!)       │
│                                                        │
│  10-Second Grace Period Expires ──► KERNEL SIGKILL!    │
│  Container dies violently (Exit Code 137)              │
└────────────────────────────────────────────────────────┘

CASE B: Exec Form: CMD ["python3", "server.py"]
┌────────────────────────────────────────────────────────┐
│  Container PID Namespace                               │
│                                                        │
│  PID 1: python3 server.py                              │
│         │ (Receives SIGTERM directly!)                 │
│         ▼                                              │
│  handle_sigterm() executes: drains state, closes FDs   │
│  Exits gracefully in <500ms (Exit Code 0)              │
└────────────────────────────────────────────────────────┘
```

## Build it
Review `server_graceful.py`, `Dockerfile.exec`, and `Dockerfile.shell` in `code/`.

## Run it
Execute the experiment runner:

```bash
./phases/17-signals-pid1-and-lifecycle/01-sigterm-propagation-and-pid1/experiments/run_experiment.sh
```

## Inspect it
1. Notice that `dfs-exec-demo` exits in **0 seconds** with code 0!
2. Check `docker logs dfs-exec-demo`: It logged `Caught SIGTERM! Draining connections... Clean shutdown complete.`
3. Notice that `dfs-shell-demo` hung until the timeout and exited with code **137**.

## Break it
Launch a container with an unhandled infinite loop:
```bash
docker run -d --name dfs-hang alpine:latest sh -c "trap '' TERM; while true; do sleep 1; done"
time docker stop -t 2 dfs-hang
docker inspect dfs-hang --format 'ExitCode: {{.State.ExitCode}}'
docker rm -f dfs-hang
```
Notice that when `SIGTERM` is explicitly ignored, `docker stop` is forced to issue `SIGKILL` (ExitCode 137).

## Debug it
When containers take 10 seconds to stop during deployments:
1. Inspect the entrypoint/command form in your Dockerfile. If it's a raw string without JSON array brackets, rewrite it as `CMD ["binary", "arg1"]`.
2. If your service requires a shell wrapper script, replace the last line with `exec "$@"`:
   ```bash
   #!/bin/sh
   # Perform migrations
   exec python3 server.py  # 'exec' replaces the shell process with python3 as PID 1!
   ```
3. Alternatively, pass `--init` to `docker run` to inject Tini as PID 1.

## Modify it
Run a shell container with `--init`:
```bash
docker run -d --name dfs-init-demo --init dfs-sig-shell:v1
docker top dfs-init-demo
docker stop dfs-init-demo
docker rm -f dfs-init-demo
```
Notice that Docker injects `docker-init` (Tini) as PID 1 to properly route signals and reap zombies!

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Timing comparison: Exec form duration vs Shell form duration.
- The graceful shutdown log lines from `server_graceful.py`.
- The exit codes observed in both scenarios.

## Questions for mastery
1. What does the bash `exec` command do, and why is it standard practice in container entrypoint scripts?
2. What happens if a child process exits inside a container and PID 1 never calls `wait()`?
3. How does `docker stop -t <seconds>` allow you to adjust the grace period?

## What comes next
We understand how signals reach applications. Now: **How does Docker capture everything the application logs to the screen?** Proceed to **Phase 18: Logs and stdout/stderr**.
