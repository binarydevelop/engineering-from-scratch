# Operating Systems From Scratch

> **Understand it. Build it. Run it. Inspect it. Measure it. Break it. Debug it. Rebuild it.**

A comprehensive, first-principles curriculum that teaches operating systems deeply through systems programming in C, Python simulations, Linux kernel inspection, hardware performance measurement, failure injection, debugging, and the progressive reconstruction of foundational OS mechanisms.

---

## The Core Philosophy & Purpose

Most software engineers treat the layer between their application code and physical hardware as an impenetrable black box:

```text
Python / C / Java / Go Code
      │
      ▼
   [ MAGIC ]
      │
      ▼
   Hardware
```

This repository dismantles the magic. By the time you complete this course, you will be able to trace and reason through the complete physical and logical journey of computation:

```text
Python / C / Go Application
            │
            ▼
     Userspace Process (Ring 3)
            │
            ▼
     C Runtime Library (glibc / musl)
            │
            ▼
     System Call Interface (syscall instruction)
            │
            ▼
     Operating System Kernel (Ring 0)
     ├── CPU Scheduler (CFS / MLFQ / Context Switching)
     ├── Virtual Memory Subsystem (MMU / Page Tables / TLB / Page Cache)
     ├── Virtual File System (Inodes / Dentries / Journal / Block Layer)
     └── Network Stack (Sockets / TCP / UDP / Packet Queues)
            │
            ▼
     Device Drivers (NVMe, SATA, Ethernet, GPU)
            │
            ▼
     Physical Hardware (CPU Registers, L1/L2/L3 Caches, RAM, Silicon Flash, NIC)
```

You will understand **why** processes, threads, file descriptors, sockets, virtual memory, page tables, system calls, context switches, schedulers, mutexes, filesystems, buffers, interrupts, and signals exist—not as vocabulary definitions, but as inevitable engineering solutions to physical hardware realities and concurrency constraints.

---

## The Four Pillars

1. **Operating System Fundamentals:** Paging, TLB, multi-level page tables, demand paging, MLFQ and CFS scheduling, Coffman deadlock conditions, VFS, crash consistency, Write-Ahead Logging.
2. **Practical Linux Systems:** Hands-on mastery of Linux diagnostic and telemetry facilities: `/proc`, `/sys`, `strace`, `lsof`, `ss`, `free`, `vmstat`, `pidstat`, `pmap`, `perf`, `gdb`.
3. **Systems Programming in C:** Writing robust, warning-clean POSIX code using `fork`, `execvp`, `waitpid`, `pipe`, `dup2`, `mmap`, `pthreads`, `mutexes`, `condition variables`, `semaphores`, and BSD sockets.
4. **Production Systems Reality:** Tracing the exact low-level primitives underlying **Docker** (namespaces + cgroups), **PostgreSQL** (shared memory + fsync + WAL), **Redis** (event loops + fork COW), and **Kafka** (sequential I/O + page cache + zero-copy `sendfile`).

---

## Curriculum Progression

```text
   Programs
      ↓
   Processes & Memory Layout
      ↓
   System Calls & strace
      ↓
   CPU Scheduling & Context Switching
      ↓
   Threads & Concurrency
      ↓
   Synchronization & Deadlocks
      ↓
   Virtual Memory & Paging
      ↓
   Filesystems & Page Cache
      ↓
   I/O Multiplexing & Event Loops
      ↓
   Networking & Sockets
      ↓
   Signals, Clocks & Drivers
      ↓
   Kernel Interfaces (/proc, /sys)
      ↓
   Resource Limits & Profiling
      ↓
   Namespaces & Control Groups
      ↓
   Containers & Sandboxing
      ↓
   Real-World Systems (Databases, Kafka, Redis, Docker, Kubernetes)
```

---

## Curriculum Structure at a Glance

