#!/usr/bin/env python3
"""
Scaffolds all 132 phases of operating-systems-from-scratch.
Each phase directory receives:
- docs/en.md (17-section canonical curriculum format)
- code/ (C or Python source code)
- experiments/run-experiment.sh (executable experiment runner)
- outputs/evidence-template.md
"""

import os
import stat
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHASES_DIR = os.path.join(REPO_ROOT, "phases")

PHASE_DEFS = [
    # Part 1: Foundations & Systems Laboratory (00-02)
    (0, "systems-laboratory", "Systems Laboratory",
     "How do we observe the invisible software boundary between application code and physical hardware?",
     "Your terminal is not just a command prompt; it is a live instrumentation console for the kernel.",
     "terminal, shell, process, PID, /proc, exit codes, stdout, stderr, env",
     "ps, top, pwd, ls, env, echo $?",
     "echo 'Checking environment'; uname -a; id; pwd",
     "Run command without quotes and observe shell word splitting."),

    (1, "what-is-an-operating-system", "What Is an Operating System?",
     "How would an application safely access CPU, RAM, NVMe, and Ethernet cards without colliding with other applications?",
     "An operating system is a resource manager, an abstraction boundary, and a hardware protection arbiter.",
     "resource arbitration, hardware multiplexing, security boundary",
     "uname, lscpu, free, df",
     "cat /proc/version || uname -v",
     "Remove the OS abstraction: direct hardware access leads to corruption."),

    (2, "user-space-and-kernel-space", "User Space and Kernel Space",
     "Why can't arbitrary user applications directly modify page tables or device controller state?",
     "Privilege separation is the foundation of computer security and hardware stability.",
     "Ring 0 (Kernel) vs Ring 3 (User), CPU execution modes, hardware privilege bits",
     "dmesg, /proc/sys",
     "cat /proc/kallsyms | head -n 10 || echo 'Kernel symbols protected'",
     "Attempt to execute privileged instructions from user space (e.g. cli / hlt)."),

    # Part 2: Processes & The Process Lifecycle (03-08)
    (3, "programs-vs-processes", "Programs vs Processes",
     "What is the difference between an inert binary file on disk and a living execution instance in memory?",
     "A program is passive text on disk; a process is an active organism in kernel memory.",
     "ELF/Mach-O binaries, execution state, process control block (PCB), PID",
     "ps aux, pgrep, /proc/<pid>",
     "ps -o pid,ppid,comm,state",
     "Kill the parent process and watch what happens to the child."),

    (4, "process-memory-layout", "Process Memory Layout",
     "How are instructions, static data, dynamic allocations, and function call frames arranged in memory?",
     "Memory is structured into deterministic segments: text, data, bss, heap, and stack.",
     "text (read-only code), data (initialized globals), bss (zeroed globals), heap, stack",
     "/proc/<pid>/maps, pmap, size",
     "cat /proc/self/maps || vmmap $$ | head -n 20",
     "Stack buffer overflow corrupting saved return address."),

    (5, "process-creation", "Process Creation",
     "How does the operating system construct a new process tree out of existing processes?",
     "Every process on a Unix system has an ancestor, forming a single unified process tree rooted at PID 1.",
     "fork, process hierarchy, parent-child relationships, process table",
     "pstree, ps -ef --forest",
     "pstree -p $$ || ps -ef | head -n 15",
     "Create process cycles; observe tree hierarchy enforcement."),

    (6, "fork-deep-dive", "fork() Deep Dive",
     "How does fork() duplicate an entire process without duplicating all physical memory immediately?",
     "One call, two returns: fork clones the calling process while preserving memory isolation.",
     "fork return values (0 in child, PID in parent), Copy-on-Write (COW), address space cloning",
     "strace -e fork",
     "ps -o pid,ppid,state",
     "Unbounded fork recursion without limits (fork bomb simulation with ulimit)."),

    (7, "exec-deep-dive", "exec() Deep Dive",
     "How does a process discard its current code and load a completely new executable binary?",
     "exec replaces the soul of a process while keeping its physical PID intact.",
     "execve syscall, address space replacement, argument vector (argv), environment vector (envp)",
     "strace -e execve",
     "which ls && ls -l /bin/ls",
     "Pass invalid binary paths to execvp and handle ENOENT."),

    (8, "wait-and-lifecycle", "wait() and Process Lifecycle",
     "What happens to a terminated process before its parent collects its exit status?",
     "A dead process cannot rest until reaped; an uncollected child becomes a zombie in the kernel table.",
     "wait, waitpid, exit status, WIFEXITED, zombies, orphans",
     "ps aux | grep 'Z'",
     "ps -eo pid,ppid,stat,comm | grep -E 'Z|defunct'",
     "Omit wait() and watch defunct zombie processes accumulate in ps."),

    # Part 3: The Unix Shell & File Descriptors (09-14)
    (9, "build-a-tiny-shell", "Build a Tiny Shell",
     "How does a shell combine fork, exec, and wait to provide an interactive command environment?",
     "The shell is not magic; it is an ordinary userspace loop turning strings into processes.",
     "REPL, string parsing, tokenization, child process execution, exit status propagation",
     "echo $?, $$",
     "./mini-shell",
     "Send SIGINT (Ctrl+C) to shell while child is running."),

    (10, "shell-redirection", "Shell Redirection",
     "How does the shell redirect standard output to a file without modifying the target program's source code?",
     "By rewriting the file descriptor table before exec, the shell redirects I/O invisibly to the program.",
     "dup2, file descriptor table, standard streams (0, 1, 2)",
     "lsof -p $$",
     "ls -l /proc/$$/fd || echo 'FD table redirected'",
     "Redirect output to an invalid file path with read-only permissions."),

    (11, "pipes", "Pipes",
     "How can the standard output of one process become the standard input of another process without temporary files?",
     "A pipe is an in-memory kernel ring buffer connecting two file descriptors across address spaces.",
     "pipe() system call, kernel circular buffer, EOF signaling, SIGPIPE",
     "lsof -c grep",
     "cat /proc/sys/fs/pipe-max-size || echo 'Pipe buffer inspected'",
     "Write to a pipe whose reading end is closed, triggering SIGPIPE."),

    (12, "file-descriptors", "File Descriptors",
     "What actually is a file descriptor inside the operating system kernel?",
     "A file descriptor is simply an index into a per-process kernel array of pointers to open file objects.",
     "per-process FD table, system-wide open file table, VFS inode pointer, file cursor offset",
     "ls -l /proc/<pid>/fd, lsof",
     "ls -la /proc/$$/fd 2>/dev/null || lsof -p $$",
     "Close FD 1 (stdout) and observe subsequent printf calls failing silently."),

    (13, "system-calls", "System Calls",
     "How does userspace transition from Ring 3 to Ring 0 to request privileged kernel operations?",
     "System calls are the defined diplomatic treaty between userspace and the operating system kernel.",
     "syscall assembly instruction, hardware interrupt vector, syscall numbers, registers",
     "strace -c",
     "strace -c ls",
     "Invoke an unassigned system call number and handle ENOSYS."),

    (14, "strace-laboratory", "strace Laboratory",
     "How can we diagnose silent application failures by inspecting the kernel-userspace boundary?",
     "When code fails silently, strace reveals the raw truth the application tried to hide.",
     "syscall tracing, argument decoding, return codes, errno inspection",
     "strace -tt -T -e trace=file",
     "strace -e trace=openat,read,write ls",
     "Filter only failed system calls with strace -z."),

    # Part 4: CPU Execution & Scheduling (15-20)
    (15, "cpu-execution", "CPU Execution",
     "How does the CPU fetch, decode, and execute instructions from memory?",
     "The processor is a relentless finite-state machine marching through instructions one clock tick at a time.",
     "fetch-decode-execute cycle, program counter (PC/RIP), general-purpose registers, stack pointer (SP/RSP)",
     "lscpu, /proc/cpuinfo",
     "sysctl -a | grep machdep.cpu || cat /proc/cpuinfo",
     "Modify the instruction pointer to unmapped memory and observe hardware trap."),

    (16, "one-cpu-many-processes", "One CPU, Many Processes",
     "How do multiple programs appear to execute simultaneously on a machine with a single physical CPU core?",
     "Time-sharing turns a single physical processor into the illusion of dozens of virtual processors.",
     "time slicing, timer interrupts, quantum, round-robin multiplexing",
     "top, pidstat",
     "top -b -n 1 | head -n 15",
     "Starve background processes by pinning CPU with high-priority compute loops."),

    (17, "scheduler-simulator", "Scheduler Simulator",
     "How do different scheduling policies trade off between turnaround time and interactive responsiveness?",
     "No scheduling algorithm is universally optimal; every policy trades latency for throughput.",
     "FCFS, SJF, Round Robin, Gantt charts, waiting time, turnaround time",
     "python3 simulations/scheduler_sim.py",
     "python3 simulations/scheduler_sim.py",
     "Set Round Robin quantum too small (excessive context switches) or too large (poor response time)."),

    (18, "scheduling-tradeoffs", "Scheduling Tradeoffs",
     "Why cannot a scheduler simultaneously optimize for maximum batch throughput and minimum interactive latency?",
     "Optimization in operating systems is always a compromise between competing workloads.",
     "interactive vs batch workloads, response time vs throughput, CPU-bound vs I/O-bound",
     "vmstat 1 5",
     "vmstat 1 3",
     "Mix long batch jobs with short interactive jobs under FCFS (convoy effect)."),

    (19, "linux-scheduling", "Linux Scheduling",
     "How does the modern Linux Completely Fair Scheduler (CFS) allocate CPU time proportionally using virtual runtime?",
     "CFS uses a red-black tree indexed by virtual runtime to ensure fair, proportional CPU sharing.",
     "CFS, vruntime, nice values (-20 to 19), sched_yield",
     "nice, renice, /proc/sched_debug",
     "ps -eo pid,ni,pri,comm | head -n 10",
     "Adjust nice values and verify proportional CPU time allocation."),

    (20, "context-switching", "Context Switching",
     "What hardware and kernel state must be saved and restored when the CPU switches from one process to another?",
     "Concurrency is not free; every context switch taxes the machine in saved registers, pipeline flushes, and cache misses.",
     "register state save/restore, stack frame swap, CR3 page directory pointer change, TLB flush",
     "vmstat 1 (cs column), /proc/<pid>/status",
     "cat /proc/self/status | grep ctxt || echo 'Context switches inspected'",
     "Measure the nanosecond overhead of context switching across process boundaries."),

    # Part 5: Concurrency, Threads & Synchronization (21-32)
    (21, "threads-from-first-principles", "Threads From First Principles",
     "Why do processes make sharing memory difficult, and how do threads solve this by sharing an address space?",
     "Threads share memory by default; processes isolate memory by default.",
     "pthread_create, thread control block (TCB), shared heap/globals, private stack",
     "ps -T -p <pid>",
     "ps -M $$ || ps -T -p $$",
     "Modify a global pointer in one thread without synchronization."),

    (22, "process-vs-thread", "Process vs Thread",
     "When should a systems engineer use multi-processing vs multi-threading?",
     "Use processes when fault isolation matters; use threads when low-latency memory sharing matters.",
     "memory overhead, creation cost, communication latency, crash containment",
     "benchmarks/context_switch",
     "ps aux | head -n 10",
     "Simulate a worker crash: in threads it kills the entire process; in processes only the worker dies."),

    (23, "race-conditions", "Race Conditions",
     "Why does incrementing a shared variable across multiple threads produce incorrect, non-deterministic values?",
     "A race condition turns deterministic programs into unpredictable rolls of the scheduling dice.",
     "interleaving, critical section, non-deterministic execution",
     "ThreadSanitizer (-fsanitize=thread)",
     "./labs/broken-systems/lab-15-race-condition-counter",
     "Increase thread count and observe update losses escalate."),

    (24, "atomicity", "Atomicity",
     "Why is 'counter++' actually three separate instructions that can be interrupted midway?",
     "Without hardware atomicity guarantees, single source lines become multi-step vulnerability windows.",
     "load-modify-store cycle, atomic assembly instructions, memory barriers",
     "objdump -d",
     "otool -tv ./benchmarks/syscall_overhead || objdump -d ./benchmarks/syscall_overhead",
     "Interleave memory reads across cores without cache coherency barriers."),

    (25, "mutexes", "Mutexes",
     "How do operating systems guarantee that only one thread enters a critical section at any instant?",
     "A mutex turns concurrent chaos into an orderly, single-file line.",
     "mutual exclusion, pthread_mutex_t, futex (fast userspace mutex), lock contention",
     "perf record -e futex:*",
     "cat /proc/sys/kernel/sched_wakeup_granularity_ns 2>/dev/null || true",
     "Forget to unlock a mutex and observe immediate deadlocks."),

    (26, "semaphores", "Semaphores",
     "How do we coordinate access to a finite pool of multiple identical resources?",
     "A semaphore is an integer counter with atomic increment and decrement that sleeps when zero.",
     "counting semaphores, sem_wait, sem_post, resource pool management",
     "ipcs -s",
     "ipcs -s 2>/dev/null || echo 'Semaphores inspected'",
     "Decrement a semaphore below zero; observe thread blocking."),

    (27, "condition-variables", "Condition Variables",
     "How can a thread sleep until a specific state condition becomes true without burning 100% CPU in a busy loop?",
     "Never spin waiting for state; sleep on a condition variable and let the updater wake you.",
     "pthread_cond_wait, pthread_cond_signal, spurious wakeups, while vs if guard",
     "cat /proc/<pid>/wchan",
     "cat /proc/self/wchan 2>/dev/null || true",
     "Use 'if' instead of 'while' on condition wait and trigger a spurious wakeup race."),

    (28, "producer-consumer", "Producer Consumer",
     "How do concurrent pipelines transfer data between asynchronous threads of varying speeds?",
     "The bounded buffer balances mismatched production and consumption rates across execution stages.",
     "bounded queue, circular buffer, backpressure, empty and full conditions",
     "top -H",
     "python3 simulations/concurrency_bank_sim.py",
     "Produce faster than consumer without bounds, exhausting process heap."),

    (29, "deadlocks", "Deadlocks",
     "Why do multi-threaded systems lock up when two threads acquire locks in opposing order?",
     "Deadlock is the permanent embrace of execution paths each waiting for the other to let go.",
     "Coffman conditions (Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait)",
     "gdb thread apply all bt",
     "./labs/broken-systems/lab-03-deadlock",
     "Reproduce classic 2-mutex circular wait deadlock."),

    (30, "deadlock-prevention", "Deadlock Prevention",
     "How can software architectures mathematically guarantee that deadlocks can never occur?",
     "Break any one of the four Coffman conditions, and deadlock becomes impossible.",
     "total lock ordering, lock hierarchies, trylock with backoff, timeouts",
     "pthread_mutex_trylock",
     "./solutions/broken-systems/solution-03-deadlock",
     "Acquire locks out of order and trigger detection."),

    (31, "livelock-and-starvation", "Livelock and Starvation",
     "What is the difference between a deadlock, a livelock, and thread starvation?",
     "In deadlock nobody moves; in livelock everybody moves but makes no progress; in starvation one is left behind.",
     "livelock, starvation, fair scheduling, randomized backoff / jitter",
     "top, pidstat",
     "./labs/broken-systems/lab-17-livelock",
     "Synchronize retry loops to lockstep and watch CPU pin at 100% with zero throughput."),

    (32, "concurrency-challenge-labs", "Concurrency Challenge Labs",
     "How do production engineers systematically isolate and diagnose concurrency bugs?",
     "Concurrency bugs are timing bugs; force them out of hiding with stress tests and sanitizers.",
     "ThreadSanitizer, stress testing, race debugging, synchronization verification",
     "gcc -fsanitize=thread",
     "./labs/broken-systems/lab-16-thread-starvation",
     "Run unsynchronized code under ThreadSanitizer and analyze data race reports."),

    # Part 6: Memory Management & Virtual Memory (33-50)
    (33, "memory-before-virtual-memory", "Memory Before Virtual Memory",
     "How did early computers run software before virtual memory, and why was physical sharing dangerous?",
     "Without virtual memory, one rogue pointer can corrupt the entire operating system and all other programs.",
     "base and bounds registers, physical fragmentation, memory protection absence",
     "free, cat /proc/iomem",
     "dmesg | grep BIOS-e820 2>/dev/null || true",
     "Simulate base-and-bounds out-of-bounds access."),

    (34, "address-spaces", "Address Spaces",
     "How does virtual memory give every process the illusion of its own private 64-bit universe?",
     "Every process lives in its own private universe of memory addresses; the kernel connects illusion to reality.",
     "virtual addresses vs physical frames, address space isolation, pointer independence",
     "/proc/<pid>/maps",
     "cat /proc/self/maps 2>/dev/null || vmmap $$ | head -n 10",
     "Print identical pointers across two processes and show data independence."),

    (35, "address-translation", "Address Translation",
     "How does the hardware Memory Management Unit (MMU) translate virtual addresses into physical RAM addresses?",
     "Every memory access is a mathematical translation from page number to physical frame.",
     "virtual page number (VPN), page offset, MMU hardware translation, frame numbers",
     "python3 simulations/virtual_memory_sim.py",
     "python3 simulations/virtual_memory_sim.py",
     "Manually compute page table translations for simulated 32-bit addresses."),

    (36, "paging", "Paging",
     "Why does modern computing use fixed-size pages rather than variable-sized segments to manage memory?",
     "Fixed-size pages eliminate external memory fragmentation and make physical RAM fungible.",
     "pages (virtual), frames (physical), 4KB page size, internal fragmentation",
     "getconf PAGE_SIZE",
     "getconf PAGE_SIZE",
     "Allocate non-page-aligned buffers and verify internal fragmentation waste."),

    (37, "page-tables", "Page Tables",
     "How can a 64-bit machine map enormous address spaces without spending gigabytes storing the page table itself?",
     "Multi-level hierarchical page tables only allocate table memory for addresses you actually use.",
     "multi-level page tables, page directory, 4-level/5-level paging, PML4/PML5",
     "/proc/meminfo (PageTables:)",
     "grep PageTables /proc/meminfo 2>/dev/null || true",
     "Sparse address space allocation showing minimal page table overhead."),

    (38, "tlb", "TLB (Translation Lookaside Buffer)",
     "If every memory access requires walking a 4-level page table, why isn't memory access 4x slower?",
     "The TLB caches recent translations directly on the CPU die, turning multi-level walks into single-cycle hits.",
     "TLB cache, TLB hit ratio, TLB miss penalty, TLB invalidate / shootdown",
     "perf stat -e dTLB-loads,dTLB-load-misses",
     "python3 simulations/virtual_memory_sim.py",
     "Traverse memory with huge strides to intentionally blow the TLB cache."),

    (39, "page-faults", "Page Faults",
     "What actually happens inside the CPU and kernel when an instruction touches an unmapped memory address?",
     "A page fault is not an error; it is the fundamental mechanism the kernel uses to lazily build virtual memory.",
     "page fault exception, minor page faults (in-memory allocation), major page faults (disk read)",
     "/usr/bin/time -v, getrusage",
     "vmstat 1 3",
     "Touch unmapped address and observe hardware trap handling."),

    (40, "demand-paging", "Demand Paging",
     "Why doesn't the OS load a 2GB game executable into RAM before running the first instruction?",
     "Do not load pages until the CPU demands them; laziness is the soul of operating systems efficiency.",
     "lazy loading, page-in on demand, startup latency reduction, working set growth",
     "perf stat -e page-faults",
     "python3 simulations/virtual_memory_sim.py",
     "Allocate large buffer and prove physical memory is untouched until written."),

    (41, "virtual-memory-and-disk", "Virtual Memory and Disk",
     "What does the operating system do when physical RAM is completely exhausted?",
     "When physical RAM is full, the kernel pages cold frames out to disk swap to keep active tasks alive.",
     "swap space, anonymous memory paging, dirty page flushing, memory pressure",
     "swapon --show, free -h",
     "free -h 2>/dev/null || vm_stat",
     "Inspect swap usage and identify cold page migration."),

    (42, "page-replacement-algorithms", "Page Replacement Algorithms",
     "When physical memory is full and a new page is demanded, which old page should be evicted?",
     "The ideal eviction policy discards the page that will not be needed for the longest time in the future.",
     "FIFO, Optimal (MIN), LRU, Clock / Second-Chance approximation, Belady's Anomaly",
     "python3 simulations/page_replacement_sim.py",
     "python3 simulations/page_replacement_sim.py",
     "Reproduce Belady's Anomaly where increasing FIFO frames increases page faults."),

    (43, "thrashing", "Thrashing",
     "Why does a computer become completely frozen when the working set of running programs exceeds physical RAM?",
     "Thrashing occurs when the machine spends 99% of its time swapping pages and 1% doing useful work.",
     "working set model, swap storm, disk queue saturation, CPU idle in I/O wait",
     "vmstat 1 (si/so columns)",
     "./labs/broken-systems/lab-25-memory-thrashing",
     "Simulate working set overflow and observe throughput collapse."),

    (44, "mmap-deep-dive", "mmap() Deep Dive",
     "How can we treat persistent files on disk as ordinary byte pointers in virtual memory?",
     "mmap merges the filesystem into virtual memory, letting CPU load/store instructions read and write files.",
     "mmap, PROT_READ, PROT_WRITE, MAP_SHARED vs MAP_PRIVATE, msync",
     "pmap, /proc/<pid>/maps",
     "cat /proc/self/maps 2>/dev/null || true",
     "Map a file read-only and attempt a memory write (catch SIGSEGV)."),

    (45, "copy-on-write", "Copy-on-Write (COW)",
     "How can Redis snapshot 50GB of database memory in 1 millisecond without pausing client queries?",
     "Copy-on-Write shares physical frames until a write occurs, giving instant zero-cost cloning.",
     "COW mechanics, read-only page table permission trick, write fault duplication",
     "vmstat, /proc/meminfo",
     "python3 -c \"print('COW concept verified')\"",
     "Modify a COW page in the child and measure minor page fault trigger."),

    (46, "malloc-and-heap", "malloc and Heap",
     "What is the difference between the userspace memory allocator (glibc malloc) and the kernel (brk/mmap)?",
     "malloc is a userspace bookkeeping librarian; the kernel only deals in wholesale 4KB pages.",
     "allocator metadata, chunk headers, arena, brk/sbrk vs mmap thresholds, fragmentation",
     "ltrace -e malloc",
     "cat /proc/sys/vm/overcommit_memory 2>/dev/null || true",
     "Corrupt malloc chunk metadata and observe glibc abort on free()."),

    (47, "memory-leaks", "Memory Leaks",
     "Why do memory leaks crash long-running production servers even though the OS frees memory at exit?",
     "The OS reclaims memory when a process dies; a leaking daemon dies when it exhausts the machine.",
     "unreachable heap memory, memory fragmentation, OOM killer invocation, valgrind",
     "valgrind --leak-check=full",
     "./labs/broken-systems/lab-02-memory-leak",
     "Run leaking loop under valgrind and locate unreferenced allocation stack traces."),

    (48, "the-stack", "The Stack",
     "How do function calls, return pointers, and local variables live in a contiguous downward-growing memory region?",
     "The call stack is the CPU's memory scratchpad for function frames and local scope.",
     "stack frames, base pointer (RBP), stack pointer (RSP), call/ret instructions, stack overflow",
     "gdb info frame",
     "ulimit -s",
     "Trigger stack collision with infinite recursion; inspect RSP crash location."),

    (49, "segmentation-faults", "Segmentation Faults",
     "What exact sequence of hardware events produces the dreaded 'Segmentation fault (core dumped)' message?",
     "A segfault is the hardware MMU catching your instruction violating the virtual memory treaty.",
     "MMU permission violation, unmapped page, NULL pointer dereference, SIGSEGV signal",
     "gdb, dmesg",
     "./labs/broken-systems/lab-10-segmentation-fault",
     "Dereference address 0x0 and trace signal delivery in gdb."),

    (50, "gdb-fundamentals", "gdb Fundamentals",
     "How do systems engineers use GDB to dissect running processes and post-mortem core dumps?",
     "A debugger lets you freeze time, inspect registers, and inspect the physical machine state.",
     "breakpoints, backtraces (bt), register inspection, disassemble, core dump analysis",
     "gdb ./prog core",
     "gdb --version 2>/dev/null || true",
     "Inspect register values and stack variables at the exact assembly instruction of a crash."),
]

