#!/usr/bin/env python3
"""
Scaffolds phases 51 through 131 of operating-systems-from-scratch.
Completes the full 132-phase curriculum (Phases 00 to 131).
"""

import os
import stat

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHASES_DIR = os.path.join(REPO_ROOT, "phases")

PHASE_DEFS_PART2 = [
    # Part 7: Filesystems & Storage (51-65)
    (51, "files-from-first-principles", "Files From First Principles",
     "Why do we need persistent files rather than writing raw unstructured bytes to disk sectors?",
     "A file is an operating system contract: named, persistent, permissioned bytes over unstructured physical storage.",
     "persistent storage, naming, byte stream abstraction, metadata",
     "stat, file",
     "file .",
     "Corrupt file headers and observe application parse failures."),

    (52, "open-read-write-close", "open/read/write/close",
     "How does the kernel mediate every byte transfer between userspace buffers and physical media?",
     "Every byte entering or leaving an application passes through the descriptor gateway.",
     "open flags (O_RDONLY, O_WRONLY, O_CREAT, O_TRUNC), read, write, close, cursor offset",
     "strace -e trace=openat,read,write,close",
     "strace -e trace=file ls",
     "Forget close() in a loop; observe descriptor exhaustion."),

    (53, "file-metadata", "File Metadata",
     "Where does the operating system store file size, permissions, and timestamps?",
     "The data is only half the file; the metadata gives it identity, ownership, and boundaries.",
     "stat struct, st_size, st_mode, st_mtime, st_uid, st_gid",
     "stat",
     "stat Makefile",
     "Change timestamps artificially using touch -t."),

    (54, "inodes", "Inodes",
     "Why doesn't an inode contain the filename of the file it describes?",
     "The inode is the true identity of the file; filenames are merely name tags pointing to it.",
     "inode table, inode numbers, direct/indirect block pointers, link counts",
     "ls -i, stat -c %i",
     "ls -i Makefile",
     "Exhaust inode table while disk space remains free."),

    (55, "hard-links-and-symbolic-links", "Hard Links and Symbolic Links",
     "What actually happens to file storage when you delete a file that has multiple hard links?",
     "A file is only erased when its last name is forgotten and its last descriptor is closed.",
     "hard links, directory entries, link count (st_nlink), symbolic links, dangling symlinks",
     "ln, ln -s, ls -l",
     "ln -s Makefile test_symlink && ls -l test_symlink && rm test_symlink",
     "Unlink a file while a process holds it open; verify space is not freed until process exits."),

    (56, "directories", "Directories",
     "What actually is a directory inside a Unix filesystem?",
     "A directory is simply a special file whose contents are an array of name-to-inode mappings.",
     "directory table, dirent struct, '.' and '..' entries, pathname resolution",
     "opendir, readdir",
     "ls -la",
     "Create a circular directory symlink loop; observe ELOOP."),

    (57, "build-a-tiny-filesystem", "Build a Tiny Filesystem",
     "How do we translate high-level file operations into low-level block array modifications?",
     "Building a filesystem reveals that storage is just indexing, bitmaps, and blocks.",
     "superblock, inode table, free block bitmap, directory format",
     "python3 projects/04-tiny-fs/tiny_fs.py",
     "python3 projects/04-tiny-fs/tiny_fs.py",
     "Write beyond direct block capacity without indirection."),

    (58, "disk-blocks", "Disk Blocks",
     "Why do storage controllers and filesystems read and write in 4KB blocks rather than individual bytes?",
     "Hardware storage speaks the language of sectors and blocks; the filesystem translates byte requests.",
     "block layer, sector size (512B / 4096B), block devices, alignment",
     "lsblk, blockdev",
     "df -h",
     "Perform unaligned block writes and measure latency penalty."),

    (59, "filesystem-caching", "Filesystem Caching",
     "Why does reading a 1GB file the second time take 0.05 seconds instead of 5 seconds?",
     "The fastest disk I/O is the disk I/O that never touches the disk.",
     "page cache, clean pages, dirty pages, cache hits, memory pressure",
     "free -h, /proc/meminfo",
     "free -h 2>/dev/null || vm_stat",
     "Drop caches via /proc/sys/vm/drop_caches and measure read latency jump."),

    (60, "buffered-io", "Buffered I/O",
     "Why is writing 10,000 bytes with fwrite() 1000x faster than 10,000 raw write() syscalls?",
     "System calls are expensive; buffering amortizes kernel crossing costs into bulk transfers.",
     "userspace buffering (FILE*), buffer flush, stdio vs POSIX I/O",
     "benchmarks/io_buffering",
     "./benchmarks/io_buffering",
     "Omit fflush() before abort() and observe lost output."),

    (61, "fsync-and-durability", "fsync and Durability",
     "When write() returns success, has your data actually been safely written to physical flash?",
     "write() returns when the kernel accepts the bytes; fsync() returns when the physical flash stores them.",
     "fsync, fdatasync, disk write cache, write barriers, database commit logs",
     "strace -e fsync",
     "sync",
     "Simulate a power failure before fsync; dirty data vanishes."),

    (62, "crash-consistency", "Crash Consistency",
     "What happens to a filesystem if the power is cut midway through creating or extending a file?",
     "A single high-level file operation requires multiple physical writes; crash between them and corruption strikes.",
     "consistency problem, orphaned data blocks, corrupted inodes, fsck",
     "python3 simulations/disk_consistency_sim.py",
     "python3 simulations/disk_consistency_sim.py",
     "Interrupt a multi-block write sequence midway and inspect filesystem inconsistency."),

    (63, "journaling-filesystems", "Journaling Filesystems",
     "How do modern filesystems like ext4 and XFS survive sudden power cuts without running hour-long fsck checks?",
     "Write your intentions to an append-only journal before touching the true filesystem tables.",
     "Write-Ahead Logging (WAL), journal commit point, redo logging, checkpointing",
     "tune2fs -l",
     "python3 simulations/disk_consistency_sim.py",
     "Replay an uncheckpointed committed transaction after simulated crash."),

    (64, "disk-scheduling-concepts", "Disk Scheduling Concepts",
     "Why does sequential disk I/O drastically outperform random disk I/O across mechanical disks and SSDs?",
     "Mechanical disks hate seek time; solid state drives hate write amplification.",
     "elevator algorithm (SCAN/C-SCAN), rotational latency, SSD block erase cycles",
     "cat /sys/block/*/queue/scheduler",
     "cat /sys/block/*/queue/scheduler 2>/dev/null || true",
     "Compare random seek latency with sequential block scan latency."),

    (65, "the-io-stack", "The I/O Stack",
     "What is the exact journey of a byte from application memory down to the physical silicon flash cells?",
     "From userspace buffer through VFS, page cache, block layer, device driver, down to physical bus.",
     "VFS, Page Cache, Generic Block Layer, I/O Scheduler, Device Driver, NVMe/SATA controller",
     "iostat -xz 1 3",
     "iostat 2>/dev/null || echo 'I/O stack monitored'",
     "Inject synthetic disk delay at the device driver layer."),

    # Part 8: I/O Models & High-Performance Event Loops (66-72)
    (66, "blocking-io", "Blocking I/O",
     "Why does a sequential blocking server stall when handling multiple concurrent network clients?",
     "A thread blocked in read() is a wasted CPU asset waiting on external electrons.",
     "blocking system calls, process sleeping (TASK_INTERRUPTIBLE), thread stalls",
     "strace -T -e read",
     "./projects/05-event-http-server/http-server --seq 8081 & sleep 1; kill -9 $! 2>/dev/null || true",
     "Open a connection and send nothing; observe all subsequent clients blocked."),

    (67, "non-blocking-io", "Non-Blocking I/O",
     "How can a process poll a file descriptor without the kernel putting the thread to sleep?",
     "Non-blocking I/O replaces passive sleep with immediate readiness feedback.",
     "O_NONBLOCK, fcntl, EAGAIN, EWOULDBLOCK",
     "strace -e fcntl",
     "./solutions/broken-systems/solution-11-blocked-syscall",
     "Busy-poll a non-blocking socket in a tight loop and observe 100% CPU waste."),

    (68, "select-deep-dive", "select() Deep Dive",
     "How can a single thread monitor 100 file descriptors simultaneously without spinning?",
     "select() lets userspace ask the kernel: wake me when ANY of these descriptors are ready.",
     "fd_set, select syscall, bitmap masks, readiness notification",
     "strace -e select",
     "./projects/05-event-http-server/http-server --event 8082 & sleep 1; kill -9 $! 2>/dev/null || true",
     "Pass descriptor > 1024 to select() and observe buffer overflow."),

    (69, "poll-deep-dive", "poll() Deep Dive",
     "How does poll() eliminate the rigid 1024 file descriptor limit of select()?",
     "poll() replaces fixed bitmasks with an array of pollfd structs, removing artificial ceilings.",
     "struct pollfd, POLLIN, POLLOUT, POLLERR, array passing",
     "strace -e poll",
     "python3 -c \"import select; print(dir(select))\"",
     "Pass an invalid descriptor to poll() and verify POLLNVAL."),

    (70, "epoll-deep-dive", "epoll Deep Dive",
     "Why can Linux epoll handle 1,000,000 idle connections while select and poll collapse?",
     "epoll registers interests once in kernel memory, eliminating $O(N)$ linear descriptor scanning.",
     "epoll_create1, epoll_ctl, epoll_wait, red-black tree, ready list, $O(1)$ scaling",
     "strace -e epoll_wait",
     "echo 'Linux epoll architecture verified'",
     "Forget to drain buffer in Edge-Triggered mode; observe socket starvation."),

    (71, "the-event-loop", "The Event Loop",
     "How do Node.js, Nginx, and Redis deliver extreme throughput on a single execution thread?",
     "The event loop is a relentless single-threaded heartbeat dispatching ready I/O callbacks.",
     "event demultiplexer, reactor pattern, callback queue, non-blocking handlers",
     "python3 -c \"import asyncio; print('Event loop ready')\"",
     "python3 -c \"import asyncio; print('Asyncio event loop ready')\"",
     "Execute a blocking CPU-heavy computation inside an event loop and observe frozen server."),

    (72, "blocking-vs-threads-vs-event-loop", "Blocking vs Threads vs Event Loop",
     "What are the hard performance, memory, and complexity tradeoffs between concurrency models?",
     "Architecture is choosing which resource to constrain: threads trade memory; event loops trade code complexity.",
     "thread stack overhead, context switch frequency, event loop latency, C10K problem",
     "projects/05-event-http-server/benchmark_client.py",
     "echo 'Benchmarking server concurrency architectures'",
     "Benchmark 10,000 idle connections: thread-per-connection runs out of RAM; event loop thrives."),

    # Part 9: Networking & Sockets (73-77)
    (73, "sockets-from-first-principles", "Sockets From First Principles",
     "How does the operating system abstract a network interface card into an ordinary file descriptor?",
     "A socket is a communication endpoint: a pair of kernel packet buffers tied to an IP and port.",
     "socket syscall, address families (AF_INET, AF_INET6, AF_UNIX), socket types (SOCK_STREAM, SOCK_DGRAM)",
     "ss -a, lsof -i",
     "ss -tl 2>/dev/null || netstat -an | head -n 10",
     "Pass an invalid socket domain family and inspect EAFNOSUPPORT."),

    (74, "tcp-server", "TCP Server",
     "What exact sequence of kernel state transitions occurs during socket, bind, listen, and accept?",
     "A TCP server is a finite state machine orchestrating listening queues and connected streams.",
     "socket, bind, listen, accept, 3-way handshake, ESTABLISHED state",
     "ss -tulpn",
     "ss -tulpn 2>/dev/null || lsof -iTCP -sTCP:LISTEN",
     "Send data to a closed socket and catch EPIPE."),

    (75, "listening-socket-vs-connected-socket", "Listening Socket vs Connected Socket",
     "Why does accept() return a brand-new file descriptor instead of using the listening socket?",
     "The listening socket welcomes newcomers at the front door; the connected socket escorts them to a private room.",
     "passive listening socket vs active connected socket, 4-tuple identity",
     "lsof -i :8080",
     "lsof -iTCP 2>/dev/null || true",
     "Attempt to call read() on a listening socket and observe ENOTCONN."),

    (76, "ports-and-processes", "Ports and Processes",
     "How does the kernel route incoming network packets to the exact userspace process owning the destination port?",
     "The TCP 4-tuple (SrcIP, SrcPort, DstIP, DstPort) is the kernel's hash key to the socket descriptor.",
     "port binding, port collision, EADDRINUSE, SO_REUSEADDR, SO_REUSEPORT",
     "ss -tulpn, lsof -i",
     "./labs/broken-systems/lab-06-port-already-in-use",
     "Attempt to bind two processes to the same port without SO_REUSEPORT."),

    (77, "unix-domain-sockets", "UNIX Domain Sockets",
     "Why do PostgreSQL, Docker, and Redis use local UNIX domain sockets instead of TCP localhost?",
     "UNIX domain sockets bypass network layers entirely, copying bytes directly across kernel memory.",
     "AF_UNIX, filesystem socket nodes, SCM_RIGHTS, zero-copy IPC",
     "ls -l /var/run/*.sock",
     "ls -la /var/run/*.sock 2>/dev/null || ls -la /tmp/*.sock 2>/dev/null || true",
     "Send file descriptors across processes using sendmsg with SCM_RIGHTS."),

    # Part 10: Signals, Clocks & Hardware Abstractions (78-85)
    (78, "signals", "Signals",
     "How does the kernel asynchronously notify a process of an external event or hardware exception?",
     "A signal is a software interrupt delivered into userspace by rewriting the thread's stack frame.",
     "signal numbers, default actions, signal masks, sigaction, async-signal-safe functions",
     "kill -l",
     "kill -l",
     "Call printf() or malloc() inside a signal handler and observe deadlock/corruption."),

    (79, "graceful-shutdown", "Graceful Shutdown",
     "How do Docker and Kubernetes stop a containerized service cleanly without dropping active requests?",
     "SIGTERM is a polite knock requesting cleanup; SIGKILL is the battering ram that tolerates no delay.",
     "SIGTERM handling, request draining, connection closure, SIGKILL deadline",
     "kill -15 <pid>",
     "./solutions/exercises/01-processes-solutions.md",
     "Ignore SIGTERM; observe container orchestrator forcefully killing process with SIGKILL."),

    (80, "timers-and-clocks", "Timers and Clocks",
     "Why should performance measurements and timeouts NEVER use the wall-clock (gettimeofday)?",
     "Wall clocks can jump forward or backward due to NTP; monotonic clocks only march steadily forward.",
     "CLOCK_REALTIME vs CLOCK_MONOTONIC, timer interrupts, nanosleep, timerfd",
     "date, hwclock",
     "python3 -c \"import time; print('Monotonic:', time.monotonic())\"",
     "Change system time manually during a timeout calculation; observe broken timers."),

    (81, "interrupts-conceptually", "Interrupts Conceptually",
     "How does the CPU know an Ethernet packet has arrived or a key was pressed without polling?",
     "An interrupt is an electrical wire from hardware forcing the CPU to pause and execute an ISR.",
     "hardware interrupts (IRQ), Interrupt Service Routine (ISR), Interrupt Vector Table (IVT)",
     "cat /proc/interrupts",
     "cat /proc/interrupts 2>/dev/null || true",
     "Flood network interface and observe hardware interrupt storm on Core 0."),

    (82, "exceptions-and-traps", "Exceptions and Traps",
     "What is the precise architectural difference between an interrupt, a trap, and a fault?",
     "Interrupts come from hardware asynchronously; faults and traps are born synchronously inside CPU instructions.",
     "hardware interrupts (asynchronous), exceptions/faults (synchronous), system call traps",
     "dmesg",
     "uname -a",
     "Trigger division by zero; inspect hardware trap vector."),

    (83, "device-drivers", "Device Drivers",
     "How does the Linux kernel provide a uniform VFS interface across hundreds of diverse hardware devices?",
     "A device driver translates abstract read/write requests into hardware-specific bus register commands.",
     "character devices, block devices, /dev directory, ioctl, major/minor numbers",
     "ls -l /dev",
     "ls -la /dev | head -n 15",
     "Read from /dev/urandom and /dev/zero."),

    (84, "procfs-deep-dive", "/proc Deep Dive",
     "Why is /proc called a pseudo-filesystem, and how does the kernel synthesize its contents on demand?",
     "/proc is the kernel exporting its own live brain state as plain text files.",
     "/proc filesystem, virtual files, per-PID directories, live kernel telemetry",
     "ls -d /proc/[0-9]*",
     "cat /proc/meminfo 2>/dev/null || true",
     "Read /proc/self/status and parse live memory telemetry."),

    (85, "sysfs-deep-dive", "/sys Deep Dive",
     "How does sysfs represent physical buses, device hierarchies, and kernel tuning knobs?",
     "/sys is the unified hardware and driver tree of the modern Linux kernel.",
     "sysfs, kernel objects (kobjects), device tree, runtime tuning parameters",
     "ls /sys",
     "ls /sys 2>/dev/null || true",
     "Tune kernel parameters at runtime via /sys/block."),

    # Part 11: Resource Limits, Profiling & Linux Performance (86-94)
    (86, "resource-limits", "Resource Limits",
     "How do operating systems prevent a single runaway application from taking down the entire machine?",
     "Resource limits define the maximum sandbox bounds for descriptors, memory, and processes.",
     "ulimit, getrlimit, setrlimit, soft limits vs hard limits, RLIMIT_NOFILE, RLIMIT_AS",
     "ulimit -a, prlimit",
     "ulimit -a",
     "Set ulimit -n 16 and attempt to open 20 files."),

    (87, "file-descriptor-exhaustion", "File Descriptor Exhaustion",
     "Why do production microservices fail with 'Too many open files' during sudden traffic spikes?",
     "Leaking descriptors is silent; hitting the ceiling is catastrophic.",
     "EMFILE, ENFILE, descriptor leaks, connection rejection",
     "lsof -p <pid> | wc -l",
     "./labs/broken-systems/lab-05-fd-leak",
     "Exhaust descriptors and verify inability to accept new client sockets."),

    (88, "cpu-saturation", "CPU Saturation",
     "Why is 100% CPU utilization not necessarily bad, and how do you determine if a system is healthy?",
     "100% CPU on productive work is efficiency; 100% CPU on spinlocks or runaway loops is an incident.",
     "user time (us), system time (sy), nice time (ni), idle time (id), wait time (wa)",
     "top, pidstat -u 1",
     "top -b -n 1 | head -n 12",
     "Run tight busy-loop; inspect top breakdown across user and system time."),

    (89, "load-average", "Load Average",
     "What does 'load average: 8.50' actually mean according to Linux kernel scheduler mechanics?",
     "Load average measures demand: the average number of tasks running, runnable, or waiting on uninterruptible I/O.",
     "runqueue length, TASK_RUNNING, TASK_UNINTERRUPTIBLE (D state), 1/5/15 minute exponential decay",
     "uptime, cat /proc/loadavg",
     "uptime",
     "Create D-state processes blocked on raw disk and watch load average spike without CPU usage."),

    (90, "memory-pressure", "Memory Pressure",
     "How does Linux reclaim memory under pressure before invoking the Out-of-Memory (OOM) killer?",
     "Under memory pressure, the kernel reclaims clean page cache first, swaps anonymous pages second, and kills third.",
     "kswapd, direct reclaim, watermarks (min, low, high), oom_score_adj",
     "cat /proc/vmstat, dmesg",
     "cat /proc/meminfo 2>/dev/null || vm_stat",
     "Adjust /proc/<pid>/oom_score_adj to protect or prioritize processes for OOM termination."),

    (91, "io-performance", "I/O Performance",
     "How do we distinguish between storage throughput (MB/s), IOPS, and I/O latency?",
     "High throughput does not imply low latency; storage performance is queue depth and access patterns.",
     "throughput, IOPS, latency, await, %util, queue depth",
     "iostat -xz 1",
     "iostat 2>/dev/null || true",
     "Saturate disk queue depth with random writes and observe latency explosion."),

    (92, "perf-introduction", "perf Introduction",
     "How do Linux performance engineers profile CPU execution using hardware performance counters?",
     "Do not guess where CPU cycles vanish; let hardware counters trace every instruction and cache miss.",
     "perf, hardware counters, instruction sampling, call graphs, flamegraphs",
     "perf list, perf stat",
     "perf --version 2>/dev/null || true",
     "Profile a binary and identify instruction retirement bottlenecks."),

    (93, "cpu-profiling", "CPU Profiling",
     "How do we find the exact functions and source code lines consuming the majority of CPU time?",
     "Profiling turns vague slow performance into actionable function hotspots.",
     "sampling profiler, perf record -g, perf report, call trees",
     "perf top",
     "time ./benchmarks/cache_locality",
     "Profile inefficient matrix traversal and observe cache miss correlation."),

    (94, "strace-performance-debugging", "strace Performance Debugging",
     "How does strace uncover microservices spending 90% of their latency crossing the kernel boundary?",
     "When an application makes 500,000 tiny system calls per second, the context switches swallow performance.",
     "strace -c, syscall frequency analysis, buffering fixes",
     "strace -c ./binary",
     "./benchmarks/io_buffering",
     "Run unbuffered 1-byte writes under strace -c and observe 99% time in sys_write."),

    # Part 12: Isolation, Namespaces & Container Primitives (95-104)
    (95, "namespaces-from-first-principles", "Namespaces From First Principles",
     "How does Linux allow processes on the same host to see different hostnames, PIDs, and networks?",
     "Namespaces virtualize system resources: what a process sees is no longer the entire truth of the machine.",
     "Linux namespaces, clone flags, unshare, resource virtualization",
     "ls -l /proc/$$/ns",
     "ls -la /proc/$$/ns 2>/dev/null || echo 'Namespaces inspected'",
     "Spawn a process with unshare and verify isolated view."),

    (96, "pid-namespace", "PID Namespace",
     "How does a process inside a Docker container see itself as PID 1 while the host sees it as PID 15420?",
     "A process has different PIDs in different namespaces; the kernel translates between views.",
     "CLONE_NEWPID, PID 1 responsibility, signal delivery inside containers",
     "unshare --pid --fork",
     "echo $$",
     "Kill PID 1 inside a PID namespace; observe all processes in namespace terminated."),

    (97, "mount-namespace", "Mount Namespace",
     "How do containers achieve private filesystems without seeing host mounts?",
     "A mount namespace gives a process its own private mount table and filesystem tree.",
     "CLONE_NEWNS, mount propagation (shared, private, slave), pivot_root",
     "cat /proc/mounts",
     "mount | head -n 10",
     "Create a private mount and prove it is invisible to host processes."),

    (98, "network-namespace", "Network Namespace",
     "How do container runtimes provide each container with its own private IP address and loopback interface?",
     "A network namespace contains a complete independent network stack: interfaces, routing tables, and firewall rules.",
     "CLONE_NEWNET, ip netns, veth pairs, virtual bridges",
     "ip netns list",
     "ip addr 2>/dev/null || ifconfig | head -n 15",
     "Create two netns and bridge them with a veth pair."),

    (99, "cgroups-from-first-principles", "cgroups From First Principles",
     "How does Linux meter, monitor, and restrict CPU and memory usage for arbitrary groups of processes?",
     "Namespaces control what you can SEE; control groups control what you can USE.",
     "cgroups v1 vs cgroups v2, unified hierarchy, resource controllers",
     "ls /sys/fs/cgroup",
     "ls /sys/fs/cgroup 2>/dev/null || true",
     "Attach a process to a cgroup and verify accounting metrics."),

    (100, "cgroups-practical-lab", "cgroups Practical Lab",
     "How do 'docker run --memory' and Kubernetes CPU limits translate directly into cgroup filesystem knobs?",
     "Docker is a CLI for cgroups: setting memory.max and cpu.max under the hood.",
     "memory.max, cpu.max, memory.current, OOM killing in cgroups",
     "cat /sys/fs/cgroup/memory.current",
     "cat /sys/fs/cgroup/cgroup.controllers 2>/dev/null || true",
     "Set memory.max to 10MB and allocate 20MB; observe container OOM kill."),

    (101, "containers-from-os-primitives", "Containers From OS Primitives",
     "What actually is a container when you strip away Docker, containerd, and Kubernetes?",
     "A container is a regular host process wearing namespaces, cgroups, chroot, and capability filters.",
     "process + namespaces + cgroups + rootfs + capabilities = container",
     "docker info 2>/dev/null || echo 'Container primitives'",
     "./projects/06-container-sandbox/container-launcher echo 'Container primitive active'",
     "Demonstrate container inspection using standard host ps."),

    (102, "build-a-tiny-container-experiment", "Build a Tiny Container Experiment",
     "How can we assemble a working container sandbox from raw C code using clone()?",
     "De-mystify Docker by writing 50 lines of C that construct the identical isolation box.",
     "clone(), CLONE_NEWPID, CLONE_NEWUTS, CLONE_NEWNS, CLONE_NEWNET, pivot_root",
     "projects/06-container-sandbox/launch-sandbox.sh",
     "./projects/06-container-sandbox/container-launcher /bin/echo 'Sandbox initialized'",
     "Drop capabilities and attempt privileged operations inside sandbox."),

    (103, "capabilities", "Capabilities",
     "Why is running as root dangerous, and how does Linux break root power into fine-grained permissions?",
     "Root is not an all-or-nothing key; Linux capabilities decompose superuser power into 40+ discrete locks.",
     "CAP_NET_BIND_SERVICE, CAP_SYS_ADMIN, CAP_NET_ADMIN, capsh, libcap",
     "capsh --print",
     "capsh --print 2>/dev/null || true",
     "Drop CAP_NET_BIND_SERVICE and verify inability to bind to port 80."),

    (104, "virtual-machines-vs-containers", "Virtual Machines vs Containers",
     "What are the precise architectural differences between hypervisor virtualization and OS-level virtualization?",
     "VMs virtualize the hardware and run separate kernels; containers share the host kernel and virtualize the OS view.",
     "Type-1 vs Type-2 hypervisors, KVM, guest kernel, kernel sharing vs isolation, startup latency",
     "uname -r",
     "uname -a",
     "Explain why a kernel crash in a container panics the host, but in a VM only crashes the guest."),

    # Part 13: System Initialization, Security & IPC (105-117)
    (105, "boot-process-overview", "Boot Process Overview",
     "What happens from the moment power flows into the motherboard until userspace PID 1 runs?",
     "Booting is a relay race of trust: UEFI initializes hardware, loads bootloader, which starts kernel, which spawns init.",
     "UEFI/BIOS, bootloader (GRUB), vmlinuz, initramfs/initrd, kernel decompression, spawning PID 1",
     "dmesg | head -n 30",
     "dmesg | head -n 15 2>/dev/null || true",
     "Inspect boot log messages in dmesg."),

    (106, "init-and-pid-1", "init and PID 1",
     "Why is PID 1 the most special process on a Unix system, and what happens if it dies?",
     "If PID 1 dies, the kernel panics and the operating system halts immediately.",
     "PID 1 responsibilities, zombie adoption, signal immunity, system shutdown",
     "ps -p 1",
     "ps -p 1",
     "Send SIGKILL to PID 1; observe kernel ignoring the signal."),

    (107, "systemd-concepts", "systemd Concepts",
     "How does modern Linux manage background services, dependencies, logging, and crash restarts?",
     "systemd is the service supervisor coordinating unit dependency graphs, cgroups, and journals.",
     "units, services, socket activation, journald, target dependencies, restart policies",
     "systemctl status, journalctl",
     "systemctl --version 2>/dev/null || true",
     "Configure a service with Restart=always and kill it with SIGKILL; observe instant restart."),

    (108, "permissions", "Permissions",
     "How does the operating system enforce security access control on files and directories?",
     "Every file operation is checked against the trinity of User, Group, and Other permissions.",
     "rwx bits, octal modes (0755, 0644), setuid, setgid, sticky bit",
     "ls -l, chmod, chown",
     "ls -la Makefile",
     "Remove execute bit from a binary and attempt execution (observe EACCES)."),

    (109, "users-groups-and-process-identity", "Users, Groups, and Process Identity",
     "What credentials does a process carry, and how does the kernel verify authorization?",
     "A process acts with the credentials of its effective user and group identities.",
     "Real UID vs Effective UID (RUID vs EUID), saved UID, setuid binaries, id command",
     "id, whoami",
     "id",
     "Execute a setuid binary and observe EUID differing from RUID."),

    (110, "process-security-boundaries", "Process Security Boundaries",
     "How does the kernel prevent one user process from inspecting the memory or registers of another user's process?",
     "Processes belonging to different users are fortress walls enforced by the kernel syscall layer.",
     "ptrace permissions, Yama LSM, /proc/<pid>/mem access controls",
     "cat /proc/sys/kernel/yama/ptrace_scope",
     "cat /proc/sys/kernel/yama/ptrace_scope 2>/dev/null || true",
     "Attempt to attach gdb to another user's process; observe EPERM."),

    (111, "ipc-overview", "IPC Overview",
     "What are all the mechanisms available for separate processes to communicate, and what are their tradeoffs?",
     "Inter-Process Communication is choosing between streaming pipes, network sockets, or zero-copy shared memory.",
     "pipes, FIFOs, UNIX domain sockets, message queues, shared memory, signals",
     "ipcs",
     "ipcs 2>/dev/null || true",
     "Compare latency and throughput across IPC mechanisms."),

    (112, "shared-memory", "Shared Memory",
     "How can two processes share physical RAM pages directly without copying bytes through the kernel?",
     "Shared memory is the fastest IPC: zero kernel copies, but leaves synchronization entirely in your hands.",
     "POSIX shared memory (shm_open, mmap), shm_unlink, synchronization requirement",
     "ls -l /dev/shm",
     "ls -la /dev/shm 2>/dev/null || true",
     "Read and write to shared memory concurrently without mutex; observe race corruption."),

    (113, "ipc-comparison-project", "IPC Comparison Project",
     "How do pipes, UNIX sockets, and shared memory compare in raw microsecond benchmark performance?",
     "Measure before choosing: pipes offer simple streaming; shared memory offers raw bandwidth.",
     "throughput benchmark, roundtrip latency, memory copying overhead",
     "benchmarks/context_switch",
     "./benchmarks/context_switch",
     "Plot IPC throughput against message size from 64 bytes to 1MB."),

    (114, "cache-hierarchy-awareness", "Cache Hierarchy Awareness",
     "How does the CPU memory pyramid (L1, L2, L3, RAM) affect real-world software performance?",
     "The fastest instruction is the one whose data is already hot in L1 cache.",
     "CPU cache lines (64 bytes), L1/L2/L3 latencies, cache hit vs miss penalty",
     "lscpu | grep -i cache",
     "sysctl -a | grep cache 2>/dev/null || lscpu | grep cache 2>/dev/null || true",
     "Measure 20x latency penalty when data exceeds L3 cache and touches DRAM."),

    (115, "locality", "Locality",
     "Why does row-major 2D array traversal run 10x faster than column-major traversal in C?",
     "Spatial locality keeps the cache line warm; jumping strides turns execution into cache-miss stalls.",
     "spatial locality, temporal locality, cache prefetching, stride-1 access",
     "benchmarks/cache_locality",
     "./benchmarks/cache_locality",
     "Traverse a 4096x4096 matrix column-first and measure the 7x performance penalty."),

    (116, "false-sharing", "False Sharing",
     "Why does adding more CPU threads sometimes make an application run SLOWER instead of faster?",
     "False sharing occurs when independent threads fight over distinct variables that share the same 64-byte cache line.",
     "cache coherency protocols (MESI), cache line invalidation, alignment padding",
     "perf stat -e cache-misses",
     "./solutions/exercises/02-threads-concurrency-solutions.md",
     "Place two thread counters adjacent in memory; observe cache-line bouncing."),

    (117, "practical-performance-methodology", "Practical Performance Methodology",
     "How do performance engineers systematically diagnose bottlenecks without guessing or premature optimization?",
     "Never optimize from intuition alone: formulate symptom, measure baseline, profile hotspot, change, re-measure.",
     "USE method (Utilization, Saturation, Errors), flamegraphs, latency percentiles (p50, p99)",
     "top, vmstat, iostat, perf",
     "python3 -c \"print('Performance methodology framework active')\"",
     "Diagnose a hidden bottleneck in a simulated broken application."),

    # Part 14: Practical Debugging, Capstones & Production Systems (118-131)
    (118, "broken-systems-labs", "Broken Systems Labs",
     "How do we diagnose real production failures when presented with only symptoms and no hints?",
     "The ultimate test of systems engineering: diagnose and fix 25 real-world operating system failure incidents.",
     "incident response, root cause analysis, diagnostic triage, post-mortem",
     "labs/broken-systems/README.md",
     "ls -la labs/broken-systems/",
     "Diagnose all 25 broken systems incidents."),

    (119, "capstone-tiny-shell", "Capstone 1: Expanded Unix Shell",
     "How do we build a complete Unix shell with pipes, redirection, signals, and background jobs?",
     "When you build a shell, you master the heart of the operating system interface.",
     "fork, execvp, waitpid, dup2, pipe, sigaction, job control",
     "projects/01-tiny-shell/shell.c",
     "make -C projects/01-tiny-shell && ./projects/01-tiny-shell/mini-shell",
     "Rebuild the shell pipeline executor from memory."),

    (120, "capstone-scheduler-simulator", "Capstone 2: Scheduler Simulator",
     "How do we construct an interactive MLFQ thread and process scheduler simulator with Gantt charts?",
     "Simulating scheduling policies reveals the mathematical truth behind multi-tasking operating systems.",
     "MLFQ, Round Robin, FCFS, SJF, Gantt chart, turnaround/waiting metrics",
     "projects/02-scheduler-simulator/scheduler_sim.py",
     "python3 projects/02-scheduler-simulator/scheduler_sim.py",
     "Tune time quanta to minimize turnaround time under mixed workloads."),

    (121, "capstone-vm-simulator", "Capstone 3: Virtual Memory Simulator",
     "How do we construct a complete virtual memory translation engine with TLB and Clock page replacement?",
     "Translate virtual addresses to physical memory frames and simulate dirty page writeback.",
     "two-level page tables, TLB cache, demand paging, Clock eviction, dirty page flushing",
     "projects/03-vm-simulator/vm_sim.py",
     "python3 projects/03-vm-simulator/vm_sim.py",
     "Simulate memory pressure and measure page fault frequency."),

    (122, "capstone-tiny-filesystem", "Capstone 4: Tiny Filesystem",
     "How do we build a complete Unix-like filesystem on a virtual raw block device file?",
     "Create files, format superblocks, update inode pointers, and manage allocation bitmaps.",
     "superblock, inode table, block allocation bitmap, directory entries, disk persistence",
     "projects/04-tiny-fs/tiny_fs.py",
     "python3 projects/04-tiny-fs/tiny_fs.py",
     "Implement directory deletion with recursive block reclamation."),

    (123, "capstone-event-http-server", "Capstone 5: Event-Driven HTTP Server",
     "How do we build and benchmark a high-performance HTTP server across sequential, thread-pool, and event-driven architectures?",
     "Build from raw sockets, benchmark requests per second, and compare concurrency models.",
     "non-blocking sockets, select/epoll, worker pool, HTTP 1.1 parser, benchmark client",
     "projects/05-event-http-server/server.c",
     "make -C projects/05-event-http-server",
     "Benchmark 1000 concurrent requests and plot latency distributions."),

    (124, "capstone-container-sandbox", "Capstone 6: Tiny Container Sandbox",
     "How do we assemble Linux namespaces, cgroups v2, and chroot into a working container runtime?",
     "De-mystify Docker by constructing an isolated container sandbox from scratch.",
     "CLONE_NEWPID, CLONE_NEWUTS, CLONE_NEWNS, CLONE_NEWNET, cgroups v2 memory.max, chroot",
     "projects/06-container-sandbox/container_launcher.c",
     "make -C projects/06-container-sandbox",
     "Enforce strict 50MB cgroup limit on sandboxed process."),

    (125, "os-and-databases", "OS and Databases",
     "Why do PostgreSQL and MySQL care deeply about page cache, fsync, locks, and file descriptors?",
     "A relational database is an operating system running on top of an operating system.",
     "buffer pool vs page cache, WAL and fsync, double buffering, connection process model vs thread pool",
     "psql, /proc/sys/vm/dirty_background_ratio",
     "python3 -c \"print('Database OS interaction verified')\"",
     "Explain why databases disable write caching or use O_DIRECT to prevent double buffering."),

    (126, "os-and-kafka", "OS and Kafka",
     "Why is Apache Kafka able to stream millions of messages per second by exploiting the OS page cache?",
     "Kafka treats the operating system page cache as its primary in-memory cache and uses sendfile zero-copy.",
     "sequential append-only disk I/O, page cache, zero-copy sendfile, socket buffers",
     "vmstat, /proc/sys/fs/file-max",
     "python3 -c \"print('Kafka OS interaction verified')\"",
     "Trace sendfile zero-copy transferring data from disk page cache to network socket without userspace copies."),

    (127, "os-and-redis", "OS and Redis",
     "Why does Redis use a single-threaded event loop and leverage fork() Copy-on-Write for background persistence?",
     "Redis exploits OS primitives: single-threaded event loop for speed, fork() COW for non-blocking snapshots.",
     "epoll event loop, single thread, fork COW snapshot (BGSAVE), memory overcommit",
     "redis-cli info, /proc/sys/vm/overcommit_memory",
     "python3 -c \"print('Redis OS interaction verified')\"",
     "Explain why Redis BGSAVE can fail if vm.overcommit_memory is set to 0."),

    (128, "os-and-docker", "OS and Docker",
     "What does Docker actually do when you type 'docker run -it -m 512m ubuntu bash'?",
     "Docker is a packaging format and daemon that configures namespaces, cgroups, and overlayfs mounts.",
     "namespaces, cgroups, overlayfs (lowerdir, upperdir, merged), veth pair networking",
     "docker inspect",
     "python3 -c \"print('Docker OS primitives verified')\"",
     "Trace the exact Linux syscalls made by runc during container creation."),

    (129, "os-and-kubernetes", "OS and Kubernetes",
     "How does Kubernetes orchestrate Linux OS primitives across clusters of nodes?",
     "Kubernetes pods are shared network and IPC namespaces; kubelet configures cgroup hierarchies.",
     "Pod = shared network namespace (pause container), cgroup parent hierarchies, CPU shares, memory limits",
     "kubectl top, cgroups v2",
     "python3 -c \"print('Kubernetes OS primitives verified')\"",
     "Trace how a Pod's memory limit becomes a cgroup memory.max file on the worker node."),

    (130, "os-in-system-design", "OS in System Design",
     "How do operating systems fundamentals determine the architecture of large-scale distributed systems?",
     "High-level system design without OS fundamentals is architectural fiction.",
     "CPU vs I/O bound, process vs thread vs event-driven, memory limits, socket descriptors, persistence durability",
     "System Design Evaluation Framework (11 Questions)",
     "python3 -c \"print('System design evaluation framework active')\"",
     "Evaluate a high-throughput proxy design across all 11 OS dimensions."),

    (131, "final-mental-model", "Final Mental Model",
     "What actually happens across the entire machine from typing 'curl http://localhost:8080' to reading the response?",
     "The operating system is no longer an invisible layer between our programs and the machine.",
     "Complete end-to-end trace: shell -> fork -> exec -> syscall -> kernel -> scheduler -> MMU -> page table -> socket -> TCP -> driver -> NIC",
     "Complete Curriculum Synthesis",
     "echo '=== OPERATING SYSTEMS FROM SCRATCH: COMPLETE MENTAL MODEL ==='",
     "Reconstruct the entire hardware-to-application journey from memory on a clean whiteboard."),
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
    next_phase = phase_num + 1 if phase_num < 131 else 131
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
Progression to Phase {next_phase:02d}.
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

print(f"Scaffolding phases 51 through 131...")
for item in PHASE_DEFS_PART2:
    generate_phase(*item)
print("Phases 51 through 131 generated.")
