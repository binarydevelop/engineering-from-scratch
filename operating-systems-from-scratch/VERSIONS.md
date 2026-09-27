# Supported Versions & Platform Compatibility Matrix

This curriculum is developed and verified across modern POSIX systems, specifically targeting long-term-supported Linux kernels and standard GNU/LLVM toolchains.

---

## 1. Verified Operating Systems & Kernels

| Operating System | Kernel Version | Support Tier | Notes |
| :--- | :--- | :---: | :--- |
| **Ubuntu 24.04 LTS (Noble Numbat)** | Linux 6.8.0+ | **Tier 1 (Primary)** | Native support for all 132 phases, cgroups v2, epoll, namespaces. |
| **Ubuntu 22.04 LTS (Jammy Jellyfish)** | Linux 5.15.0+ | **Tier 1** | Native support; verify cgroups v2 delegation if testing rootless. |
| **Debian 12 (Bookworm)** | Linux 6.1.0+ | **Tier 1** | Full compatibility with all C labs and Python simulations. |
| **Fedora 39 / 40** | Linux 6.5+ / 6.8+ | **Tier 1** | Full compatibility; SELinux may require `chcon` for loop mounts. |
| **Windows 11 WSL2 (Ubuntu 22.04/24.04)**| Microsoft Linux 5.15+ / 6.6+ | **Tier 1** | Full syscall tracing, `/proc`, cgroups v2 supported. |
| **macOS 14 (Sonoma) / 15 (Sequoia)** | Darwin 23.x / 24.x / 25.x | **Tier 2 (Hybrid)** | Native POSIX (threads, sockets, fork/exec, IPC). Linux-specific phases (epoll, namespaces, `/proc/maps`, cgroups) run inside Docker / Lima sandbox. |

---

## 2. Compilers & Toolchains

| Tool | Minimum Version | Recommended Version | Tested Flags |
| :--- | :--- | :--- | :--- |
| **GCC** | 11.4 | 13.2 / 14.1 | `-Wall -Wextra -pedantic -std=c11 -pthread -O2` |
| **Clang** | 14.0 | 17.0 / 18.0 / Apple Clang 16+ | `-Wall -Wextra -pedantic -std=c11 -pthread -O2` |
| **GNU Make** | 3.81 | 4.3+ | Standard POSIX targets |
| **Python** | 3.9 | 3.11 / 3.12 / 3.14 | Standard library only (no mandatory third-party dependencies) |
| **GDB** | 12.1 | 14.1 | Full DWARF-5 debugging symbols (`-g`) |
| **Strace** | 5.16 | 6.5+ | Full syscall argument decoding (`-s 256 -T -tt`) |
| **Valgrind** | 3.18 | 3.22+ | Memcheck leak and illegal memory access validation |

---

## 3. CPU Architectures

* **x86_64 (AMD64):** Fully tested and supported. Syscall registers: `rax` (call num), `rdi`, `rsi`, `rdx`, `r10`, `r8`, `r9`.
* **aarch64 (ARM64 / Apple Silicon / AWS Graviton):** Fully tested and supported. Syscall registers: `x8` (call num), `x0`-`x5`. Memory page size default is 4KB on Linux aarch64 and 16KB on macOS Darwin.

---

## 4. Software Dependencies

To maintain zero friction and long-term reproducibility, this course relies exclusively on:
1. **The C Standard Library (`libc` / `glibc` / `musl`)** and POSIX system call APIs.
2. **The Python Standard Library** (`sys`, `os`, `time`, `socket`, `threading`, `collections`, `dataclasses`, `queue`).
3. Standard Linux core diagnostic packages (`strace`, `lsof`, `procps`, `iproute2`, `sysstat`).

No external package managers, npm, or heavy third-party C libraries are required.
