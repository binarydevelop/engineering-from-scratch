# Lesson 13.1: Bind Mounts and Development Workflows

## Motto
"Bind mounts bridge your host filesystem and container namespace; use them for live code editing, not production database storage."

## Problem
When developing web applications, running `docker build` every time you change a single CSS rule or Python function is agonizingly slow.
Developers want instant feedback: edit code in VS Code or Vim on the host, save the file, and have the web framework or dev server automatically reload inside the container.
How can a container directly see files that live on your host development machine?

## Prediction
1. If you mount a host directory into a container, does Docker copy the files or share the exact same underlying disk inodes?
2. If the container process edits a file inside a bind mount, will the change immediately appear on the host?
3. Which has faster I/O on macOS Docker Desktop: a named volume or a host bind mount?

## Why this matters
Bind mounts power modern local development environments (live reload, nodemon, uvicorn `--reload`). But using bind mounts in production creates catastrophic security holes, host-coupling problems, and severe filesystem I/O degradation on macOS and Windows due to virtualization file sharing overhead (gRPC-FUSE / VirtioFS).

## First principles
1. **Kernel Bind Mount**:
   A Linux kernel primitive that makes an existing directory subtree visible at another mount point in the filesystem hierarchy.
2. **Bind Mount vs. Named Volume**:
   - **Bind Mount** (`-v /path/on/host:/path/in/container`): You specify the exact host path. Docker mounts your host folder directly. Subject to host file permissions and UID mismatches.
   - **Named Volume** (`-v my-vol:/path/in/container`): Docker engine manages the directory location (`/var/lib/docker/volumes/`). Isolated, managed, high-performance.
3. **The macOS / Windows Virtualization Tax**:
   On macOS/Windows, the Docker daemon runs inside a Linux VM. For a bind mount to work, every file read/write must cross the host-to-VM virtualization boundary via a filesystem sharing protocol. For large codebases (e.g. `node_modules` with 50,000 files), bind mounts can be 10x to 50x slower than named volumes.

| Dimension | Named Volume | Bind Mount |
| :--- | :--- | :--- |
| **Managed by** | Docker Engine daemon | User / Host filesystem |
| **Path definition** | Named identifier (`pgdata`) | Absolute host path (`/Users/...`) |
| **Performance (macOS/Win)** | Native VM speed (Fastest) | Virtualization bridge (Slower for many small files) |
| **Primary Use Case** | Databases, persistent state, CI | Live code reload during development |

## Mental model

```text
HOST MACHINE (macOS / Linux)
┌────────────────────────────────────────────────────────┐
│  /Users/tushar/.../code/app                            │
│  └── hello.txt ◄────────────┐                          │
└─────────────────────────────┼──────────────────────────┘
                              │ Bidirectional Kernel Mirroring
                              ▼
CONTAINER (dfs-bind-demo)
┌────────────────────────────────────────────────────────┐
│  /workspace                                            │
│  └── hello.txt ◄────────────┘                          │
│                                                        │
│  Edit on host  ──► Immediately visible in container!   │
│  Edit in container ──► Immediately written to host!    │
└────────────────────────────────────────────────────────┘
```

## Build it
Review [experiments/run_experiment.sh](../experiments/run_experiment.sh).
It mounts the local directory `code/app` to `/workspace` inside an Alpine container.

## Run it
Execute the experiment runner:

```bash
./phases/13-bind-mounts-and-development-workflows/01-host-filesystem-mirroring/experiments/run_experiment.sh
```

## Inspect it
1. Notice that `hello.txt` is read by the container.
2. The experiment edits `hello.txt` on the host, and the running container immediately outputs the new text without restarting.
3. The container creates `from_container.txt`, which appears instantly on your host disk!

## Break it
Mount a non-existent host file as a bind mount using `-v`:
```bash
docker run --rm -v $(pwd)/nonexistent_folder:/data alpine:latest ls /data
```
Notice what Docker does: **It automatically creates a directory named `nonexistent_folder` on your host machine!**
This implicit directory creation is a notorious source of bugs (e.g. accidentally creating empty folders owned by `root`).
Clean up: `rm -rf nonexistent_folder`.

## Debug it
When encountering `Permission denied` inside a bind mount:
1. Check process UID inside container: `docker exec <c> id -u`.
2. Check host file ownership: `ls -la /path/on/host`.
3. If container runs as UID `1000` (non-root) and host files are owned by UID `501` or `0`, the container process cannot write to the bind mount. Fix by aligning UIDs with `--user $(id -u):$(id -g)`.

## Modify it
Mount a single file as read-only:
```bash
docker run --rm -v $(pwd)/phases/13-bind-mounts-and-development-workflows/01-host-filesystem-mirroring/code/app/hello.txt:/config.txt:ro alpine:latest sh -c "echo 'hack' >> /config.txt"
```
Verify that the append fails with `Read-only file system`.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- Verification of bidirectional editing between host and container.
- Comparison of named volumes vs bind mounts.
- Host permissions behavior observed.

## Questions for mastery
1. Why should you exclude `node_modules` or Python `.venv` from host bind mounts?
2. What is the difference between `-v /host:/container` and `--mount type=bind,source=/host,target=/container`?
3. Why do bind mounts present a security hazard in multi-tenant environments?

## What comes next
We know how to supply files and state. Now we examine configuration: **How do we make the same container image behave differently across development, staging, and production?** Proceed to **Phase 14: Environment Variables and Configuration**.
