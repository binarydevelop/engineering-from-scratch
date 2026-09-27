# Phase 23: Race Conditions

## Motto
> **A race condition turns deterministic programs into unpredictable rolls of the scheduling dice.**

## Problem
Why does incrementing a shared variable across multiple threads produce incorrect, non-deterministic values?

## Prediction
Before executing the code or experiments in this phase:
1. What will the machine or kernel state look like before invocation?
2. Which system calls will be invoked, and in what sequence?
3. How will memory, CPU scheduling, or file descriptors be affected?
4. What happens when resource limits or concurrent access edge-cases are reached?

## Why this matters
This mechanism directly governs production performance and stability:
* Key Concepts: interleaving, critical section, non-deterministic execution
* Essential Linux Tools: `ThreadSanitizer (-fsanitize=thread)`
* Real-World Impact: Diagnosing high CPU, memory leaks, I/O bottlenecks, and container boundaries.

## First principles
Deconstructing to physical computer architecture:
* CPU execution mode: Privilege levels, instruction pointer, registers.
* Memory subsystem: Virtual page tables, physical RAM, hardware caches.
* I/O subsystem: File descriptors, kernel ring buffers, persistent disk blocks.

## Mental model
```text
┌────────────────────────────────────────────────────────┐
│               USER APPLICATION (Ring 3)                │
└───────────────────────────┬────────────────────────────┘
                            │ System Call / Hardware Trap
┌───────────────────────────▼────────────────────────────┐
│                  KERNEL SUBSYSTEM (Ring 0)             │
│   Race Conditions Mechanisms & Kernel State Tables             │
└───────────────────────────┬────────────────────────────┘
                            │ Hardware Control
┌───────────────────────────▼────────────────────────────┐
│                    PHYSICAL HARDWARE                   │
│             CPU Cores, RAM, Disk, Sockets              │
└────────────────────────────────────────────────────────┘
```

## Build / simulate it
Check `code/` in this phase directory for working implementations demonstrating this mechanism.

## Observe the real OS
Run the compiled code and observe real operating system state using diagnostic utilities:
```bash
./labs/broken-systems/lab-15-race-condition-counter
```

## Inspect it
Use Linux telemetry tools to inspect internal tables:
* Key utilities: `ThreadSanitizer (-fsanitize=thread)`
* Check `/proc/<pid>/` on Linux or equivalent platform tools.

## Trace it
Use `strace` or tracing tools to inspect the system call boundary:
```bash
strace -c -e trace=all ./labs/broken-systems/lab-15-race-condition-counter
```

## Measure it
Quantify latency, context switches, memory consumption, or throughput. Compare with benchmarks in `benchmarks/`.

## Break it
Increase thread count and observe update losses escalate.

## Debug it
Diagnose the failure using `gdb`, `strace`, `/proc`, and `lsof` without modifying source code initially. Identify the exact error code or hardware signal.

## Modify it
Extend the implementation to handle edge cases:
* Add defensive error handling for return codes.
* Handle signals gracefully.
* Ensure deterministic cleanup of descriptors and allocated memory.

## Evidence
Record your experimental findings in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does the operating system provide this abstraction rather than raw direct hardware access?
2. How does the kernel represent this mechanism internally in memory?
3. How would you diagnose an incident in production involving this subsystem?

## Production connection
Connects directly to:
* High-concurrency web servers (Nginx, Envoy, Node.js)
* Databases (PostgreSQL, MySQL, Redis, Kafka)
* Container runtimes (Docker, Podman, Kubernetes)

## What comes next
Progression to Phase 24.
