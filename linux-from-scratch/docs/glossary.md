# First-Principles Linux Glossary

A rigorous reference defining foundational Linux concepts in terms of kernel abstractions and system resources.

---

### Core Concepts

- **Kernel**: The core privileged program that manages hardware resources (CPU, RAM, block devices, network controllers) and exposes services to user space via system calls.
- **User Space**: The unprivileged execution environment where applications, shells, and system services execute without direct hardware access.
- **System Call (Syscall)**: The programmatic interface between user applications and the Linux kernel (e.g. `read()`, `write()`, `openat()`, `execve()`, `clone()`).
- **Process**: An instance of a computer program in execution, possessing its own virtual address space, file descriptor table, and PID.
- **PID (Process ID)**: A positive integer assigned by the kernel to uniquely identify an active process.
- **PPID (Parent Process ID)**: The PID of the process that created this process via `fork()` / `clone()`.
- **PID 1**: The initial user-space process spawned directly by the kernel at boot (systemd in modern Linux). PID 1 adopts orphaned processes and manages system services.
- **File Descriptor (FD)**: An integer index into a process's per-process file descriptor table in the kernel, pointing to an open file description.
- **Inode (Index Node)**: A data structure on a filesystem that stores metadata about a file (size, permissions, owner, timestamps, block pointers), excluding its filename.
- **Dentry (Directory Entry)**: A kernel object associating a human-readable file name with an inode number.
- **Virtual Filesystem (VFS)**: The kernel abstraction layer that provides a uniform interface (`open`, `read`, `write`) across diverse filesystems (ext4, xfs, btrfs, procfs, sysfs).
- **`/proc` (procfs)**: A pseudo-filesystem synthesized in RAM by the kernel to expose runtime metrics, hardware details, and per-process internals.
- **`/sys` (sysfs)**: A pseudo-filesystem synthesized by the kernel representing device buses, network interfaces, and kernel objects in a structured hierarchy.
- **`/dev` (devtmpfs)**: A virtual filesystem populated by the kernel containing device nodes that allow user processes to communicate with hardware or kernel pseudo-devices.
- **Block Device**: A storage device that transfers data in fixed-size blocks with random-access capability (e.g. SSD, HDD, loop device).
- **Character Device**: A device that transfers data as an unbuffered stream of individual bytes (e.g. `/dev/urandom`, `/dev/tty`, serial ports).
- **Socket**: An endpoint for inter-process or network communication represented as a file descriptor in user space.
- **Pipe**: A unidirectional data channel implemented as an in-memory kernel circular buffer connecting the stdout of one process to the stdin of another.
- **Redirection**: Instructing the shell to adjust a process's file descriptors (0, 1, 2) before calling `execve()`.
- **Globbing**: Shell pathname expansion using wildcards (`*`, `?`, `[]`), resolved by the shell before the command is executed.
- **UID (User ID)**: An integer identifying a user account (UID 0 is root).
- **GID (Group ID)**: An integer identifying a group of users for shared permissions.
- **DAC (Discretionary Access Control)**: Traditional Linux permission model based on file ownership (User, Group, Other) and mode bits (`rwx`).
- **umask**: A bitmask that determines the default permissions stripped from newly created files and directories.
- **SUID (Set User ID)**: A special permission bit (`4000`) on an executable file that causes it to run with the permissions of the file owner (typically root) rather than the executing user.
- **SGID (Set Group ID)**: On an executable, runs with group privileges; on a directory, causes newly created files to inherit the parent directory's group ownership.
- **Sticky Bit**: On a directory (e.g. `/tmp`, mode `1777`), prevents users from deleting or renaming files unless they own the file or directory.
- **cgroups (Control Groups)**: A Linux kernel feature that isolates, prioritizes, and limits resource usage (CPU, Memory, Disk I/O, PIDs) for groups of processes.
- **Namespaces**: A Linux kernel mechanism that partitions system resources so that a group of processes sees an isolated view of the system (PID, Network, Mount, UTS, IPC, User).
- **systemd**: The dominant system and service manager for Linux, responsible for booting the system, supervising daemons, tracking cgroups, and collecting logs.
- **journald**: The systemd logging daemon that captures structured binary logs from the kernel, services, stdout/stderr, and syslog.
- **Load Average**: The average number of processes in the runnable state (`R`) or uninterruptible disk sleep state (`D`) over 1, 5, and 15 minute intervals.
- **RSS (Resident Set Size)**: The exact amount of physical RAM currently allocated and held by a process in memory.
- **VSZ (Virtual Size)**: The total virtual memory address space mapped by a process, including shared libraries and memory-mapped files.
- **Page Cache**: Transparent kernel RAM cache that stores recently read and written disk blocks to dramatically accelerate filesystem I/O.
- **OOM-Killer (Out-Of-Memory Killer)**: The kernel mechanism that terminates a process (assigning an `oom_score`) when physical RAM and Swap are entirely exhausted.
