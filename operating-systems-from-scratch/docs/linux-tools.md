# Linux Diagnostic & Systems Inspection Toolkit

> **Core Philosophy:** Tools are not commands to memorize. Every diagnostic tool answers a specific hypothesis about why hardware, kernel tables, or processes behave unexpectedly.

---

## The Master Diagnostic Matrix

| Question You Are Asking | Primary Tool | Target Resource | Key Flag / Usage |
| :--- | :--- | :--- | :--- |
| **"Which processes are active, who spawned them, and what state are they in?"** | `ps`, `pstree` | Process Table / Scheduler | `ps aux`, `ps -ef --forest`, `pstree -p` |
| **"Which process is consuming CPU cores right now?"** | `top`, `pidstat` | CPU Cores / Scheduling | `top -b -n 1`, `pidstat -u 1 5` |
| **"What system calls is my application executing and where is it blocking?"** | `strace` | Syscall Boundary / Kernel | `strace -c ./prog`, `strace -T -e trace=network` |
| **"Why is my program crashing or segmentation faulting?"** | `gdb` | CPU Registers / Stack Frames | `gdb ./prog core`, `bt` (backtrace) |
| **"Why won't my server bind to its port?"** | `ss`, `lsof` | Network Sockets / TCP Table | `ss -tulpn`, `lsof -i :8080` |
| **"Which files, sockets, and pipes does this process currently hold open?"** | `lsof`, `/proc` | File Descriptor Table | `lsof -p <PID>`, `ls -l /proc/<PID>/fd` |
| **"How much physical RAM is truly available vs cached as disk pages?"** | `free`, `vmstat` | Memory Management / Page Cache | `free -h`, `vmstat 1 5` |
| **"How is virtual address space mapped into memory for this process?"** | `pmap`, `/proc` | Virtual Address Space / VMA | `pmap -x <PID>`, `cat /proc/<PID>/maps` |
| **"Is disk I/O saturated or waiting on hardware queues?"** | `iostat` | Block Layer / Storage | `iostat -xz 1 5` |
| **"Where are CPU cycles being spent inside userspace vs kernel code?"** | `perf` | CPU Hardware Counters | `perf record -g ./prog`, `perf report` |
| **"What limits are placed on this process's open files or memory?"** | `ulimit` | Resource Limits (`RLIMIT`) | `ulimit -a`, `prlimit --pid=<PID>` |
| **"How long did this command spend in userspace vs kernel mode?"** | `time` | CPU Accounting | `/usr/bin/time -v ./prog` |

---

## Deep Tool References

### 1. `strace`: The Syscall Microscope
* **What question does it answer?** *"What exact conversation is userspace having with the operating system kernel?"*
* **When to use:** When a binary fails silently, hangs on startup, or exhibits unexpected file access.
* **Essential invocations:**
  ```bash
  # Count calls, total time, and errors per syscall
  strace -c ./my_program

  # Filter only file operations with timestamps
  strace -t -e trace=openat,read,write,close ./my_program

  # Attach to an already running background daemon
  sudo strace -p <PID>
  ```

### 2. `lsof` & `ss`: The Descriptor & Socket Investigators
* **What question does it answer?** *"Who owns this port or file descriptor right now?"*
* **Real-world scenario:** A web server fails on restart with `EADDRINUSE`.
  ```bash
  # Find process listening on TCP port 8080
  lsof -i :8080
  # or using the Linux socket statistics tool
  ss -tulpn | grep 8080
  ```

### 3. `/proc`: The Kernel's Window into its Own Brain
* **What question does it answer?** *"What is the kernel's live internal state for hardware and processes?"*
* `/proc` is not stored on disk; it is a virtual pseudo-filesystem synthesized on-the-fly by the kernel.
  ```bash
  # Check physical memory allocation
  cat /proc/meminfo

  # Inspect open file descriptors of process 1234
  ls -l /proc/1234/fd

  # Inspect virtual memory regions (VMA) of process 1234
  cat /proc/1234/maps

  # Inspect process state, threads, and context switches
  cat /proc/1234/status
  ```

### 4. `free` & `vmstat`: The Memory & Paging Gauges
* **What question does it answer?** *"Is the system out of memory, or is memory merely being utilized productively as page cache?"*
* **The Golden Insight:** In Linux, "free" memory is wasted memory. Linux fills unused RAM with the **page cache** to accelerate filesystem reads. The number that matters for capacity planning is **available memory**.
  ```bash
  free -h
  # vmstat: r (runnable), b (blocked I/O), si/so (swap in/out), bi/bo (block in/out)
  vmstat 1 5
  ```

### 5. `gdb`: The Execution Dissector
* **What question does it answer?** *"What assembly instruction and source line caused the processor exception?"*
  ```bash
  # Launch program under gdb
  gdb ./buggy_binary
  (gdb) run
  # When it crashes with SIGSEGV:
  (gdb) bt              # Print stack backtrace
  (gdb) info registers  # View register contents (e.g. $rip, $rsp)
  (gdb) print ptr       # Inspect variable values at crash site
  ```

### 6. `ulimit` & `prlimit`: The Resource Boundary Police
* **What question does it answer?** *"Why is the application throwing 'Too many open files' or 'Cannot allocate memory' despite abundant hardware?"*
  ```bash
  # Show current soft limits
  ulimit -a

  # Check limits of a running remote daemon
  cat /proc/<PID>/limits
  ```