| Metric | Scope & Count | Details |
| :--- | :---: | :--- |
| **Total Phases** | **132 Phases** | Phase 00 (Systems Laboratory) through Phase 131 (Final Mental Model) |
| **Thematic Modules** | **14 Parts** | Spanning Processes, Scheduling, Memory, Filesystems, I/O, Sockets, Containers |
| **Practical Exercises** | **160 Exercises** | Organized into 9 tracks with separate solutions in `solutions/exercises/` |
| **Broken Systems Labs** | **25 Incidents** | Real-world failure scenarios (deadlocks, leaks, thrashing, saturation) |
| **Major Capstone Projects** | **6 Projects** | Complete implementations in `projects/` with source, Makefiles, and tests |
| **Algorithmic Simulators** | **6 Simulators** | Interactive Python models of Schedulers, Paging, TLB, Cache, and Journaling |
| **Systems Benchmarks** | **5 Benchmarks** | Nanosecond-precision C benchmarks for context switches, cache locality, buffering |

---

## The 6 Major Capstone Projects

Located in `projects/`:

1. **Capstone 1: Expanded Unix Shell (`projects/01-tiny-shell/`):**  
   Interactive REPL, command argument parsing, `fork()`, `execvp()`, `waitpid()`, pipelines (`cmd1 | cmd2`), input/output redirection (`<`, `>`, `>>`), background execution (`&`), built-ins (`cd`, `pwd`, `exit`), and signal interception (`SIGINT`).
2. **Capstone 2: User-Space Thread Scheduler Simulator (`projects/02-scheduler-simulator/`):**  
   Multi-Level Feedback Queue (MLFQ) scheduler with 3 priority queues, dynamic time-slice demotion, starvation-prevention priority boost, I/O burst simulation, and text-based Gantt charts.
3. **Capstone 3: Virtual Memory & Page Eviction Simulator (`projects/03-vm-simulator/`):**  
   Two-level hierarchical page tables, Translation Lookaside Buffer (TLB) with LRU eviction, demand paging fault handler, and Clock (Second Chance) page replacement with dirty page writeback.
4. **Capstone 4: Tiny Educational Filesystem (`projects/04-tiny-fs/`):**  
   Complete Unix-like filesystem on a raw virtual block device file: Superblock, Inode table, Free Block Bitmap, Inode Bitmap, Directory entry arrays, `format`, `create`, `write`, `read`, `ls`, and `delete`.
5. **Capstone 5: High-Performance HTTP Server (`projects/05-event-http-server/`):**  
   Progressive implementation comparing 3 server architectures: (A) Sequential single-threaded blocking, (B) Multi-threaded worker pool with bounded work queue, and (C) Non-blocking event-driven loop (`select`/`poll`/`epoll`). Includes concurrent benchmarking client.
6. **Capstone 6: Tiny Container Sandbox (`projects/06-container-sandbox/`):**  
   Reconstructs Docker from raw Linux primitives: PID namespaces (`CLONE_NEWPID`), UTS hostnames (`CLONE_NEWUTS`), Mount namespaces (`CLONE_NEWNS`), Network isolation (`CLONE_NEWNET`), cgroups v2 memory/CPU limits, and capability dropping.

---

## The 25 Broken Systems Labs

Located in `labs/broken-systems/` (with separate verified solutions in `solutions/broken-systems/`):

