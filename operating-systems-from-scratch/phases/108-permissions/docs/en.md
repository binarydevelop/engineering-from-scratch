# Phase 108: Permissions

## Motto
> **Every file operation is checked against the trinity of User, Group, and Other permissions.**

## Problem
How does the operating system enforce security access control on files and directories?

## Prediction
Before executing the code or experiments in this phase:
1. What will the machine or kernel state look like before invocation?
2. Which system calls will be invoked, and in what sequence?
3. How will memory, CPU scheduling, or file descriptors be affected?
4. What happens when resource limits or concurrent access edge-cases are reached?

## Why this matters
This mechanism directly governs production performance and stability:
* Key Concepts: rwx bits, octal modes (0755, 0644), setuid, setgid, sticky bit
* Essential Linux Tools: `ls -l, chmod, chown`
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
│   Permissions Mechanisms & Kernel State Tables             │
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
ls -la Makefile
```

## Inspect it
Use Linux telemetry tools to inspect internal tables:
* Key utilities: `ls -l, chmod, chown`
* Check `/proc/<pid>/` on Linux or equivalent platform tools.

## Trace it
Use `strace` or tracing tools to inspect the system call boundary:
```bash
strace -c -e trace=all ls -la Makefile
```

## Measure it
Quantify latency, context switches, memory consumption, or throughput. Compare with benchmarks in `benchmarks/`.

## Break it
Remove execute bit from a binary and attempt execution (observe EACCES).

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
Progression to Phase 109.
