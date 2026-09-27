# Lesson 15.1: Resource Limits and Control Groups (`cgroups`)

## Motto
"Control groups (cgroups) are the kernel's resource meters and throttles; without them, a single runaway process can crash your entire host."

## Problem
In unconstrained shared environments, a memory leak or an infinite loop in one container can consume all available RAM on the server.
When the Linux kernel runs out of physical memory, the system panics or the kernel Out-Of-Memory (OOM) killer randomly selects and terminates critical host processes (like `sshd` or `dockerd`).
How does Docker ensure that a buggy microservice cannot crash its neighbors or freeze the host machine?

## Prediction
1. What happens if a Python container with a 50MB memory limit tries to allocate 100MB of RAM?
2. Does the process receive a `MemoryError` exception, or is it killed by the kernel?
3. If killed, what exit code does Docker report?

## Why this matters
Production multi-tenant clusters (Kubernetes, ECS, Docker Compose) rely entirely on cgroups to enforce Quality of Service (QoS). Understanding exit code 137 and `OOMKilled: true` is essential for diagnosing sudden microservice crashes under production traffic spikes.

## First principles
1. **Control Groups (cgroups)**:
   A Linux kernel mechanism that organizes processes into hierarchical groups and meters/limits their physical resource consumption:
   - `memory`: Limits physical RAM usage (`memory.max` in cgroups v2).
   - `cpu`: Throttles CPU execution time using the Completely Fair Scheduler (CFS) quota (`cpu.max`).
   - `pids`: Limits the maximum number of processes/threads to prevent fork bombs.
2. **The Out-Of-Memory (OOM) Killer**:
   When a cgroup's memory usage reaches its limit and cannot reclaim memory through page flushing, the kernel invokes `oom_killer`.
   The kernel sends an uncatchable `SIGKILL` (signal 9) to the process.
3. **The 137 Formula**:
   Because `SIGKILL` is signal 9, POSIX shells report exit code `128 + 9 = 137`.

## Mental model

```text
LINUX KERNEL CONTROL GROUPS:
┌────────────────────────────────────────────────────────────────────────┐
│  Host Memory Pool (Total: 8 GB)                                        │
├────────────────────────────────────────────────────────────────────────┤
│  Cgroup: /docker/dfs-oom-test (Memory Limit: 50 MB)                    │
│                                                                        │
│   Heap: [ 10MB ] ──► [ 20MB ] ──► [ 30MB ] ──► [ 40MB ] ──► [ 50MB ]   │
│                                                                 │      │
│                                           Kernel OOM Triggered! ▼      │
│                                           Sends SIGKILL (9) ─────────┐ │
│                                                                      │ │
│   Process Terminated Immediately!                                    ▼ │
│   Exit Code: 137 (128 + 9)                                  [KILLED]   │
└────────────────────────────────────────────────────────────────────────┘
```

## Build it
Review [memory_hog.py](../code/memory_hog.py).
It allocates 10MB byte arrays into a list in a loop without releasing them.

## Run it
Execute the experiment runner:

```bash
./phases/15-resource-limits-and-cgroups/01-cgroup-limits-and-oom/experiments/run_experiment.sh
```

## Inspect it
1. Observe the process termination after allocating 40MB.
2. Inspect the exit code: `echo $?` -> `137`.
3. Query Docker Engine metadata:
   ```bash
   docker inspect dfs-oom-test --format 'OOMKilled: {{.State.OOMKilled}}, ExitCode: {{.State.ExitCode}}'
   ```
   Notice `OOMKilled: true`.
4. In Step 4, observe that `--cpus 0.5` caps an infinite CPU loop at exactly ~50% CPU utilization in `docker stats`!

## Break it
Launch a fork-bomb container with a PID limit to observe process throttling:
```bash
docker run --rm --pids-limit 10 alpine:latest sh -c "while true; do sleep 10 & done"
```
Notice that when the container attempts to spawn its 11th process, the kernel returns `sh: can't fork: Resource temporarily unavailable`. The host remains completely safe!

## Debug it
When a container in production randomly dies with exit code 137:
1. Check `docker inspect <container> --format '{{.State.OOMKilled}}'`.
2. If `true`, the application ran out of cgroup memory. Either increase the memory limit (`-m`) or optimize application memory efficiency.
3. Check host kernel messages:
   ```bash
   dmesg -T | grep -i oom
   ```

## Modify it
Increase the container limit to `-m 100m`. Run `memory_hog.py` and observe that it safely allocates up to 90MB before terminating.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The exact memory allocation log where termination occurred.
- The `OOMKilled: true` confirmation from `docker inspect`.
- The CPU percentage measured during the CPU throttling test.

## Questions for mastery
1. Why does an OOM-killed process not have a Python traceback in `docker logs`?
2. What is the difference between `--memory-swap` and `--memory`?
3. How do cgroups differ from Linux namespaces?

## What comes next
We now understand how cgroups restrict *what a process can consume*. But how does Docker restrict *what a process can see*? Proceed to **Phase 16: Isolation and Namespaces**.
