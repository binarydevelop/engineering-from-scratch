# 25+ Broken Systems Debugging Labs

> **Pedagogical Rule:** Symptoms first, diagnosis second, root cause third, fix fourth. Solutions are strictly isolated in `solutions/broken-systems/`.

When real production systems fail, there is no error message telling you which line of code to edit. You are presented with a **symptom**: a server is unresponsive, memory is vanishing, CPU is pegged at 100%, or requests fail with cryptic error codes.

Each lab in this directory provides:
1. **The Symptom:** What the user or monitoring dashboard observes.
2. **The Reproduction:** A compiled C program or script inducing the exact failure.
3. **The Diagnostic Challenge:** Which tools (`ps`, `top`, `strace`, `gdb`, `lsof`, `ss`, `/proc`) to use to identify the root cause without reading the source code.
4. **The Goal:** Formulate a hypothesis, confirm it with measurement, and implement the fix.

---

## The 25 Diagnostic Incidents

| Lab | Incident Title | Primary Symptom | Key Diagnostic Tool |
| :--- | :--- | :--- | :--- |
| **Lab 01** | `cpu-saturation` | CPU core pegged at 100%, fans spinning, laptop heats up | `top`, `pidstat`, `perf` |
| **Lab 02** | `memory-leak` | Process memory continuously grows until OOM-killer intervenes | `valgrind`, `pmap`, `/proc/<pid>/status` |
| **Lab 03** | `deadlock` | Multi-threaded application freezes; CPU drops to 0% | `gdb`, `thread apply all bt` |
| **Lab 04** | `zombie-process` | Process table fills with `<defunct>` entries | `ps aux \| grep 'Z'`, `pstree -p` |
| **Lab 05** | `fd-leak` | Application fails with `EMFILE (Too many open files)` | `lsof -p <pid>`, `ls -l /proc/<pid>/fd` |
| **Lab 06** | `port-already-in-use` | Server fails on restart with `EADDRINUSE (Address already in use)` | `ss -tulpn`, `lsof -i :8080` |
| **Lab 07** | `permission-denied` | Application aborts with `EACCES (Permission denied)` | `ls -l`, `stat`, `id` |
| **Lab 08** | `full-disk-simulation` | Silent data truncation when disk is full | `df -h`, `strace -e write` |
| **Lab 09** | `unhandled-signal-crash` | Binary abruptly terminates with `Floating point exception` | `gdb`, `dmesg`, signal handler |
| **Lab 10** | `segmentation-fault` | Binary terminates with `Segmentation fault (core dumped)` | `gdb`, `core` analysis, `bt` |
| **Lab 11** | `blocked-syscall` | Thread hangs indefinitely on `read()` syscall | `strace -p <pid>`, `cat /proc/<pid>/wchan` |
| **Lab 12** | `network-timeout` | Client stalls for 120 seconds before failing | `tcpdump`, `strace -T -e connect` |
| **Lab 13** | `unbuffered-io-bottleneck` | Small file write takes 15 seconds instead of 5 ms | `strace -c`, `/usr/bin/time -v` |
| **Lab 14** | `orphan-process` | Background worker remains running after terminal closes | `ps -ef`, `PPID == 1` |
| **Lab 15** | `race-condition-counter` | Counter reports 1,120,400 instead of expected 2,000,000 | `ThreadSanitizer`, code inspection |
| **Lab 16** | `thread-starvation` | Worker thread never receives work; latency spikes to infinity | `strace -tt`, lock profiling |
| **Lab 17** | `livelock` | CPU is 100% busy but zero work items complete | `top`, state inspection, `gdb` |
| **Lab 18** | `stack-overflow` | Deep recursion crashes abruptly with `SIGSEGV` near `$rsp` | `gdb`, stack pointer comparison |
| **Lab 19** | `use-after-free` | Intermittent data corruption and heap crashes | `AddressSanitizer` (`-fsanitize=address`) |
| **Lab 20** | `zombie-apocalypse` | Child processes accumulate faster than parent can reap | `ps -u $USER`, `waitpid(-1, WNOHANG)` |
| **Lab 21** | `broken-pipe-sigpipe` | Writing process mysteriously dies when peer disconnects | `strace`, `signal(SIGPIPE, SIG_IGN)` |
| **Lab 22** | `path-lookup-failure` | Shell says `command not found` despite binary existing | `echo $PATH`, `which`, `chmod +x` |
| **Lab 23** | `priority-inversion` | High priority task blocked waiting on low priority task | Priority inheritance mutexes |
| **Lab 24** | `listen-backlog-overflow` | Clients experience connection drops during traffic bursts | `netstat -s`, `ss -lnt` |
| **Lab 25** | `memory-thrashing` | System freezes under heavy page faults | `vmstat 1`, `free -h` |
