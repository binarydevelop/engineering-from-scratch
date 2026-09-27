# Lesson 02.1: Your First Container (`hello-world` Dissected)

## Motto
"An image is inert storage; a container is an ephemeral instance; a running container exists only as long as its root process is alive."

## Problem
Every beginner runs `docker run hello-world`, sees a few lines of celebratory text, and immediately runs `docker ps`. The list is empty!
Where did the container go? Did it delete itself? Did it crash? Is Docker broken?
Without understanding the link between an image, a container, and the lifecycle of its root process, developers mistakenly think containers are like virtual machines that stay on forever until powered down.

## Prediction
Before running `docker run hello-world`:
1. Will an operating system boot?
2. If `docker ps` returns an empty table, does the container still exist on your disk?
3. What process was executed inside `hello-world`?

## Why this matters
If you don't know why `docker ps` is empty after running a container, you will not understand why web servers stay running (they keep PID 1 listening indefinitely) while migration scripts or CLI utilities exit immediately. You will also accumulate hundreds of dead, exited containers eating disk space on your machine.

## First principles
1. **The Invariant Relationship**:
   ```text
   Image (Read-Only Template)
      ↓ docker create / run
   Container (Isolated Writable Instance)
      ↓ executes
   Root Process (PID 1 inside namespace)
   ```
2. **Process-Bound Lifecycle**: A container has no independent pulse or kernel heartbeat. The container is alive if and only if its primary process (PID 1) is in a running state.
3. **Exit Code Propagation**: When PID 1 inside the container exits (for example, after printing text to stdout and calling `exit(0)`), the Linux kernel cleans up the container's process tree and the Docker daemon records the container's state as `exited` with that exact exit code.
4. **State Persistence**: The container does not vanish when it exits! Its logs, exit code, metadata, and writable filesystem modifications remain preserved on disk until explicitly removed via `docker rm`.

## Mental model

```text
               ┌───────────────────────────────┐
               │    Image: "hello-world"       │
               │ (Contains static binary /hello│
               └──────────────┬────────────────┘
                              │
                              ▼ docker run
               ┌───────────────────────────────┐
               │     Container: "dfs-hello"    │
               │                               │
               │   Process: /hello (PID 1)     │
               │   1. Prints text to stdout    │
               │   2. Calls exit(0)            │
               └──────────────┬────────────────┘
                              │ Process terminates
                              ▼
               ┌───────────────────────────────┐
               │  Container State: "exited"    │
               │  - ExitCode: 0                │
               │  - Running: false             │
               │  - Still stored on disk!      │
               │  - Visible in "docker ps -a"  │
               └───────────────────────────────┘
```

## Build it
We use Docker's inspection engine to inspect the state machine of the container without relying on high-level summaries.
Look at [inspect_container_lifecycle.py](../code/inspect_container_lifecycle.py). It parses the low-level JSON returned by `docker inspect` to display:
- `State.Status` (`exited`)
- `State.Running` (`false`)
- `State.ExitCode` (`0`)
- `Config.Path` (`/hello`)

## Run it
Execute the experiment script:

```bash
./phases/02-your-first-container/01-hello-world-dissected/experiments/run_experiment.sh
```

## Inspect it
1. Run `docker ps`: The table is empty because `docker ps` filters by `status=running` by default.
2. Run `docker ps -a`: The `-a` flag (all) reveals `dfs-hello` with status `Exited (0)`.
3. Run `python3 inspect_container_lifecycle.py dfs-hello` to verify that `Path: /hello` executed and terminated at `FinishedAt`.

## Break it
Run a container with a command that immediately fails:

```bash
docker run --name dfs-fail alpine sh -c "echo 'failing now' >&2; exit 42"
```

Inspect the container:
```bash
docker inspect dfs-fail --format 'Status: {{.State.Status}}, ExitCode: {{.State.ExitCode}}'
```
Notice that Docker faithfully records `ExitCode: 42`.
Clean up:
```bash
docker rm dfs-fail
```

## Debug it
When a container unexpectedly stops:
1. Run `docker ps -a` to locate the container ID and name.
2. Check `docker logs <container>` to see what the process printed to `stdout` or `stderr` before dying.
3. Check `docker inspect <container> --format '{{.State.ExitCode}}'` to identify why the process terminated.
4. Check `docker inspect <container> --format '{{.State.OOMKilled}}'` to see if the kernel killed it for exceeding RAM limits.

## Modify it
Run an interactive container that does *not* exit immediately:
```bash
docker run --name dfs-interactive -it alpine sh
```
Inside the container, run `ps`. Notice that `sh` is PID 1.
Open a second terminal window on your host and run `docker ps`. Notice that `dfs-interactive` is actively listed as `Up`!
Exit the shell (`exit`). Run `docker ps` again; it is now gone from the active list.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Output of `docker ps` vs `docker ps -a`.
- The `ExitCode`, `Path`, and timestamps from `inspect_container_lifecycle.py`.
- What happened when you injected exit code `42`.

## Questions for mastery
1. What is the fundamental difference between an image and a container?
2. If you run `docker run hello-world` 5 times, how many images exist on your machine? How many containers exist?
3. Why does an Nginx or PostgreSQL container stay running, while `hello-world` exits after 1 second?

## What comes next
We saw that `hello-world` ran an executable from an image. But what *is* an image? Where are its files stored? How are layers structured? Proceed to **Phase 03: Images From First Principles**.
