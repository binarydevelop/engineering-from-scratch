# Platform Setup Guide: Operating Systems Laboratory

> **Core Rule:** Never treat macOS, BSD, and Linux kernel internals as identical. Learn their common POSIX foundations, but respect their unique kernel architectures.

This guide prepares your operating-systems laboratory across different host platforms. It guarantees a safe, reproducible, and isolated environment for running experiments, tracing syscalls, measuring context switches, and building containers from scratch.

---

## 1. Supported Platform Matrix

| Environment | POSIX Systems Programming (C / pthreads / Sockets) | Linux Syscall Tracing (`strace`) | Linux Procfs & Sysfs (`/proc`, `/sys`) | Namespaces & Cgroups (Containers) | Performance Profiling (`perf`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Native Linux (Ubuntu 22.04 / 24.04, Debian, Fedora)** | Full (Native) | Native (`strace`) | Native | Native (Root / Sudo) | Native Hardware Counters |
| **WSL2 (Windows 11 with Ubuntu kernel)** | Full (Native) | Native (`strace`) | Native | Native (v2 cgroups) | Emulated / Limited |
| **macOS (Apple Silicon & Intel)** | Full (Darwin POSIX) | Emulated (`dtruss` / macOS Instruments) | macOS equivalents (`sysctl`) | **Requires Linux VM / Container** | Instruments / `sample` |
| **Linux Container (Docker Desktop / OrbStack)** | Full | Full (if unconfined) | Isolated mount | Nested / Rootless | Host dependent |
| **Disposable Linux VM (Lima / Multipass / UTM)** | Full | Full | Full | Full (Dedicated kernel) | High accuracy |

---

## 2. Platform 1: Native Linux Setup

If you are running native Ubuntu, Debian, Arch, or Fedora, your machine is ready for every single phase of this course.

### Ubuntu / Debian Package Installation
```bash
sudo apt-get update && sudo apt-get install -y \
    build-essential \
    clang \
    gcc \
    gdb \
    make \
    strace \
    lsof \
    iproute2 \
    procps \
    sysstat \
    valgrind \
    linux-tools-generic \
    python3 \
    python3-pip \
    libcap-dev
```

### Fedora Package Installation
```bash
sudo dnf groupinstall -y "Development Tools" "C Development Tools and Libraries"
sudo dnf install -y \
    clang \
    gdb \
    strace \
    lsof \
    iproute \
    procps-ng \
    sysstat \
    valgrind \
    perf \
    python3 \
    libcap-devel
```

---

## 3. Platform 2: macOS Setup (Darwin Kernel)

macOS uses the **XNU kernel** (a hybrid of Mach microkernel, BSD POSIX subsystem, and I/O Kit), whereas Linux uses the monolithic Linux kernel.

### What Works Natively on macOS:
* All standard C systems programming (Phases 03–12, 21–28, 44, 46–50, 52, 66–69, 73–80).
* `fork()`, `exec()`, `wait()`, `pipe()`, `dup2()`, standard file descriptors.
* POSIX threads (`pthreads`), mutexes, condition variables, semaphores.
* BSD sockets, TCP echo servers, UNIX domain sockets, `select()`, `poll()`.
* Python algorithmic simulators (Scheduling, Page Replacement, Virtual Memory, TLB).

### What Requires a Linux Sandbox on macOS:
* Linux-specific syscall tracing with `strace` (macOS uses DTrace/SIP-protected tracing).
* Linux procfs details (`/proc/<pid>/maps`, `/proc/<pid>/status`, `/proc/meminfo`). macOS uses Mach task APIs and `vm_map`.
* Linux epoll (`epoll_create`, `epoll_ctl`, `epoll_wait`). macOS uses BSD `kqueue`.
* Linux Namespaces (`clone` with `CLONE_NEWPID`, `CLONE_NEWNS`, `CLONE_NEWNET`).
* Linux Control Groups (`cgroups v1/v2`).
* Inode-level raw block experiments and ext4 journaling mechanics.

### Recommended macOS Options:

#### Option A: Lightweight Disposable Linux VM with Lima (Recommended)
[Lima](https://github.com/lima-vm/lima) provides an isolated, fast Ubuntu Linux VM with automatic directory sharing:
```bash
# Install Lima via Homebrew
brew install lima

# Launch an Ubuntu VM named 'os-lab'
limactl start --name=os-lab template://ubuntu

# Open a shell inside the Linux environment
limactl shell os-lab

# Inside the shell:
sudo apt-get update && sudo apt-get install -y build-essential gcc clang gdb strace lsof procps
```

#### Option B: Docker Linux Sandbox
If Docker Desktop or OrbStack is installed:
```bash
# Run an interactive Ubuntu sandbox mounting the repository directory
docker run --rm -it \
    --cap-add=SYS_PTRACE \
    --cap-add=SYS_ADMIN \
    --security-opt seccomp=unconfined \
    -v "$(pwd)":/lab \
    -w /lab \
    ubuntu:24.04 bash

# Inside the container:
apt-get update && apt-get install -y build-essential clang gcc gdb strace lsof procps python3
```

#### Option C: Native macOS Compilation
For native compilation on macOS, Apple Clang and Make are sufficient:
```bash
xcode-select --install
brew install python3
```

---

## 4. Platform 3: Windows Subsystem for Linux (WSL2)

WSL2 runs a genuine, Microsoft-maintained Linux kernel inside a lightweight Hyper-V utility VM. It supports native ELF binaries, syscalls, and `/proc`.

### Installation
Open PowerShell as Administrator:
```powershell
wsl --install -d Ubuntu-24.04
```

After rebooting and logging in:
```bash
sudo apt update && sudo apt install -y \
    build-essential gcc clang gdb strace lsof procps valgrind python3
```

> **WSL2 Note on Cgroups:** WSL2 uses cgroups v2 by default in modern Windows builds. Verify with `mount -t cgroup2`.

---

## 5. Privilege Safety & Protection Principles

Some operating-system experiments inspect or manipulate kernel tables (e.g. mounting filesystems, creating network interfaces, altering process priorities, adjusting cgroups).

### The Golden Safety Rules:
1. **Never run destructive commands on your primary workstation without isolation.**
2. **Commands requiring elevated privileges are clearly prefixed:**
   * `sudo`: Administrative elevation.
   * `CAP_SYS_ADMIN`: Required for mount, pivot_root, namespaces.
   * `CAP_NET_ADMIN`: Required for creating virtual interfaces (veth pairs).
3. **No uncontrolled fork-bomb code is ever compiled without strict process limits.**
4. **Always verify active PID and directory before running signals or file cleanups:**
   ```bash
   pwd && id && ps -ef
   ```
5. **Always provide clean termination handlers (`SIGINT` via Ctrl+C) in infinite loops.**

---

## 6. Verifying Your Setup

Run the included environment checking script from the root of the repository:
```bash
./scripts/check-environment.sh
```

It checks compiler versions, Python version, available diagnostic utilities (`strace`, `lsof`, `ss`), and detects whether you are running under native Linux, WSL2, or macOS Darwin.
