# Systems & Operating Systems Glossary

A comprehensive reference for low-level systems programming, kernel architecture, and Linux mechanics.

---

### A
* **Address Space:** The range of discrete memory addresses accessible by a process. Under virtual memory, every user process possesses a private, isolated virtual address space.
* **ASLR (Address Space Layout Randomization):** A security defense where the kernel randomizes the starting memory positions of the stack, heap, and libraries on each program invocation.
* **Atomicity:** A property of an operation ensuring it completes entirely or not at all, with no observable intermediate state to concurrent observers.

### B
* **BSS Segment (Block Started by Symbol):** The portion of an object file or process memory holding statically allocated, uninitialized global variables, initialized to zero by the kernel.
* **Buffer Cache / Page Cache:** A unified Linux kernel cache storing disk pages in unused physical RAM to eliminate slow physical storage round-trips.
* **Bus Error (`SIGBUS`):** A hardware signal raised when a process attempts to access memory that the CPU cannot physically address (e.g. unaligned access or truncated mmap).

### C
* **Capability:** A discrete privilege unit in Linux (e.g. `CAP_NET_BIND_SERVICE`, `CAP_SYS_ADMIN`) decomposing the monolithic power of `root`.
* **Cgroup (Control Group):** A Linux kernel feature organizing processes into hierarchical groups to meter, monitor, and restrict resources (CPU, RAM, block I/O, PIDs).
* **Context Switch:** The hardware/kernel operation of saving the processor register state of an active thread or process and restoring the saved register state of another.
* **Copy-on-Write (COW):** An optimization where memory pages shared between parent and child after `fork()` are marked read-only; physical copying occurs only when a write is attempted.

### D
* **Deadlock:** A state where a set of concurrent execution paths are blocked indefinitely, each waiting for a lock or resource held by another in the set.
* **Demand Paging:** An operating system memory architecture where pages are loaded from disk or swap into physical RAM only upon an initial access fault.
* **Device Driver:** A kernel module or subsystem providing a standard interface for the kernel to issue commands to physical hardware peripherals.

### E
* **Epoll:** A Linux-specific scalable I/O event notification facility with $O(1)$ readiness polling, replacing $O(N)$ linear scans in `select()` and `poll()`.
* **Exception:** An internal synchronous processor event (such as divide-by-zero or page fault) triggered directly by instruction execution.
* **Exec (`execve`):** A system call that replaces the current process image, text, and data segments with a newly executed program binary while preserving the PID.

### F
* **False Sharing:** A multicore performance degradation where independent threads mutate distinct variables residing on the same physical CPU cache line (typically 64 bytes).
* **File Descriptor (FD):** A non-negative integer used by user space to identify an open file, socket, pipe, or device within a process-local table.
* **Fork:** A system call creating a new child process that is an exact duplicate of the parent process, returning 0 to the child and the child's PID to the parent.
* **Fsync:** A system call forcing all buffered dirty pages and metadata for an open file descriptor down to physical persistent storage.

### I
* **Inode (Index Node):** A filesystem data structure storing all metadata for a file (size, permissions, timestamps, owner, block pointers) except its human-readable name.
* **Interrupt (IRQ):** An asynchronous electrical signal from physical hardware (keyboard, NIC, timer) demanding immediate attention from the CPU.
* **IPC (Inter-Process Communication):** Mechanisms (pipes, FIFOs, UNIX sockets, shared memory, message queues) enabling separate processes to exchange data.

### L
* **Livelock:** A concurrency failure where two or more threads continuously change their state in response to each other without making any functional progress.
* **Load Average:** The exponentially smoothed average number of runnable tasks (`TASK_RUNNING`) plus tasks waiting in uninterruptible disk sleep (`TASK_UNINTERRUPTIBLE`) over 1, 5, and 15 minutes.

### M
* **Memory Management Unit (MMU):** A hardware component inside the CPU responsible for translating virtual memory addresses into physical memory addresses via page tables.
* **Mmap:** A system call that maps files or devices directly into process virtual memory, or creates anonymous memory regions for large heap allocations.
* **Mutex (Mutual Exclusion):** A synchronization lock allowing at most one thread to enter a critical section at any given time.

### N
* **Namespace:** A Linux kernel feature partitioning global system resources (PIDs, network interfaces, mount points, hostnames) so processes see isolated views.
* **Nice Value:** A user-visible integer (-20 to 19) influencing the priority assigned by the CPU scheduler to a runnable process.

### O
* **OOM Killer (Out-of-Memory Killer):** A Linux kernel subcomponent that selects and terminates high-memory processes using a heuristic score when RAM is exhausted.
* **Orphan Process:** A child process whose parent exited before reaping it; automatically re-parented to `init` (PID 1) or a local subreaper.

### P
* **Page Fault:** An interrupt raised by the MMU when a program accesses a virtual page that is not currently mapped to physical RAM.
* **Page Table:** A per-process data structure maintained by the operating system and read by the MMU to translate virtual page numbers to physical frame numbers.
* **PID (Process Identifier):** A unique numerical identifier assigned by the kernel to an active process.
* **Pipe:** A unidirectional byte stream IPC channel backed by a circular kernel buffer connecting standard output of one process to standard input of another.
* **Pthread:** A POSIX-compliant standardized threading interface for C/C++ supporting thread creation, joins, mutexes, and condition variables.

### R
* **Race Condition:** A software flaw where the final state depends on the non-deterministic scheduling timing and execution interleaving of concurrent threads.
* **Resident Set Size (RSS):** The portion of a process's virtual memory that currently occupies physical RAM.

### S
* **Segmentation Fault (`SIGSEGV`):** A signal sent to a process when it attempts to access memory outside its mapped address space or violates permissions (e.g. writing to read-only code).
* **Semaphore:** A synchronization variable maintaining an integer counter used to govern concurrent access to a finite pool of resources.
* **Signal:** An asynchronous notification sent by the kernel or a process to another process to inform it of an event (`SIGINT`, `SIGTERM`, `SIGKILL`, `SIGPIPE`).
* **Socket:** A software endpoint abstraction for network and inter-process communication.
* **Spinlock:** A low-level lock where a thread loops repeatedly ("spins") checking a condition rather than yielding the CPU.
* **Strace:** A Linux diagnostic utility intercepting and recording system calls made and signals received by a process.
* **System Call (Syscall):** The programmatic interface through which a userspace program requests privileged services from the operating system kernel.

### T
* **Thrashing:** A pathological system state where excessive paging/swapping absorbs all I/O bandwidth, causing CPU utilization and progress to collapse.
* **Translation Lookaside Buffer (TLB):** A small, high-speed hardware cache inside the CPU storing recent virtual-to-physical address translations.
* **Traps:** Synchronous software-initiated interrupts transferring control into the kernel (often used interchangeably with syscalls or software exceptions).

### V
* **Virtual Address:** An address generated by an executing program instruction that must be translated by the MMU before indexing physical memory.
* **Virtual File System (VFS):** A kernel abstraction layer providing a uniform POSIX filesystem API (`open`, `read`, `write`) across different filesystem formats (ext4, XFS, NFS, procfs).

### Z
* **Zombie Process:** A terminated process whose exit status has not yet been consumed by its parent via `wait()` or `waitpid()`. It occupies an entry in the kernel process table.
