# Curriculum Roadmap: 132 Phases to Operating Systems Mastery

> **Repository Motto:** Understand it. Build it. Run it. Inspect it. Measure it. Break it. Debug it. Rebuild it.

This roadmap details the complete 132-phase curriculum progression across systems programming, Linux kernel internals, diagnostic debugging, performance measurement, and container reconstruction.

---

## High-Level Curriculum Progression

```text
PART 01: FOUNDATIONS & SYSTEMS LAB           PART 08: I/O MODELS & EVENT LOOPS
  ├── Phase 00: Systems Laboratory             ├── Phase 66: Blocking I/O
  ├── Phase 01: What Is an Operating System?   ├── Phase 67: Non-Blocking I/O
  └── Phase 02: User Space & Kernel Space      ├── Phase 68: select()
                                               ├── Phase 69: poll()
PART 02: PROCESSES & LIFECYCLE                 ├── Phase 70: epoll
  ├── Phase 03: Programs vs Processes          ├── Phase 71: Event Loop
  ├── Phase 04: Process Memory Layout          └── Phase 72: Blocking vs Threads vs Event Loop
  ├── Phase 05: Process Creation
  ├── Phase 06: fork()                         PART 09: NETWORKING & SOCKETS
  ├── Phase 07: exec()                         ├── Phase 73: Sockets From First Principles
  └── Phase 08: wait() & Process Lifecycle     ├── Phase 74: TCP Server
                                               ├── Phase 75: Listening vs Connected Socket
PART 03: THE UNIX SHELL & DESCRIPTORS          ├── Phase 76: Ports & Processes
  ├── Phase 09: Build a Tiny Shell             └── Phase 77: UNIX Domain Sockets
  ├── Phase 10: Shell Redirection
  ├── Phase 11: Pipes                          PART 10: SIGNALS, CLOCKS & HARDWARE
  ├── Phase 12: File Descriptors               ├── Phase 78: Signals
  ├── Phase 13: System Calls                   ├── Phase 79: Graceful Shutdown
  └── Phase 14: strace Laboratory              ├── Phase 80: Timers & Clocks
                                               ├── Phase 81: Interrupts Conceptually
PART 04: CPU EXECUTION & SCHEDULING            ├── Phase 82: Exceptions & Traps
  ├── Phase 15: CPU Execution                  ├── Phase 83: Device Drivers
  ├── Phase 16: One CPU, Many Processes        ├── Phase 84: /proc
  ├── Phase 17: Scheduler Simulator            └── Phase 85: /sys
  ├── Phase 18: Scheduling Tradeoffs
  ├── Phase 19: Linux Scheduling (CFS)         PART 11: RESOURCE LIMITS & PROFILING
  └── Phase 20: Context Switching              ├── Phase 86: Resource Limits
                                               ├── Phase 87: File Descriptor Exhaustion
PART 05: CONCURRENCY, THREADS & SYNCHRONIZATION ├── Phase 88: CPU Saturation
  ├── Phase 21: Threads From First Principles  ├── Phase 89: Load Average
  ├── Phase 22: Process vs Thread              ├── Phase 90: Memory Pressure
  ├── Phase 23: Race Conditions                ├── Phase 91: I/O Performance
  ├── Phase 24: Atomicity                      ├── Phase 92: perf Introduction
  ├── Phase 25: Mutexes                        ├── Phase 93: CPU Profiling
  ├── Phase 26: Semaphores                     └── Phase 94: strace Performance Debugging
  ├── Phase 27: Condition Variables
  ├── Phase 28: Producer Consumer              PART 12: ISOLATION & CONTAINERS
  ├── Phase 29: Deadlocks                      ├── Phase 95: Namespaces From First Principles
  ├── Phase 30: Deadlock Prevention            ├── Phase 96: PID Namespace
  ├── Phase 31: Livelock & Starvation          ├── Phase 97: Mount Namespace
  └── Phase 32: Concurrency Challenge Labs     ├── Phase 98: Network Namespace
                                               ├── Phase 99: cgroups From First Principles
PART 06: VIRTUAL MEMORY & PAGING               ├── Phase 100: cgroups Practical Lab
  ├── Phase 33: Memory Before Virtual Memory   ├── Phase 101: Containers From OS Primitives
  ├── Phase 34: Address Spaces                 ├── Phase 102: Tiny Container Experiment
  ├── Phase 35: Address Translation            ├── Phase 103: Capabilities
  ├── Phase 36: Paging                         └── Phase 104: VMs vs Containers
  ├── Phase 37: Page Tables
  ├── Phase 38: TLB                            PART 13: INITIALIZATION, SECURITY & IPC
  ├── Phase 39: Page Faults                    ├── Phase 105: Boot Process Overview
  ├── Phase 40: Demand Paging                  ├── Phase 106: init & PID 1
  ├── Phase 41: Virtual Memory & Disk          ├── Phase 107: systemd Concepts
  ├── Phase 42: Page Replacement Algorithms    ├── Phase 108: Permissions
  ├── Phase 43: Thrashing                      ├── Phase 109: Users, Groups & Process Identity
  ├── Phase 44: mmap()                         ├── Phase 110: Process Security Boundaries
  ├── Phase 45: Copy-on-Write                  ├── Phase 111: IPC Overview
  ├── Phase 46: malloc and Heap                ├── Phase 112: Shared Memory
  ├── Phase 47: Memory Leaks                   ├── Phase 113: IPC Comparison Project
  ├── Phase 48: The Stack                      ├── Phase 114: Cache Hierarchy Awareness
  ├── Phase 49: Segmentation Faults            ├── Phase 115: Locality
  └── Phase 50: gdb Fundamentals               ├── Phase 116: False Sharing
                                               └── Phase 117: Practical Performance Methodology
PART 07: FILESYSTEMS & STORAGE
  ├── Phase 51: Files From First Principles    PART 14: DEBUGGING, CAPSTONES & REAL SYSTEMS
  ├── Phase 52: open/read/write/close          ├── Phase 118: Broken Systems Labs (25 Incidents)
  ├── Phase 53: File Metadata                  ├── Phase 119: Capstone 1 - Expanded Unix Shell
  ├── Phase 54: Inodes                         ├── Phase 120: Capstone 2 - MLFQ Scheduler Simulator
  ├── Phase 55: Hard Links & Symlinks          ├── Phase 121: Capstone 3 - Virtual Memory Simulator
  ├── Phase 56: Directories                    ├── Phase 122: Capstone 4 - Tiny Filesystem (TinyFS)
  ├── Phase 57: Build a Tiny Filesystem        ├── Phase 123: Capstone 5 - Event-Driven HTTP Server
  ├── Phase 58: Disk Blocks                    ├── Phase 124: Capstone 6 - Tiny Container Sandbox
  ├── Phase 59: Filesystem Caching             ├── Phase 125: OS and Databases (PostgreSQL / InnoDB)
  ├── Phase 60: Buffered I/O                   ├── Phase 126: OS and Kafka (Sequential I/O & Page Cache)
  ├── Phase 61: fsync & Durability             ├── Phase 127: OS and Redis (Event Loop & Fork COW)
  ├── Phase 62: Crash Consistency              ├── Phase 128: OS and Docker (Namespaces & Cgroups)
  ├── Phase 63: Journaling Filesystems         ├── Phase 129: OS and Kubernetes (Kubelet & CGroups)
  ├── Phase 64: Disk Scheduling Concepts       ├── Phase 130: OS in System Design (11 Dimensions)
  └── Phase 65: The I/O Stack                  └── Phase 131: Final Mental Model (Complete Trace)
```

