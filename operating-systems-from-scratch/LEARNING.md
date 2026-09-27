# Learning Operating Systems From Scratch: Pedagogical Method & Study Guide

> **Motto:** Understand it. Build it. Run it. Inspect it. Measure it. Break it. Debug it. Rebuild it.

Operating systems cannot be learned by passively reading textbook diagrams or memorizing API signatures. The kernel is an active, stateful engine continuously mediating between your code and the hardware. To truly understand it, you must interact with it, force it into corner cases, observe its live state, and reconstruct its abstractions.

---

## 1. The Core Pedagogical Loop

Every phase in this curriculum follows the 11-step learning loop:

```text
       ┌───────────────┐
       │ 1. PROBLEM    │  Hardware reality or concurrency conflict
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 2. PREDICT    │  Formulate exact hypothesis before typing a command
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 3. BUILD      │  Implement minimal C code or Python simulation
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 4. RUN        │  Execute the program
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 5. INSPECT    │  Examine kernel tables via ps, lsof, /proc
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 6. TRACE      │  Inspect the boundary with strace
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 7. MEASURE    │  Quantify latency, context switches, or memory
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 8. EXPLAIN    │  Write the mechanism in your own words
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 9. BREAK      │  Intentionally induce race, deadlock, leak, or OOM
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 10. DEBUG     │  Diagnose using gdb, /proc, and error codes
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ 11. REBUILD   │  Re-implement from blank file without looking
       └───────────────┘
```

---

## 2. The Nine Study Habits of Systems Engineers

### 1. Predict Before Running
Before you run `fork()`, `open()`, or launch 50 threads, write down your prediction:
* *How many processes will exist?*
* *Will the shared variable be 2,000,000 or less?*
* *Will the file descriptor number be 3?*
If the machine's behavior contradicts your prediction, **do not proceed** until you have found which assumption was flawed.

### 2. Draw Process & Memory Diagrams
Never keep process trees or pointer graphs in your head. Draw:
* The process hierarchy: Parent PID -> Child PID.
* Virtual address layout: Stack growing down, Heap growing up.
* Descriptor table mapping: FD 0, 1, 2 -> Open File Object -> VFS Inode.

### 3. Inspect `/proc`
On Linux, the kernel maintains live telemetry in `/proc`. If you wonder what your process is doing:
```bash
cat /proc/<PID>/status
cat /proc/<PID>/maps
ls -l /proc/<PID>/fd
```

### 4. Use `strace` Relentlessly
When code fails, crashes, or hangs, do not guess. Run it under `strace`:
```bash
strace -f -tt -T ./my_binary
```
The exact failing syscall and its `errno` will be displayed on your terminal.

### 5. Compile Manually
Do not hide behind bloated build systems or IDE "play" buttons initially. Type:
```bash
gcc -Wall -Wextra -pthread -O2 prog.c -o prog
```
Notice what headers are required, what libraries are linked, and what warnings the compiler issues.

### 6. Break Programs Intentionally
A working program teaches you 20% of a concept. A broken program that you intentionally crashed and systematically diagnosed teaches you the remaining 80%.
* Remove the mutex lock.
* Comment out `wait()`.
* Close FD 1 and write to it.
* Dereference address `0x0`.

### 7. Debug Rather Than Restart Blindly
When an experiment deadlocks or throws `EADDRINUSE`, do not reboot or close your terminal. Inspect it:
* Who owns the lock? Use `gdb`.
* Who holds the port? Use `lsof -i :8080`.
* Which process is a zombie? Use `ps aux | grep 'Z'`.

### 8. Measure Before Optimizing
Never claim threads are faster than processes, or that `epoll` is faster than `select`, without measurement. Run the benchmarks provided in `benchmarks/`. Collect hard numbers on wall time, CPU time, and context switches.

### 9. Rebuild from Memory
Once you complete a capstone (like the Tiny Shell or the Event-Driven Server), close your editor, open an empty file, and re-implement the core loop from memory. If you can build it on a clean whiteboard, you own the concept forever.

---

## 3. What It Means to "Master" a Concept

A lesson is **never complete** simply because a code snippet compiled and exited with code 0.

You have mastered a topic only when you can answer:
1. What hardware condition or abstraction goal necessitated this OS mechanism?
2. What exact state transitions occur inside the kernel when it executes?
3. How do you inspect this state on a running production Linux server?
4. How does this mechanism fail under extreme load, and how do you diagnose the failure?
5. How does this mechanism empower real-world systems like Docker, PostgreSQL, Redis, and Kubernetes?
