# Track 8: Linux Diagnostic & Kernel Inspection Exercises

> **Motto:** Never guess why an operating system is behaving strangely when the kernel exports its live telemetry into `/proc`, `strace`, and hardware counters.

All solutions are located in `solutions/exercises/08-linux-debugging-and-inspection-solutions.md`.

---

### Exercise 8.1: The Syscall Counter (`strace -c`)
Run `strace -c ls /usr` and `strace -c python3 -c "print('hello')"`. Compare the total number of system calls, the most frequent syscalls, and the percentage of time spent in the kernel.

### Exercise 8.2: Filtering Syscalls by Class
Using `strace -e trace=file` and `strace -e trace=network`, trace a `curl` command. Filter only operations that open files or initiate network connections.

### Exercise 8.3: Syscall Timing & Latency Profiling
Run `strace -T -tt ./my_program` to log microsecond timestamps and the exact duration spent inside each kernel system call. Identify which syscall acts as the latency bottleneck.

### Exercise 8.4: Attaching `strace` to a Running Daemon
Start a background process that sleeps in a loop. In another terminal, attach to the running PID using `sudo strace -p <PID>`. Observe system calls in real-time as the process wakes up.

### Exercise 8.5: Inspecting `/proc/<pid>/status`
Write a program and examine its `/proc/<pid>/status`. Identify:
* `VmPeak` vs `VmSize` vs `VmRSS`
* `Threads` count
* `voluntary_ctxt_switches` vs `nonvoluntary_ctxt_switches`
What is the difference between a voluntary and an involuntary context switch?

### Exercise 8.6: Live Inspection of Descriptor Tables
Open 3 files and 1 pipe in a C program and call `getchar()`. Inspect `/proc/<pid>/fd/` using `ls -l`. Verify that each file descriptor is a symlink pointing to the true file path or pipe ID.

### Exercise 8.7: Inspecting Virtual Memory Regions (`/proc/<pid>/maps`)
Parse `/proc/<pid>/maps`. What do the address range, permissions (`rwxp`), offset, device, and pathname indicate? How does the kernel distinguish private (`p`) vs shared (`s`) mappings?

### Exercise 8.8: Debugging Crashes with `gdb`
Compile a crashing program with `gcc -g`. Launch it under `gdb ./prog`. When it crashes, run:
* `bt` (print full stack backtrace)
* `info registers` (inspect CPU registers)
* `print ptr` (inspect pointer values at crash site)

### Exercise 8.9: Setting Hardware Breakpoints & Watchpoints
In `gdb`, use `watch global_var` to set a hardware watchpoint on a memory address. Run the program and observe `gdb` pausing execution the exact moment any thread or function writes to that memory location.

### Exercise 8.10: Tracking File Descriptors with `lsof`
Use `lsof` to answer:
1. Which processes are currently holding `/var/log/syslog` open?
2. Which process is listening on TCP port 5432?
3. Which deleted files are still holding disk space open? (`lsof +L1`).

### Exercise 8.11: Measuring Memory Utilization with `free` and `vmstat`
Run `free -h` and `vmstat 1 5`. Explain:
* Why "free" memory is often small on active Linux systems.
* What "available" memory represents.
* What the `buff/cache` column measures.
* What `si` (swap in) and `so` (swap out) columns indicate.

### Exercise 8.12: Process Limits via `ulimit` and `prlimit`
Check soft and hard limits on your shell with `ulimit -a`. Lower the maximum open files to 32 using `ulimit -n 32`. Run a program that attempts to open 40 files and observe `EMFILE`.

### Exercise 8.13: Tracing Library Calls with `ltrace`
Where supported, compare `ltrace ./hello` with `strace ./hello`. What is the difference between tracing C library function calls (`printf`, `malloc`) and tracing kernel system calls (`write`, `brk`)?

### Exercise 8.14: CPU Utilization Tracking with `pidstat`
Run `pidstat -u 1 5` while running a compute-bound task. Differentiate `%usr` (time spent executing user instructions) from `%system` (time spent executing kernel code on behalf of the process).

### Exercise 8.15: Hardware Performance Counters with `perf`
Where supported, run `perf stat ls -R /usr`. Inspect:
* CPU clock and task-clock
* Context switches and CPU migrations
* Page faults
* Instructions per cycle (IPC) and branch-misses.
