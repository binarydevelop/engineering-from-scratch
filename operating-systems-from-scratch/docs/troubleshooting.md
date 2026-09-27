# Systems Programming Troubleshooting Guide

> **Core Philosophy:** In systems programming, errors are not vague bugs; they are explicit integer return codes and signals emitted by the kernel. Read the error code, inspect the kernel table, and trace the syscall.

---

## 1. Common Compilation & Linker Errors

### Issue: `undefined reference to 'pthread_create'`
* **Cause:** The POSIX threads runtime library was not linked during compilation.
* **Resolution:** Ensure `-pthread` is passed to both the compiler and linker:
  ```bash
  gcc -Wall -Wextra -pthread program.c -o program
  ```

### Issue: `fatal error: sys/epoll.h: No such file or directory`
* **Cause:** You are compiling on macOS (Darwin), which provides BSD `kqueue`, not Linux `epoll`.
* **Resolution:** Run the Linux-specific networking lessons inside the provided Docker sandbox or Lima VM:
  ```bash
  docker run --rm -it -v "$(pwd)":/lab -w /lab ubuntu:24.04 bash
  ```

### Issue: `error: implicit declaration of function 'execvp'`
* **Cause:** Missing POSIX feature test macro or header (`<unistd.h>`).
* **Resolution:** Ensure `<unistd.h>` and `<sys/wait.h>` are included at the top of your C file.

---

## 2. Common Runtime & Syscall Errors

### Issue: `bind failed: Address already in use` (`EADDRINUSE`, errno 98 / 48)
* **Cause:** A previous instance of the server crashed or was terminated, but its listening port is still tied to an active process or held in the kernel's `TIME_WAIT` state.
* **Diagnosis & Resolution:**
  1. Find the offending PID:
     ```bash
     lsof -i :8080
     # or
     ss -tulpn | grep 8080
     ```
  2. Kill the stale process:
     ```bash
     kill -9 <PID>
     ```
  3. Ensure your server code sets the `SO_REUSEADDR` socket option before binding:
     ```c
     int opt = 1;
     setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
     ```

### Issue: `fork: Resource temporarily unavailable` (`EAGAIN`, errno 11)
* **Cause:** The process limit (`ulimit -u`) has been reached, or the system process table is exhausted.
* **Resolution:**
  ```bash
  # Check current max user processes
  ulimit -u
  # Check how many processes you are running
  ps -u $USER | wc -l
  # Terminate rogue child processes
  pkill -f my_experiment_binary
  ```

### Issue: `write failed: Broken pipe` (`EPIPE` / `SIGPIPE`, errno 32)
* **Cause:** The process attempted to write to a pipe or socket whose reading end has been closed by the peer.
* **Resolution:** Ignore `SIGPIPE` or pass `MSG_NOSIGNAL` in `send()`:
  ```c
  signal(SIGPIPE, SIG_IGN);
  ```

### Issue: `Segmentation fault (core dumped)` (`SIGSEGV`, signal 11)
* **Cause:** The process attempted to dereference a NULL pointer, an unmapped address, or write to a read-only code page.
* **Diagnosis:**
  ```bash
  # Compile with debug symbols
  gcc -g -Wall program.c -o program
  # Launch under gdb
  gdb ./program
  (gdb) run
  (gdb) bt
  ```

---

## 3. macOS Darwin Differences

| Linux Diagnostic | macOS Equivalent | Notes |
| :--- | :--- | :--- |
| `strace ./binary` | `dtruss ./binary` (requires disabling SIP) | **Recommendation:** Use Docker / Lima for Linux syscalls |
| `ss -tulpn` | `netstat -anv` or `lsof -iTCP -sTCP:LISTEN` | Lists listening TCP sockets on macOS |
| `free -h` | `vm_stat` or `top -l 1 -s 0 \| grep PhysMem` | Reports page sizes (4KB vs 16KB on Apple Silicon) |
| `/proc/<pid>/maps` | `vmmap <pid>` | Reports virtual memory regions under Mach |
| `cat /proc/cpuinfo`| `sysctl -a \| grep machdep.cpu` | Reports CPU features and core layout |
