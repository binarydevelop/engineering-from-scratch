# Track 9: Containers, Namespaces & Systems Performance Exercises

> **Motto:** Containers do not exist. Docker and Kubernetes are simply API managers coordinating standard Linux namespaces, cgroups, and filesystem mounts.

All solutions are located in `solutions/exercises/09-containers-and-performance-solutions.md`.

---

### Exercise 9.1: The PID Namespace (`CLONE_NEWPID`)
In a disposable Linux sandbox or container, use `unshare --pid --fork bash` to enter a new PID namespace. Run `echo $$` and `ps -ef`. Why does the new shell perceive itself as PID 1?

### Exercise 9.2: Mounting a Private `/proc` in a Container
In Exercise 9.1, why does `ps -ef` still show all host processes before running `mount -t proc proc /proc`? Explain how `ps` reads live process tables from `/proc`, and how mount namespaces complete the isolation.

### Exercise 9.3: UTS Namespace Hostname Isolation
Use `unshare --uts bash` to enter a private UTS namespace. Change the hostname with `hostname container-node`. In a second terminal on the host, run `hostname`. Prove that the host's hostname was not modified!

### Exercise 9.4: Network Namespace Isolation (`ip netns`)
Create two isolated network namespaces:
```bash
sudo ip netns add net-a
sudo ip netns add net-b
```
Connect them using a virtual ethernet pair (`veth-a` $\leftrightarrow$ `veth-b`). Assign IP addresses `10.0.0.1/24` and `10.0.0.2/24`. Ping from `net-a` to `net-b`.

### Exercise 9.5: Cgroups v2 Memory Limits
In a Linux environment, inspect `/sys/fs/cgroup`. Create a control group directory `/sys/fs/cgroup/test_limit`. Set a memory limit of 50MB:
`echo "52428800" > /sys/fs/cgroup/test_limit/memory.max`
Attach a process and trigger an allocation exceeding 50MB. Observe the kernel OOM killer terminating the process.

### Exercise 9.6: Cgroups v2 CPU Throttling (`cpu.max`)
Set a CPU limit of 0.5 cores:
`echo "50000 100000" > /sys/fs/cgroup/test_limit/cpu.max` (50ms quota per 100ms period).
Run a 100% compute loop inside the cgroup and verify with `top` that its CPU utilization is clamped to exactly 50%.

### Exercise 9.7: Dropping Capabilities with `capsh`
Inspect current capabilities with `capsh --print`. Write a program that drops `CAP_NET_BIND_SERVICE` and attempts to bind to privileged port 80. Observe `EACCES`.

### Exercise 9.8: Filesystem Isolation via `chroot`
Create a minimal directory `mini_root/` with a statically linked `/bin/sh` or `/bin/busybox`. Use `chroot mini_root/ /bin/sh`. Try to access `/etc/passwd` on the host. Explain why `chroot` restricts the visible filesystem tree.

### Exercise 9.9: Why `chroot` Is Not a Security Boundary
Explain how a root process inside a traditional `chroot` can break out into the host filesystem using `mkdir("escape"); chroot("escape"); chdir("../../../.."); chroot(".");`. How does modern container isolation use `pivot_root` instead?

### Exercise 9.10: Reconstructing Docker: Five Primitives in One Command
Combine all 5 primitives using `unshare`:
```bash
sudo unshare --pid --uts --mount --net --fork /bin/bash
```
Identify how this single command sets up the identical namespace foundation used by `docker run`.

### Exercise 9.11: Measuring CPU L1/L2 Cache Latency
Write a program that traverses arrays of varying sizes (from 8KB to 64MB) with random strides. Plot access latency per element. Identify the abrupt step changes corresponding to L1 cache (32KB), L2 cache (512KB), L3 cache (16MB), and physical DRAM.

### Exercise 9.12: False Sharing Elimination
Create 2 threads that mutate two adjacent `uint64_t` integers in a struct. Compare performance against a struct where each integer is aligned to 64 bytes (`alignas(64)`). Measure with `perf stat -e cache-misses`.

### Exercise 9.13: Branch Prediction Penalty
Create an array of 1,000,000 random integers. Compare the time required to sum elements that are $> 128$:
1. With an unsorted array (branch predictor fails ~50% of the time).
2. With a sorted array (branch predictor achieves near 100% accuracy).
Measure branch misses using `perf stat -e branch-misses`.

### Exercise 9.14: Syscall Frequency Bottleneck
Write two programs that process 1MB of text:
1. Program A calls `read()` 1 byte at a time (1,000,000 syscalls).
2. Program B calls `read()` 64KB at a time (16 syscalls).
Compare CPU time spent in userspace vs system time using `/usr/bin/time -v`.

### Exercise 9.15: Profiling with Flamegraphs
Use Linux `perf record -g` and `perf report` on an intentionally inefficient CPU-bound binary. Identify the hottest function in the stack backtrace and explain why optimization should be guided by profiler data rather than guesswork.
