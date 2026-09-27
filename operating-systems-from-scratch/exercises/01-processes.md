# Track 1: Process Lifecycle & Process Creation Exercises

> **Motto:** Understand it. Build it. Run it. Inspect it. Measure it. Break it. Debug it. Rebuild it.

All solutions are located in `solutions/exercises/01-processes-solutions.md`.

---

### Exercise 1.1: The Identity of a Process
Write a C program that prints its own PID, its parent PID (PPID), its real user ID (UID), and its real group ID (GID) using `getpid()`, `getppid()`, `getuid()`, and `getgid()`. Verify the output matches `ps -o pid,ppid,uid,gid -p $$`.

### Exercise 1.2: Predicting Fork Output
Predict the exact console output before compiling and running this snippet:
```c
int x = 10;
if (fork() == 0) {
    x += 5;
    printf("Child: %d\n", x);
} else {
    wait(NULL);
    printf("Parent: %d\n", x);
}
```
Explain why `Parent: 10` is printed instead of `15`.

### Exercise 1.3: The Binary Fork Tree
Write a C program where a parent process calls `fork()` twice in a loop:
```c
for (int i = 0; i < 2; i++) fork();
```
Draw the resulting process tree. How many total processes are created? How many child processes does the root parent directly own?

### Exercise 1.4: Inspecting Process Memory Regions
Write a C program that declares an uninitialized global, an initialized global, a stack integer, and a `malloc`'d heap buffer. Print their memory addresses and compare them with the layout reported in `/proc/<pid>/maps` on Linux (or `vmmap` on macOS).

### Exercise 1.5: Program Image Replacement with `execvp`
Write a program that creates a child process. The child replaces its address space with `ls -la /usr` using `execvp()`. The parent prints `"Child finished"` only after the child exits.

### Exercise 1.6: The Anatomy of `waitpid` Exit Status
Write a program where a child process exits with code `77`. The parent process uses `waitpid()` with the `status` pointer, evaluates `WIFEXITED(status)` and `WEXITSTATUS(status)`, and prints the recovered exit code.

### Exercise 1.7: Detecting Abnormal Termination via Signal
Write a program where the child enters an infinite loop. The parent sleeps for 1 second, then sends `SIGKILL` to the child using `kill(child_pid, SIGKILL)`. The parent inspects `WIFSIGNALED(status)` and `WTERMSIG(status)` to confirm termination via signal 9.

### Exercise 1.8: Creating a Controlled Zombie Process
Write a program that deliberately spawns a child that exits immediately, while the parent sleeps for 10 seconds without calling `wait()`. Inspect the process using `ps aux | grep 'Z'`. Verify that the child occupies an entry in the kernel process table despite executing zero CPU instructions.

### Exercise 1.9: Safe Zombie Reaping via `SIGCHLD`
Modify Exercise 1.8 by installing a signal handler for `SIGCHLD`. In the signal handler, invoke `while (waitpid(-1, NULL, WNOHANG) > 0);`. Verify that the zombie is reaped immediately upon termination without pausing the parent.

### Exercise 1.10: Observing Orphan Reparenting
Write a program where a parent forks a child and exits immediately. The child sleeps for 2 seconds, prints its PPID before and after the parent exits, and demonstrates reparenting to `init` (PID 1) or a subreaper.

### Exercise 1.11: Environment Variable Inheritance
Write a program that sets an environment variable using `setenv("COURSE", "OS_FROM_SCRATCH", 1)`, forks a child, and invokes `getenv("COURSE")` inside the child. Verify that environment variables are copied across address spaces.

### Exercise 1.12: Passing Arguments via `execve`
Write a program that uses the raw `execve()` system call to execute `/usr/bin/env` with a custom `char *const envp[]` array containing `{"VAR1=Alpha", "VAR2=Beta", NULL}`.

### Exercise 1.13: Controlled Process Fan-out
Write a program that spawns exactly $N=5$ child processes concurrently, where each child sleeps for $N - i$ seconds before exiting with exit code $i$. The parent reaps them in completion order using `wait()`.

### Exercise 1.14: Measuring `fork()` Execution Latency
Using `clock_gettime(CLOCK_MONOTONIC)`, measure the time in microseconds required for the kernel to execute `fork()` and return control to the parent. Compare with thread creation latency.

### Exercise 1.15: Intercepting `SIGINT` (Ctrl+C)
Write a daemon program that catches `SIGINT`. When the user presses Ctrl+C, print `"SIGINT received; cleaning up..."` and exit with code 0 instead of terminating abruptly.

### Exercise 1.16: Non-maskable Signals
Write a program that attempts to register a signal handler for `SIGKILL` and `SIGSTOP`. Observe the return value of `signal()` or `sigaction()`, inspect `errno` (`EINVAL`), and explain why the kernel forbids catching these signals.

### Exercise 1.17: Process State Transitions in `/proc`
Write a program that cycles through three states:
1. `TASK_RUNNING` (busy computation)
2. `TASK_INTERRUPTIBLE` (`sleep()`)
3. `TASK_STOPPED` (`raise(SIGSTOP)`)
Inspect the `State:` field in `/proc/<pid>/status` during each phase.

### Exercise 1.18: Process Nice Values and Priorities
Write a CPU-bound worker program. Run two instances simultaneously: one with `nice -n -10` and one with `nice -n 19`. Observe their CPU shares using `top` or `pidstat`.

### Exercise 1.19: Process Groups & Sessions
Write a program that calls `setsid()` to create a new session and detach from the controlling terminal. Verify with `ps -o pid,pgid,sess,tty`.

### Exercise 1.20: The Subreaper Primitives (`PR_SET_CHILD_SUBREAPER`)
On Linux, write a process that marks itself as a subreaper using `prctl(PR_SET_CHILD_SUBREAPER, 1)`. Fork a child that forks a grandchild and exits. Prove that the grandchild is re-parented to the subreaper instead of PID 1!