---

## Detailed 132-Phase Directory Map

| Phase | Directory | Title | Core Focus |
| :---: | :--- | :--- | :--- |
| **00** | `phases/00-systems-laboratory` | Systems Laboratory | Terminal, processes, PIDs, exit codes, environment inspection |
| **01** | `phases/01-what-is-an-operating-system` | What Is an Operating System? | Resource management, abstraction layers, hardware protection |
| **02** | `phases/02-user-space-and-kernel-space` | User Space and Kernel Space | Ring 0 vs Ring 3 privilege, hardware execution modes |
| **03** | `phases/03-programs-vs-processes` | Programs vs Processes | Passive executable image vs active memory instance, PCB |
| **04** | `phases/04-process-memory-layout` | Process Memory Layout | Text, data, BSS, heap, stack segments, ASLR |
| **05** | `phases/05-process-creation` | Process Creation | Process tree hierarchy, ancestor chains, parent-child |
| **06** | `phases/06-fork-deep-dive` | fork() Deep Dive | Address space cloning, Copy-on-Write, return values |
| **07** | `phases/07-exec-deep-dive` | exec() Deep Dive | Execve, program image replacement, argv, envp |
| **08** | `phases/08-wait-and-lifecycle` | wait() and Process Lifecycle | Exit status codes, WIFEXITED, zombies, orphans |
| **09** | `phases/09-build-a-tiny-shell` | Build a Tiny Shell | Command parsing, REPL, fork, exec, wait coordination |
| **10** | `phases/10-shell-redirection` | Shell Redirection | dup2, standard streams, descriptor table manipulation |
| **11** | `phases/11-pipes` | Pipes | Unidirectional in-memory kernel ring buffers, SIGPIPE |
| **12** | `phases/12-file-descriptors` | File Descriptors | Per-process FD table, open-file description, vnodes |
| **13** | `phases/13-system-calls` | System Calls | Hardware syscall instruction, registers, errno conventions |
| **14** | `phases/14-strace-laboratory` | strace Laboratory | Syscall tracing, filtering, latency profiling |
| **15** | `phases/15-cpu-execution` | CPU Execution | Fetch-decode-execute cycle, PC/RIP, registers, stack pointer |
| **16** | `phases/16-one-cpu-many-processes` | One CPU, Many Processes | Time-sharing, timer interrupts, quantum multiplexing |
| **17** | `phases/17-scheduler-simulator` | Scheduler Simulator | FCFS, SJF, Round Robin simulation, Gantt charts |
| **18** | `phases/18-scheduling-tradeoffs` | Scheduling Tradeoffs | Interactive latency vs batch throughput, convoy effect |
| **19** | `phases/19-linux-scheduling` | Linux Scheduling | Completely Fair Scheduler (CFS), vruntime, nice values |
| **20** | `phases/20-context-switching` | Context Switching | Hardware register save/restore, pipeline flushes, overhead |
| **21** | `phases/21-threads-from-first-principles` | Threads From First Principles | Shared address space, private stacks, TCB, pthreads |
| **22** | `phases/22-process-vs-thread` | Process vs Thread | Fault isolation vs memory sharing performance tradeoffs |
| **23** | `phases/23-race-conditions` | Race Conditions | Shared mutable state, non-deterministic scheduling |
| **24** | `phases/24-atomicity` | Atomicity | Load-modify-store instruction cycles, hardware atomics |
| **25** | `phases/25-mutexes` | Mutexes | Mutual exclusion, critical sections, futex mechanics |
| **26** | `phases/26-semaphores` | Semaphores | Counting semaphores, resource pool tracking |
| **27** | `phases/27-condition-variables` | Condition Variables | Sleeping until state change, spurious wakeups, while loops |
| **28** | `phases/28-producer-consumer` | Producer Consumer | Bounded FIFO queue, backpressure, empty/full conditions |
| **29** | `phases/29-deadlocks` | Deadlocks | Circular lock acquisition, Coffman conditions |
| **30** | `phases/30-deadlock-prevention` | Deadlock Prevention | Total lock ordering, trylock with backoff, timeouts |
| **31** | `phases/31-livelock-and-starvation` | Livelock and Starvation | High-CPU lockstep backoff, unfair contention, starvation |
| **32** | `phases/32-concurrency-challenge-labs` | Concurrency Challenge Labs | ThreadSanitizer, stress testing, concurrency diagnostics |
| **33** | `phases/33-memory-before-virtual-memory` | Memory Before Virtual Memory | Base and bounds registers, physical fragmentation risks |
| **34** | `phases/34-address-spaces` | Address Spaces | Virtual address isolation, pointer independence |
| **35** | `phases/35-address-translation` | Address Translation | VPN to frame mapping, page offset calculations |
| **36** | `phases/36-paging` | Paging | Fixed 4KB pages vs variable segments, internal fragmentation |
| **37** | `phases/37-page-tables` | Page Tables | Multi-level hierarchical page tables, PML4, overhead |
| **38** | `phases/38-tlb` | TLB | Hardware translation cache, hit ratios, miss penalty |
| **39** | `phases/39-page-faults` | Page Faults | CPU exceptions, minor page faults vs major disk page faults |
| **40** | `phases/40-demand-paging` | Demand Paging | Lazy frame loading on first access, startup acceleration |
| **41** | `phases/41-virtual-memory-and-disk` | Virtual Memory and Disk | Swap space, cold page eviction, memory pressure |
| **42** | `phases/42-page-replacement-algorithms` | Page Replacement Algorithms | FIFO, LRU, Clock (Second Chance), Belady's Anomaly |
| **43** | `phases/43-thrashing` | Thrashing | Working set exceeding RAM, swap storms, throughput collapse |
| **44** | `phases/44-mmap-deep-dive` | mmap() Deep Dive | File-backed memory mapping, anonymous allocation, msync |
| **45** | `phases/45-copy-on-write` | Copy-on-Write (COW) | Read-only page sharing, instant memory cloning |
| **46** | `phases/46-malloc-and-heap` | malloc and Heap | Userspace allocator metadata, chunk headers, brk/mmap |
| **47** | `phases/47-memory-leaks` | Memory Leaks | Unreachable heap allocations, Valgrind leak detection |
| **48** | `phases/48-the-stack` | The Stack | Stack frames, RSP/RBP registers, stack overflow traps |
| **49** | `phases/49-segmentation-faults` | Segmentation Faults | Hardware MMU violation, unmapped pages, SIGSEGV |
| **50** | `phases/50-gdb-fundamentals` | gdb Fundamentals | Breakpoints, stack backtraces, register inspection |
| **51** | `phases/51-files-from-first-principles` | Files From First Principles | Naming, persistent byte streams, metadata contracts |
| **52** | `phases/52-open-read-write-close` | open/read/write/close | POSIX descriptor lifecycle, cursor repositioning |
| **53** | `phases/53-file-metadata` | File Metadata | Inodes, permissions, size, timestamps, stat struct |
| **54** | `phases/54-inodes` | Inodes | True identity of files, direct and indirect block pointers |
| **55** | `phases/55-hard-links-and-symbolic-links` | Hard Links and Symbolic Links | Reference counting, directory entries vs dangling symlinks |
| **56** | `phases/56-directories` | Directories | Mapping filenames to inode numbers, '.' and '..' entries |
| **57** | `phases/57-build-a-tiny-filesystem` | Build a Tiny Filesystem | Superblock, bitmaps, inode tables on virtual block files |
| **58** | `phases/58-disk-blocks` | Disk Blocks | Block layer, sector alignment, block device interfaces |
| **59** | `phases/59-filesystem-caching` | Filesystem Caching | Kernel page cache, buffer hit ratios, drop_caches |
| **60** | `phases/60-buffered-io` | Buffered I/O | Userspace stdio buffering vs raw unbuffered write syscalls |
| **61** | `phases/61-fsync-and-durability` | fsync and Durability | Flushing dirty pages to physical non-volatile media |
| **62** | `phases/62-crash-consistency` | Crash Consistency | Multi-block update consistency, partial write corruption |
| **63** | `phases/63-journaling-filesystems` | Journaling Filesystems | Write-Ahead Logging (WAL), transaction commits, recovery |
| **64** | `phases/64-disk-scheduling-concepts` | Disk Scheduling Concepts | Mechanical seek times vs SSD block erase cycles |
| **65** | `phases/65-the-io-stack` | The I/O Stack | VFS to page cache, block layer, scheduler, device driver |
| **66** | `phases/66-blocking-io` | Blocking I/O | Head-of-line blocking, sleeping threads in read() |
| **67** | `phases/67-non-blocking-io` | Non-Blocking I/O | O_NONBLOCK, EAGAIN, asynchronous readiness polling |
| **68** | `phases/68-select-deep-dive` | select() Deep Dive | Synchronous I/O multiplexing, fd_set bitmasks, limits |
| **69** | `phases/69-poll-deep-dive` | poll() Deep Dive | struct pollfd arrays, eliminating 1024 descriptor cap |
| **70** | `phases/70-epoll-deep-dive` | epoll Deep Dive | Kernel ready list, red-black tree, $O(1)$ event scalability |
| **71** | `phases/71-the-event-loop` | The Event Loop | Reactor pattern, single-threaded non-blocking dispatch |
| **72** | `phases/72-blocking-vs-threads-vs-event-loop` | Blocking vs Threads vs Event Loop | Performance, memory, and architectural concurrency matrix |
| **73** | `phases/73-sockets-from-first-principles` | Sockets From First Principles | Network endpoints, kernel queues, address families |
| **74** | `phases/74-tcp-server` | TCP Server | Socket, bind, listen, accept, 3-way handshake states |
| **75** | `phases/75-listening-socket-vs-connected-socket` | Listening vs Connected Socket | Passive listen queues vs active 4-tuple connections |
| **76** | `phases/76-ports-and-processes` | Ports and Processes | Port collisions, EADDRINUSE, SO_REUSEADDR |
| **77** | `phases/77-unix-domain-sockets` | UNIX Domain Sockets | Local zero-copy IPC, SCM_RIGHTS descriptor passing |
| **78** | `phases/78-signals` | Signals | Asynchronous kernel notifications, sigaction, signal masks |
| **79** | `phases/79-graceful-shutdown` | Graceful Shutdown | SIGTERM request draining vs forceful SIGKILL deadlines |
| **80** | `phases/80-timers-and-clocks` | Timers and Clocks | CLOCK_REALTIME vs CLOCK_MONOTONIC, drift immunity |
| **81** | `phases/81-interrupts-conceptually` | Interrupts Conceptually | Hardware electrical IRQs, Interrupt Service Routines |
| **82** | `phases/82-exceptions-and-traps` | Exceptions and Traps | Hardware faults, software traps, syscall vectoring |
| **83** | `phases/83-device-drivers` | Device Drivers | Translating abstract VFS requests to hardware buses |
| **84** | `phases/84-procfs-deep-dive` | /proc Deep Dive | Live kernel state exported as virtual plain-text files |
| **85** | `phases/85-sysfs-deep-dive` | /sys Deep Dive | Unified hardware topology and kernel object hierarchy |
| **86** | `phases/86-resource-limits` | Resource Limits | ulimit, prlimit, RLIMIT_NOFILE, RLIMIT_AS sandboxes |
| **87** | `phases/87-file-descriptor-exhaustion` | File Descriptor Exhaustion | EMFILE failure modes and connection drop incidents |
| **88** | `phases/88-cpu-saturation` | CPU Saturation | Distinguishing user, system, nice, idle, and I/O wait |
| **89** | `phases/89-load-average` | Load Average | Exponentially decaying average of runnable and D-state tasks |
| **90** | `phases/90-memory-pressure` | Memory Pressure | kswapd, page reclaim watermarks, OOM score tuning |
| **91** | `phases/91-io-performance` | I/O Performance | Storage throughput, IOPS, latency, queue depth metrics |
| **92** | `phases/92-perf-introduction` | perf Introduction | Hardware performance counters, instruction sampling |
| **93** | `phases/93-cpu-profiling` | CPU Profiling | Function hotspot detection, call trees, flamegraphs |
| **94** | `phases/94-strace-performance-debugging` | strace Performance Debugging | Syscall frequency analysis, kernel boundary tax |
| **95** | `phases/95-namespaces-from-first-principles` | Namespaces From First Principles | Resource virtualization, unshare, clone isolation |
| **96** | `phases/96-pid-namespace` | PID Namespace | Private process trees, PID 1 inside container sandboxes |
| **97** | `phases/97-mount-namespace` | Mount Namespace | Isolated mount tables, pivot_root, rootfs isolation |
| **98** | `phases/98-network-namespace` | Network Namespace | Private network stacks, veth interfaces, virtual bridges |
| **99** | `phases/99-cgroups-from-first-principles` | cgroups From First Principles | Unified cgroups v2 resource metering and limits |
| **100** | `phases/100-cgroups-practical-lab` | cgroups Practical Lab | Configuring memory.max and cpu.max resource ceilings |
| **101** | `phases/101-containers-from-os-primitives` | Containers From OS Primitives | Reconstructing containers from namespaces, cgroups, chroot |
| **102** | `phases/102-build-a-tiny-container-experiment` | Tiny Container Experiment | C launcher invoking clone() with namespace flags |
| **103** | `phases/103-capabilities` | Capabilities | Decomposing monolithic root power into fine-grained units |
| **104** | `phases/104-virtual-machines-vs-containers` | VMs vs Containers | Hardware hypervisors vs shared host kernel isolation |
| **105** | `phases/105-boot-process-overview` | Boot Process Overview | Firmware to bootloader, kernel, initramfs, and PID 1 |
| **106** | `phases/106-init-and-pid-1` | init and PID 1 | Special responsibilities, zombie reaping, kernel panic on death |
| **107** | `phases/107-systemd-concepts` | systemd Concepts | Service units, socket activation, dependency graphs |
| **108** | `phases/108-permissions` | Permissions | POSIX user, group, other mode bits, setuid, setgid |
| **109** | `phases/109-users-groups-and-process-identity` | Users, Groups & Process Identity | RUID, EUID, saved UID, credential verification |
| **110** | `phases/110-process-security-boundaries` | Process Security Boundaries | Inter-process memory isolation, ptrace Yama LSM |
| **111** | `phases/111-ipc-overview` | IPC Overview | Tradeoffs across pipes, sockets, message queues, shared memory |
| **112** | `phases/112-shared-memory` | Shared Memory | Zero-copy POSIX shared memory, synchronization needs |
| **113** | `phases/113-ipc-comparison-project` | IPC Comparison Project | Benchmarking throughput and latency across IPC mechanisms |
| **114** | `phases/114-cache-hierarchy-awareness` | Cache Hierarchy Awareness | CPU memory pyramid, L1/L2/L3 latencies, cache lines |
| **115** | `phases/115-locality` | Locality | Spatial vs temporal locality, cache prefetching |
| **116** | `phases/116-false-sharing` | False Sharing | Cache line bouncing across CPU cores, 64-byte padding |
| **117** | `phases/117-practical-performance-methodology` | Practical Performance Methodology | USE method, measurement baselines, hypothesis testing |
| **118** | `phases/118-broken-systems-labs` | Broken Systems Labs | 25 real-world incident debugging scenarios |
| **119** | `phases/119-capstone-tiny-shell` | Capstone 1: Expanded Unix Shell | Final shell with pipes, redirection, signals, builtins |
| **120** | `phases/120-capstone-scheduler-simulator` | Capstone 2: Scheduler Simulator | Interactive MLFQ scheduler with Gantt visualization |
| **121** | `phases/121-capstone-vm-simulator` | Capstone 3: Virtual Memory Simulator | Two-level page tables, TLB, Clock page replacement |
| **122** | `phases/122-capstone-tiny-filesystem` | Capstone 4: Tiny Filesystem | Superblock, inodes, bitmaps, blocks on virtual disk |
| **123** | `phases/123-capstone-event-http-server` | Capstone 5: Event-Driven HTTP Server | High-performance server comparing 3 concurrency models |
| **124** | `phases/124-capstone-container-sandbox` | Capstone 6: Tiny Container Sandbox | Linux namespaces, cgroups v2, capability dropping |
| **125** | `phases/125-os-and-databases` | OS and Databases | PostgreSQL / MySQL buffer pools, page cache, WAL, fsync |
| **126** | `phases/126-os-and-kafka` | OS and Kafka | Sequential append-only I/O, page cache, sendfile zero-copy |
| **127** | `phases/127-os-and-redis` | OS and Redis | Single-threaded event loop, fork COW background snapshots |
| **128** | `phases/128-os-and-docker` | OS and Docker | Namespaces, cgroups, overlayfs, veth pair networking |
| **129** | `phases/129-os-and-kubernetes` | OS and Kubernetes | Pod network namespaces, pause container, cgroup limits |
| **130** | `phases/130-os-in-system-design` | OS in System Design | 11-dimension evaluation framework for distributed systems |
| **131** | `phases/131-final-mental-model` | Final Mental Model | Complete trace from curl command down to physical silicon |
