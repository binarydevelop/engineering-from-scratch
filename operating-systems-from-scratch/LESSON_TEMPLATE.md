# Lesson Template

Use this canonical template when writing or extending any lesson across the curriculum.

---

# [Phase XX] Lesson Title

## Motto
> **Understand it. Build it. Run it. Inspect it. Measure it. Break it. Debug it. Rebuild it.**

*(A memorable one-sentence operating systems principle specific to this lesson)*

## Problem
What fundamental hardware limitation, concurrency hazard, or resource contention problem forces this abstraction to exist? Why can't we simply write raw user code without the kernel?

## Prediction
Before executing the code or simulation:
1. What will the terminal output look like?
2. How many processes, threads, or file descriptors will be active?
3. Which system calls will be invoked?
4. What happens when two entities race or resource limits are reached?

## Why this matters
How does this mechanism directly impact software engineering? (e.g. why Redis uses an event loop, why databases fsync their write-ahead log, why Docker containers can share host memory).

## First principles
Deconstruct the mechanism into basic computer architecture facts:
* CPU registers and execution rings
* Physical RAM bytes and buses
* Disk sectors and storage controllers
* Network hardware interrupts

## Mental model
Visual ASCII diagram illustrating state transitions, table mappings, or memory layouts.

```text
[ Userspace Application ]
          │
          ▼ Syscall
[ Kernel Table / MMU ]
          │
          ▼ Hardware
[ Physical Device / Memory ]
```

## Build / simulate it
Build a simplified educational version in Python or C to isolate the core logic before dealing with real kernel complexity.

## Observe the real OS
Run the compiled C code or command against the live operating system.

## Inspect it
Use diagnostic tools to view kernel tables and live metrics:
* `ps`, `top`, `pidstat`
* `lsof`, `ss`
* `/proc/<pid>/`
* `vmstat`, `free`

## Trace it
Use system call and trace tools:
```bash
strace -c -e trace=memory ./binary
```

## Measure it
Quantify latency, throughput, context switches, or memory footprint using benchmarks and timers.

## Break it
Intentionally trigger the failure mode:
* Remove the lock to cause a race condition
* Omit `wait()` to create a zombie
* Leak descriptors to hit `EMFILE`
* Exceed memory to trigger swap or OOM

## Debug it
Walk step-by-step through the diagnosis using:
* `gdb` backtraces
* `strace` logs
* `/proc` descriptor counts
* `valgrind` / sanitizers

## Modify it
Challenge yourself with an explicit modification task that forces you to adapt the code to handle edge cases.

## Evidence
Record your observations in `outputs/evidence-template.md`:
* System kernel version
* Actual vs predicted output
* Syscall trace counts
* Final diagnostic resolution

## Questions for mastery
Deep, reasoning-based questions that test mechanical understanding rather than memorization.

## Production connection
How does this lesson explain real-world behaviors in:
* PostgreSQL / MySQL
* Docker / Kubernetes
* Nginx / Envoy / Node.js
* Kafka / Distributed Brokers

## What comes next
Bridge to the next phase in the curriculum progression.
