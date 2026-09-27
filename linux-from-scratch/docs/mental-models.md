# Core Linux Mental Models

> "Linux is a collection of coherent abstractions—files, processes, users, permissions, sockets, devices, mounts, services, logs, and kernel interfaces—that can be inspected and composed using small tools."

---

## 1. The Kernel vs. User Space Split

Linux strictly separates privileged supervisor hardware access from unprivileged application runtime:

```text
+-------------------------------------------------------------------------+
|                              USER SPACE                                 |
|                                                                         |
|  Interactive Shells     User Applications      System Services (systemd)|
|  (bash, zsh)            (python, nginx, curl)  (sshd, cron, journald)   |
|         │                        │                        │             |
|         ▼                        ▼                        ▼             |
|  Standard C Library (glibc / musl)                                      |
+─────────────────────────────────────────────────────────────────────────+
                              ▲ System Calls (syscalls)
                              │ open(), read(), fork(), execve(), socket()
+─────────────────────────────▼───────────────────────────────────────────+
|                             KERNEL SPACE                                |
|                                                                         |
|  +-------------------+  +-------------------+  +---------------------+  |
|  | Process Scheduler |  |  Virtual Memory   |  | Virtual Filesystem  |  |
|  | (CFS, task_struct)|  |  (Page Tables)    |  | (VFS, Inodes, Dentry|  |
|  +-------------------+  +-------------------+  +---------------------+  |
|  +-------------------+  +-------------------+  +---------------------+  |
|  | Networking Stack  |  | Security & DAC    |  | Device Drivers      |  |
|  | (TCP/IP, Netfilter|  | (UID, Capabilities|  | (Char, Block, Net)  |  |
|  +-------------------+  +-------------------+  +---------------------+  |
+─────────────────────────────────────────────────────────────────────────+
                              ▲ Hardware Interrupts & DMA
                              ▼
+─────────────────────────────────────────────────────────────────────────+
|                              HARDWARE                                   |
|               CPU  |  RAM  |  NVMe/SSD  |  NIC  |  Timers               |
+-------------------------------------------------------------------------+
```

Every user command, script, or server is merely a user-space process requesting the kernel to do work via **system calls**.

---

## 2. The Single-Rooted Filesystem & Virtual Filesystems

Unlike systems with drive letters (`C:\`, `D:\`), Linux provides one unified hierarchical namespace rooted at `/`.

```text
/
├── bin -> usr/bin        # Standard essential binaries
├── boot/                 # Kernel (vmlinuz), initramfs, bootloader (GRUB)
├── dev/  [devtmpfs]      # Device nodes (disks, ttys, /dev/null)
├── etc/                  # Host-specific system configuration files
├── home/                 # User personal home directories
├── lib -> usr/lib        # Shared dynamic libraries (.so)
├── proc/ [procfs]        # KERNEL VIRTUAL FS: Processes, memory, kernel state
├── root/                 # Superuser (root) home directory
├── sys/  [sysfs]         # KERNEL VIRTUAL FS: Hardware devices, buses, drivers
├── tmp/                  # Temporary files (often tmpfs in RAM)
├── usr/                  # Read-only user software, libraries, docs
└── var/                  # Variable runtime data (logs, spools, caches)
```

### The Three Virtual Filesystems
1. `/proc`: The kernel's live window into running processes and system resources. `/proc/cpuinfo`, `/proc/meminfo`, `/proc/<pid>/fd/` exist only in RAM!
2. `/sys`: The kernel's structured hierarchy of hardware buses, network interfaces, and cgroups (`/sys/class/net/`, `/sys/block/`).
3. `/dev`: Device files representing character streams (`/dev/urandom`, `/dev/tty`) and block storage devices (`/dev/sda`, `/dev/nvme0n1`).

---

## 3. The Stream & File Descriptor Model

In Unix, standard I/O is governed by integer handles called **File Descriptors (FDs)**:

```text
               THE PROCESS STREAM MODEL
                  ┌─────────────────┐
                  │ Running Process │
                  │     (PID)       │
                  └──┬──────┬─────┬─┘
  FD 0 (stdin)       │      │     │       FD 1 (stdout)
  ◄──────────────────┘      │     └─────────────────────►
  Input stream              │             Output stream
  (keyboard / pipe)         │             (terminal / file)
                            │
                            │             FD 2 (stderr)
                            └───────────────────────────►
                                          Diagnostic stream
                                          (terminal / error log)
```

- **Pipes (`|`)**: Connect `stdout` (FD 1) of process A directly to `stdin` (FD 0) of process B via kernel circular memory buffer.
- **Redirection (`>`, `2>`, `>>`)**: Instructs the kernel to point an FD at an open file description rather than the terminal.

---

## 4. The Storage Stack: From Silicon to Directory

```text
Hardware Disk (NVMe SSD)
        │
        ▼
Block Device Kernel Representation (`/dev/nvme0n1`)
        │
        ▼
Partition Table (GPT) -> Partition (`/dev/nvme0n1p2`)
        │
        ▼
Filesystem Structure (ext4 Superblock, Inode Table, Data Blocks)
        │
        ▼
VFS Mount Operation (`mount /dev/nvme0n1p2 /var`)
        │
        ▼
Directory Tree Node (`/var/log/syslog`)
```

- **`df`** inspects the filesystem **superblock** (total blocks allocated vs. free).
- **`du`** walks the **directory entries (dentries)** summing up individual file sizes.
- **Inodes** hold file metadata (permissions, owner, timestamps, block pointers). The filename lives in the parent directory entry!

---

## 5. The Networking Stack & Sockets

```text
Application Layer    : curl / nginx / python
          ▲
          │ Berkeley Sockets API (socket, bind, listen, accept)
          ▼
Transport Layer (L4) : TCP / UDP (Port numbers: 0 - 65535)
          ▲
          │
          ▼
Network Layer (L3)   : IP Routing Table (`ip route`), Netfilter / iptables
          ▲
          │
          ▼
Link Layer (L2)      : Network Interface (`eth0`, MAC Address, ARP Cache)
          ▲
          │
          ▼
Physical Layer (L1)  : Physical Ethernet cable, Wi-Fi radio, or virtual bridge
```

A **socket** is an endpoint for communication referenced by a file descriptor. A listening port is simply a socket bound to an IP and port waiting in the `LISTEN` state.
