# Lesson 01.1: Host Process Lifecycle Before Containers

## Motto
"If you do not understand processes on the host, containers will always look like magic."

## Problem
Developers often describe a container as a "lightweight virtual machine" or "a running image". But what is actually executing on the CPU?
When a container is started, no operating system boots. There is no BIOS, no kernel initialization, and no hypervisor context switch. If you cannot explain what a process ID (PID) is, how environment variables are inherited, why `stdout` differs from `stderr`, or what happens when the kernel sends `SIGKILL`, you will never be able to diagnose a crashed container or an application exiting with code 137.

## Prediction
1. If an application process handles `SIGTERM`, can it intercept `SIGKILL` (signal 9) too?
2. If a process exits due to `SIGKILL`, what exit code does Unix return?
3. Where do environment variables come from when a process starts?

## Why this matters
Every single container lifecycle event in Docker maps directly to host process mechanics:
- `docker stop` sends `SIGTERM`, waits 10 seconds, and if the process hasn't exited, sends `SIGKILL`.
- Container exit code `137` is simply `128 + 9` (`SIGKILL`), indicating an ungraceful forced termination or kernel Out-Of-Memory (OOM) kill.
- When you pass `-e KEY=VAL` to `docker run`, Docker simply populates the initial environment block of the container's PID 1 process.

## First principles
1. **Program vs. Process**: A program is inert bytes sitting on disk (like a Python file or compiled binary). A process is an active instance loaded into memory, assigned a Process ID (PID), memory pages, file descriptors (FDs 0, 1, 2 for stdin, stdout, stderr), and an execution thread scheduled by the OS kernel.
2. **Process Hierarchy**: Every process is spawned by a parent process via `fork()` (or `clone()`) and `execve()`. It receives a Parent Process ID (PPID).
3. **Signals**: Asynchronous notifications sent by the kernel:
   - `SIGTERM` (15): Polite request to terminate. Processes can catch this signal, flush buffers, close database connections, and exit cleanly with code 0.
   - `SIGKILL` (9): Immediate, uncatchable termination. The kernel reclaims process memory instantly without notifying the process.
4. **Exit Codes**: A byte returned to the OS kernel upon termination. By convention, `0` indicates success; any non-zero value indicates an error. If killed by an unhandled signal `N`, the exit code is `128 + N`.

## Mental model

```text
OPERATING SYSTEM PROCESS LIFECYCLE:
┌────────────────────────────────────────────────────────┐
│  Disk: server.py (Inert bytes)                         │
└──────────────────────────┬─────────────────────────────┘
                           │ fork() + execve()
                           ▼
┌────────────────────────────────────────────────────────┐
│  RUNNING PROCESS (PID: 93838, PPID: 93831)             │
│  ├── File Descriptors:                                 │
│  │   ├── 0: stdin                                      │
│  │   ├── 1: stdout --> /tmp/dfs_server.stdout          │
│  │   ├── 2: stderr --> /tmp/dfs_server.stderr          │
│  │   └── 3: TCP Socket listening on 127.0.0.1:8001     │
│  ├── Environment: { APP_ENV: "production", PATH: ... } │
│  └── Signal Handlers:                                  │
│      ├── SIGTERM: [custom graceful_shutdown()]         │
│      └── SIGKILL: [Uncatchable kernel termination]     │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             │ kill -TERM                │ kill -9 (SIGKILL)
             ▼                           ▼
┌──────────────────────────┐ ┌──────────────────────────┐
│ Flushes state & exits    │ │ Killed by kernel instantly│
│ Exit code: 0             │ │ Exit code: 137 (128 + 9)  │
└──────────────────────────┘ └──────────────────────────┘
```

## Build it
Look at [server.py](../code/server.py).
It creates an HTTP server that:
- Reads its own PID (`os.getpid()`) and PPID (`os.getppid()`).
- Reads `APP_ENV` from the environment table (`os.environ`).
- Registers a signal handler on `signal.SIGTERM` that sleeps for 1 second to flush buffers before calling `sys.exit(0)`.
- Writes informational logs to `sys.stdout` and lifecycle events to `sys.stderr`.

## Run it
Execute the experiment script:

```bash
./phases/01-processes-before-containers/01-host-process-lifecycle/experiments/run_experiment.sh
```

## Inspect it
Observe:
1. `curl http://127.0.0.1:8001` returns the process PID and environment.
2. `lsof -Pan -p <PID> -i` proves file descriptor 3 is bound to TCP port 8001.
3. In `ps -p <PID> -o pid,ppid,stat,command`, the PPID matches the shell that launched it.

## Break it
Launch `server.py` and issue a raw `kill -9 <PID>`:
```bash
python3 phases/01-processes-before-containers/01-host-process-lifecycle/code/server.py &
KILL_PID=$!
kill -9 $KILL_PID
wait $KILL_PID
echo "Exit code: $?"
```
Observe that the server had no opportunity to print its shutdown notice to stderr, and the shell reports an exit code of `137`.

## Debug it
When investigating an unexpected process termination:
1. Check exit code:
   - `0`: Normal exit.
   - `1`: Exception / error.
   - `137`: Killed by `SIGKILL` (signal 9) or OOM.
   - `143`: Killed by `SIGTERM` (signal 15).
2. Check standard error streams (`stderr`) for traceback logs.
3. Check open ports using `lsof -i :<PORT>` to ensure port conflicts didn't abort startup (`EADDRINUSE`).

## Modify it
Edit [server.py](../code/server.py) to exit with code `42` if an environment variable `FAIL_ON_BOOT=1` is passed. Run it and verify with `echo $?`.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The observed PID, PPID, and port binding.
- Stderr output when `SIGTERM` was received.
- The exact exit code observed after `kill -9`.

## Questions for mastery
1. Why does `kill -9` not allow a process to close open files or database connections?
2. If Docker runs programs, what is Docker actually managing? (Hint: it's not virtual machines; it's processes!)
3. Why do containers fail if the application forks into the background (daemonizes)?

## What comes next
Now that we have deeply observed processes, signals, and ports on the host, we are ready to run our first container and see how Docker manages this process lifecycle. Proceed to **Phase 02: Your First Container**.