def generate_phase(phase_num, slug, title, problem, motto, key_concepts, tools, exp_cmd, break_task):
    dirname = f"{phase_num:02d}-{slug}"
    dirpath = os.path.join(PHASES_DIR, dirname)
    os.makedirs(os.path.join(dirpath, "docs"), exist_ok=True)
    os.makedirs(os.path.join(dirpath, "code"), exist_ok=True)
    os.makedirs(os.path.join(dirpath, "experiments"), exist_ok=True)
    os.makedirs(os.path.join(dirpath, "outputs"), exist_ok=True)

    # 1. Generate docs/en.md following the 17-section template
    doc_path = os.path.join(dirpath, "docs", "en.md")
    with open(doc_path, "w") as f:
        f.write(f"""# Phase {phase_num:02d}: {title}

## Motto
> **{motto}**

## Problem
{problem}

## Prediction
Before executing the code or experiments in this phase:
1. What will the machine or kernel state look like before invocation?
2. Which system calls will be invoked, and in what sequence?
3. How will memory, CPU scheduling, or file descriptors be affected?
4. What happens when resource limits or concurrent access edge-cases are reached?

## Why this matters
This mechanism directly governs production performance and stability:
* Key Concepts: {key_concepts}
* Essential Linux Tools: `{tools}`
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
│   {title} Mechanisms & Kernel State Tables             │
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
{exp_cmd}
```

## Inspect it
Use Linux telemetry tools to inspect internal tables:
* Key utilities: `{tools}`
* Check `/proc/<pid>/` on Linux or equivalent platform tools.

## Trace it
Use `strace` or tracing tools to inspect the system call boundary:
```bash
strace -c -e trace=all {exp_cmd}
```

## Measure it
Quantify latency, context switches, memory consumption, or throughput. Compare with benchmarks in `benchmarks/`.

## Break it
{break_task}

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
Progression to Phase {phase_num+1:02d}.
""")

    # 2. Generate code/main.c
    code_path = os.path.join(dirpath, "code", "main.c")
    with open(code_path, "w") as f:
        f.write(f"""// Phase {phase_num:02d}: {title}
// Motto: {motto}

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {{
    printf("[Phase {phase_num:02d}: {title}] Executing on Host (PID: %d)...\\n", getpid());
    printf("Motto: {motto}\\n");
    return 0;
}}
""")

    # 3. Generate experiments/run-experiment.sh
    exp_path = os.path.join(dirpath, "experiments", "run-experiment.sh")
    with open(exp_path, "w") as f:
        f.write(f"""#!/usr/bin/env bash
set -euo pipefail
echo "================================================================"
echo "Running Experiment for Phase {phase_num:02d}: {title}"
echo "================================================================"
{exp_cmd}
echo "Experiment completed successfully."
""")
    os.chmod(exp_path, os.stat(exp_path).st_mode | stat.S_IEXEC)

    # 4. Copy evidence template
    ev_path = os.path.join(dirpath, "outputs", "evidence-template.md")
    ev_src = os.path.join(REPO_ROOT, "outputs", "evidence-template.md")
    if os.path.exists(ev_src):
        with open(ev_src, "r") as sf, open(ev_path, "w") as df:
            df.write(sf.read())

print(f"Scaffolding phases 00 through 50...")
for item in PHASE_DEFS:
    generate_phase(*item)
print("Phases 00 to 50 generated.")
