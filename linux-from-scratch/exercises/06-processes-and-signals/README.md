# Exercise Set 06: Processes, Signals & Job Control

### Ex 6.1: Program vs Process Distinction
Explain the difference between an executable binary on disk and an active process in the kernel. What kernel data structure tracks an active process?

### Ex 6.2: Inspecting Process Lineage
Run `sleep 100 &` in your terminal. Use `ps` to find its PID, PPID (parent PID), and state. Verify that the PPID equals your interactive shell's PID (`$$`).

### Ex 6.3: Foreground to Background Job Control
Start a long-running process in the foreground (`sleep 300`). Suspend it using `Ctrl-Z`. Inspect shell jobs with `jobs`. Resume it in the background with `bg`. Finally bring it back to foreground with `fg` and terminate it with `Ctrl-C`.

### Ex 6.4: Signals: SIGTERM vs SIGKILL
Launch two background `sleep` processes. Terminate the first using `SIGTERM` (signal 15) and the second using `SIGKILL` (signal 9). Which signal can be intercepted or ignored by a process?

### Ex 6.5: SIGHUP and Hangup Immunity
Why do processes launched in an interactive terminal die when you close the SSH session? Demonstrate how `nohup` or `disown` detaches a process from the controlling terminal's SIGHUP signal.

### Ex 6.6: Exploring /proc/<pid>/ Internals
Start a Python HTTP server in the background. Inspect its `/proc/<pid>/cmdline`, `/proc/<pid>/cwd`, `/proc/<pid>/environ`, and `/proc/<pid>/fd/`.

### Ex 6.7: Process States (R, S, D, Z, T)
Explain what each single-letter process state code in `ps aux` means. Which state indicates uninterruptible disk sleep waiting on hardware I/O?

### Ex 6.8: Trapping Signals in Bash
Write a small Bash script that intercepts `SIGINT` (Ctrl-C) and `SIGTERM`, prints a graceful shutdown message, cleans up a temporary file, and exits cleanly.

### Ex 6.9: Auditing Open File Descriptors with lsof
Use `lsof -p <pid>` to list every open regular file, network socket, and shared library mapped by a running process.

### Ex 6.10: Process Priorities with Nice and Renice
Launch a CPU-intensive loop with a lower priority (`nice -n 19`). While running, use `renice` to adjust its scheduling niceness back to `0`.

### Ex 6.11: Inspecting Thread Trees
Run a multi-threaded process (e.g. Python multithreading or web browser). Use `ps -T -p <pid>` to inspect individual thread IDs (SPIDs).

### Ex 6.12: Identifying Zombie Processes
Explain why a zombie process appears in state `Z`. Why cannot a zombie process be killed with `kill -9`? What action must be taken to remove a zombie from the process table?