* **Lab 01:** CPU core saturation (tight spin loop without yielding)
* **Lab 02:** Memory leak (continuous heap growth exhausting RAM)
* **Lab 03:** Deadlock (out-of-order 2-mutex circular wait)
* **Lab 04:** Zombie process (unreaped child lingering in process table)
* **Lab 05:** File descriptor leak (`EMFILE: Too many open files`)
* **Lab 06:** Port collision (`EADDRINUSE: Address already in use`)
* **Lab 07:** Permission denied (`EACCES` on read-only file mode bits)
* **Lab 08:** Full disk & partial write handling (`ENOSPC`)
* **Lab 09:** Unhandled hardware arithmetic trap (`SIGFPE`)
* **Lab 10:** Segmentation fault (NULL pointer dereference)
* **Lab 11:** Blocked syscall (unresponsive read on pipe with no writers)
* **Lab 12:** Network timeout (connect stalling on unreachable IP)
* **Lab 13:** Unbuffered I/O bottleneck (50,000 1-byte syscalls)
* **Lab 14:** Orphan process (abandoned child reparented to init)
* **Lab 15:** Race condition counter (unsynchronized multi-thread increments)
* **Lab 16:** Thread starvation (greedy lock holder starving workers)
* **Lab 17:** Livelock (two workers politely yielding in lockstep)
* **Lab 18:** Stack overflow (unbounded recursion hitting guard page)
* **Lab 19:** Use-after-free (dangling pointer heap corruption)
* **Lab 20:** Zombie apocalypse (fork loop without SIGCHLD reaping)
* **Lab 21:** Broken pipe (`SIGPIPE` on write to closed socket)
* **Lab 22:** PATH lookup failure (`execvp ENOENT`)
* **Lab 23:** Priority inversion concept & priority inheritance mutexes
* **Lab 24:** TCP listen backlog queue overflow (dropped SYN bursts)
* **Lab 25:** Memory thrashing (working set exceeding physical frame cache)

---

## Pedagogical Methodology: The 11-Step Learning Loop

Every phase follows a disciplined loop designed to eradicate cargo-cult programming:

```text
1. Problem   ──► Hardware limitation or concurrency hazard
2. Predict   ──► Formulate exact hypothesis before typing commands
3. Build     ──► Implement minimal C code or simulation
4. Run       ──► Execute on the machine
5. Inspect   ──► View internal kernel tables via ps, lsof, /proc
6. Trace     ──► Inspect syscall boundary via strace
7. Measure   ──► Quantify latency, context switches, or RSS memory
8. Explain   ──► Articulate the mechanism in your own words
9. Break     ──► Intentionally trigger edge case or crash
10. Debug    ──► Diagnose using gdb, /proc, and error codes
11. Rebuild  ──► Re-implement from memory on a blank whiteboard
```

---

## Platform Compatibility

| Host Operating System | Compatibility Status | Recommended Workflow |
| :--- | :---: | :--- |
| **Native Linux (Ubuntu 22.04 / 24.04, Debian, Fedora)** | **Tier 1 (Native)** | All 132 phases run directly on host. |
| **Windows 11 WSL2 (Ubuntu kernel)** | **Tier 1 (Native)** | Full syscall tracing, `/proc`, and cgroups v2 supported. |
| **macOS (Apple Silicon & Intel)** | **Tier 2 (Hybrid)** | All POSIX C programming, threads, sockets, benchmarks, and Python simulations run natively. Linux-specific phases (epoll, namespaces, cgroups) run inside the provided Docker or Lima VM sandbox. |

See [docs/platform-setup.md](file:///Users/tushar/Desktop/private/repos/operating-systems-from-scratch/docs/platform-setup.md) for full setup instructions.

---

## Quickstart: Your First Commands

### 1. Check Your Environment
```bash
./scripts/check-environment.sh
```

### 2. Compile All Benchmarks, Capstones, and Solutions
```bash
make build
```

### 3. Run the Automated Test Suite
```bash
make test
```

### 4. Begin Phase 00 (Systems Laboratory)
```bash
cd phases/00-systems-laboratory
cat docs/en.md
./experiments/run-experiment.sh
```

---

## License & Safety Notice

Always adhere to the safety containment guidelines in [SAFETY.md](file:///Users/tushar/Desktop/private/repos/operating-systems-from-scratch/SAFETY.md). Never run unbounded allocation loops or privileged mount commands on primary host workstations without isolation.

---

> The operating system is no longer an invisible layer between our programs and the machine.
>
> We started with ordinary programs, turned them into processes, followed their system calls into the kernel, scheduled them on CPUs, shared work across threads, translated virtual memory into physical memory, stored bytes through filesystems, communicated through sockets, and finally reconstructed containers from the isolation and resource-control primitives provided by Linux.
>
> Now when a server becomes slow, a database performs I/O, a container receives a memory limit, or thousands of network connections arrive at once, we can reason about what the machine is actually doing underneath.
