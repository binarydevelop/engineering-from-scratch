# Lesson: Debugging Zombie Process Accumulation and PID 1 Signal Traps

## Motto
"If PID 1 is not an init process, orphaned processes become eternal zombies and SIGTERM falls on deaf ears."

## Problem
A backend service container exhibits two distinct production pathologies:
1. Whenever the container is stopped (`docker stop <container>`), the command freezes for 10 seconds before forcibly exiting with exit code 137.
2. In long-running worker containers that spawn background tasks, the process table gradually fills up with `<defunct>` zombie processes, eventually exhausting kernel PID limits.

## Prediction
If a container uses shell form in `ENTRYPOINT` or `CMD` (e.g., `CMD python worker.py` instead of `["python", "worker.py"]`), the Linux shell (`/bin/sh`) becomes PID 1. The shell does not forward `SIGTERM` to child processes and does not reap orphaned child processes. Using exec form or Docker's built-in init supervisor (`--init` / `tini`) restores signal propagation and zombie reaping.

## Why this matters
In Kubernetes, ECS, or Docker Compose, orchestration platforms send `SIGTERM` to initiate graceful draining before terminating a container. When a container ignores `SIGTERM`, it blocks deployments for the full termination grace period (default 10 to 30 seconds), drops active user connections, and risks database connection leaks or corrupted file writes.

## First principles
1. **The Special Nature of PID 1 in Linux:**
   - **Signal Immunity:** In standard Linux processes, an unhandled `SIGTERM` terminates the process. For PID 1, the Linux kernel ignores unhandled signals to prevent accidental system crashes. If PID 1 does not install an explicit signal handler, `SIGTERM` has zero effect.
   - **Orphan Reaping:** When a child process terminates, it enters the `zombie` state (`Z`) until its parent calls `wait()` or `waitpid()` to read its return code. If the parent terminates before calling `wait()`, the child is orphaned and adopted by PID 1. If PID 1 does not call `wait()`, the zombie entry remains in the kernel process table indefinitely.
2. **The Shell Form Trap:**
   - Writing `CMD python /worker.py` compiles to `/bin/sh -c "python /worker.py"`.
   - `/bin/sh` runs as PID 1. It does not forward POSIX signals to the child Python process.
3. **Docker Init (`tini`):**
   - Running with `docker run --init` or `init: true` in Compose inserts `/sbin/docker-init` (a lightweight C binary based on `tini`) as PID 1.
   - `tini` registers signal handlers, forwards all signals to child process groups, and continuously reaps zombie orphans.

## Mental model
```
Shell Form (Broken):
[Docker Stop: SIGTERM]
         |
         v
     [PID 1: /bin/sh] ---> Ignores SIGTERM! (Does not forward to child)
         |
         v
     [PID 7: python]  ---> Never receives SIGTERM!
         ... 10 seconds elapse ...
[Docker Engine sends SIGKILL (137)] ---> Forcible kill, dropped connections!

With --init / tini (Fixed):
[Docker Stop: SIGTERM]
         |
         v
     [PID 1: docker-init] ---> Forwards SIGTERM immediately!
         |
         v
     [PID 2: python]      ---> Handles SIGTERM -> clean flush -> exits 0!
```

## Build it
1. `code/worker.py`: A Python worker that installs a `SIGTERM` handler and forks short-lived child processes without calling `wait()`.
2. `code/Dockerfile.broken`: Uses shell form `CMD python /worker.py`.
3. `code/Dockerfile.fixed`: Uses exec form `ENTRYPOINT ["python", "-u", "/worker.py"]` and runs with `--init`.

## Run it
Run the experiment script:
```bash
./phases/28-container-debugging-without-magic/lab-08-zombie-reaping-pid1/experiments/run_experiment.sh
```

## Inspect it
Inspect the process hierarchy from the host:
```bash
docker top <container>
```
In the broken container, observe `/bin/sh` as PID 1. In the fixed container, observe `/sbin/docker-init` as PID 1.

## Break it
Launch a container with `CMD ["sh", "-c", "python /worker.py"]` and trigger `docker stop`. Notice the exact 10-second delay before exit code 137.

## Debug it
1. Run `docker inspect <container> --format '{{.State.ExitCode}}'`. If it is `137` after `docker stop`, `SIGTERM` was ignored.
2. Inspect the entrypoint configuration using `docker inspect <container> --format '{{json .Config.Cmd}}'`.
3. Check if the process responds to signals by running `docker kill -s SIGTERM <container>`. If it continues running, PID 1 has not trapped the signal.

## Modify it
In `docker-compose.yml`, enable the init supervisor declaratively for any service by adding:
```yaml
services:
  worker:
    init: true
```

## Evidence
Running `run_experiment.sh` produces:
```
[*] Process tree inside broken container (via docker top):
UID   PID    PPID   CMD
root  11499  11476  /bin/sh -c python /worker.py
root  11513  11499  python /worker.py

[*] Testing stop behavior on broken container (with 2s timeout)...
[+] Stopped in 2s with exit code 137
[+] CONFIRMED: Process failed to handle SIGTERM and was SIGKILLed (exit code 137).

[*] Process tree inside fixed container (via docker top, note docker-init):
UID   PID    PPID   CMD
root  11596  11574  /sbin/docker-init -- python -u /worker.py
root  11611  11596  python -u /worker.py

[*] Testing stop behavior on fixed container...
[+] Fixed container stopped in 0s with exit code 0
[+] SUCCESS: Graceful shutdown verified under PID 1 init supervisor!
```

## Questions for mastery
1. Why does Python's `multiprocessing` or subprocess management sometimes spawn zombies inside containers?
2. What is the difference between `docker stop` and `docker kill`?
3. When is it preferable to handle signals directly in application code vs delegating to `tini`?

## What comes next
Having conquered all 8 real-world debugging labs, we now transition to Phase 29: Rebuilding the complete multi-service production system design lab step-by-step from first principles.
