# Lesson 28.2: Debugging Lab 02 — Immediate Exit (`ExitCode: 127`)

## Motto
"Exit code 127 means the kernel cannot find the binary you told it to execute; verify binary existence and paths inside the container."

## Problem
**Symptom:**
A developer runs `docker run -d my-app`.
Running `docker ps` shows no running containers.
Running `docker ps -a` shows the container in state `Exited (127) 2 seconds ago`.
The developer runs `docker logs` and sees:
`exec: "/usr/bin/python": stat /usr/bin/python: no such file or directory`
Why did the container exit immediately?

## Prediction
1. What does exit code 127 mean in Unix and POSIX systems?
2. If Python is installed in `/usr/local/bin/python3`, will calling `/usr/bin/python` succeed?
3. What is the difference between exit code 126 and 127?

## Why this matters
Binary path mismatches, missing dynamic linkers (`/lib64/ld-linux-x86-64.so.2` on Alpine), and Windows `CRLF` line endings in shebang lines (`#!/bin/sh\r`) all cause immediate exit code 127.

## First principles
When Docker starts a container, `runc` invokes `execve(path, argv, envp)`.
If `execve()` returns `ENOENT` (No such file or directory), the container cannot spawn PID 1, and the runtime returns exit code `127`.

## Mental model
```
[Docker Engine: runc execve("/usr/bin/python")]
                      │
                      ▼
            Kernel searches rootfs
                      │
           ├── Found? ──► Spawns PID 1 (Container RUNNING)
           └── Missing? ─► ENOENT (Container terminates with ExitCode 127)
```

## Build it
Review `Dockerfile.broken` in `code/`. It specifies `CMD ["/usr/bin/python", "--version"]`.

## Run it
Execute the lab runner:

```bash
./phases/28-container-debugging-without-magic/lab-02-immediate-exit/experiments/run_experiment.sh
```

## Inspect it
1. `docker ps` returns empty.
2. `docker ps -a` shows `Exited (127)`.
3. `docker inspect` confirms `ExitCode: 127`.

## Break it
Add a script with Windows CRLF line endings (`\r\n`) as the entrypoint:
The Linux kernel attempts to execute `/bin/sh\r`, fails to find that interpreter, and throws code 127!

## Debug it
1. Hypothesis: The binary path specified in `ENTRYPOINT` or `CMD` does not exist inside the image.
2. Test binary presence inside the image:
   ```bash
   docker run --rm <image> which <binary>
   ```
3. Fix: Specify the correct absolute path or ensure the package is installed.

## Modify it
Change `Dockerfile.fixed` to call `/bin/date`. Rebuild and run.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- The `Exited (127)` status observed.
- Diagnostic reasoning used to locate the missing binary.

## Questions for mastery
1. Why does an Alpine Linux container fail with exit code 127 when running a dynamically-linked Go binary compiled on Ubuntu?
2. How does `dos2unix` fix script-related exit code 127 errors?

## What comes next
In the next lab, a container starts successfully but immediately crashes on an unhandled environment variable. Proceed to **Lab 03: Missing Environment Variable**.
