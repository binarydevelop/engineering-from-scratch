# Lesson 00.1: Verifying the Engine and Client Split

## Motto
"The `docker` command does not run containers; it asks a background daemon to run them."

## Problem
When engineers first learn Docker, they treat the `docker` terminal command as a monolithic program that compiles and runs containers on their machine, much like `gcc` or `node`.
This mental model breaks immediately when:
- The terminal hangs with `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`.
- Port mappings and filesystem permissions behave differently on macOS and Windows than on Linux.
- Environment variables set on the host terminal are not present inside the container.

We need to uncover what the `docker` binary actually does when you invoke it in a terminal.

## Prediction
Before executing `docker version`, consider:
1. Why does `docker version` display two distinct sections: **Client** and **Server**?
2. If we kill the Docker desktop application or daemon, will `docker --help` still work? Will `docker ps` still work?

## Why this matters
If you believe `docker` is a local binary doing all the work, you cannot debug socket permission errors, remote deployment over SSH/TLS, CI/CD Docker-in-Docker pipelines, or the boundary between your host OS and the container engine.

## First principles
The Docker system is built on a **Client-Server architecture**:
1. **The Client (`docker`)**: A lightweight CLI compiled in Go. Its sole job is to parse your flags, package arguments into HTTP requests, send them over an IPC channel (Unix Domain Socket at `/var/run/docker.sock` or TCP socket), and format the returned JSON into terminal text.
2. **The Server (`dockerd`)**: The Docker Engine daemon. It listens on `/var/run/docker.sock`, exposes an HTTP REST API, manages storage, networks, and containers, and delegates container execution to `containerd` and `runc`.

On Linux, the daemon runs directly as a `systemd` unit on your host kernel.
On macOS and Windows, Docker Desktop launches a lightweight virtual machine running a minimal Linux kernel (`linuxkit`). The Unix socket on your host is forwarded into this VM.

## Mental model

```text
HOST TERMINAL (e.g. macOS / Darwin)
┌────────────────────────────────────────────────────────┐
│  $ docker ps                                           │
│       │                                                │
│       ▼                                                │
│  Docker CLI Client (Go binary)                         │
│       │                                                │
│       │ HTTP GET /v1.55/containers/json                │
│       ▼                                                │
│  Unix Domain Socket: /var/run/docker.sock              │
└───────┬────────────────────────────────────────────────┘
        │ (Crosses VM boundary on macOS / Windows Desktop)
        ▼
DOCKER ENGINE DAEMON (Linux Kernel)
┌────────────────────────────────────────────────────────┐
│  dockerd REST API Router                               │
│       │                                                │
│       ▼                                                │
│  containerd -> runc -> Linux Namespaces & Cgroups      │
└────────────────────────────────────────────────────────┘
```

## Build it
Rather than relying on the Docker CLI, we will build a raw Python client that speaks HTTP directly over the `/var/run/docker.sock` Unix Domain Socket.

See [inspect_socket.py](../code/inspect_socket.py):
It uses Python's standard `http.client` and `socket.socket(socket.AF_UNIX)` to issue:
- `GET /version`
- `GET /info`

## Run it
Execute the experiment script:

```bash
# Run from repository root
./phases/00-environment-and-orientation/01-verify-engine-and-client/experiments/run_experiment.sh
```

Or run the Python socket inspector manually:

```bash
python3 phases/00-environment-and-orientation/01-verify-engine-and-client/code/inspect_socket.py
```

## Inspect it
Compare the output of:
1. `docker version`
2. `docker info`
3. The raw JSON parsed by `inspect_socket.py`

Notice:
- `Client.Os`: `darwin` (if on Mac) or `linux` (if on Linux).
- `Server.Os`: `linux` in both cases!
- `Storage Driver`: `overlayfs` (or `overlay2`).

## Break it
Simulate a broken daemon connection by pointing the client to a non-existent socket:

```bash
DOCKER_HOST="unix:///tmp/fake.sock" docker ps
```

Expected error:
`Cannot connect to the Docker daemon at unix:///tmp/fake.sock. Is the docker daemon running?`

Notice that `docker --help` still works, because the client binary itself is intact; only the API connection failed.

## Debug it
When Docker reports connection failure:
1. Verify if `/var/run/docker.sock` exists:
   ```bash
   ls -la /var/run/docker.sock
   ```
2. Verify permissions on the socket:
   ```bash
   # On Linux, your user must belong to the 'docker' group
   groups $USER
   ```
3. Check daemon process status:
   ```bash
   # Linux:
   sudo systemctl status docker
   # macOS:
   pgrep -fl Docker
   ```

## Modify it
Open [inspect_socket.py](../code/inspect_socket.py) and add a call to query the `/images/json` endpoint. Print out the ID and repository tags of any images currently stored locally on your machine.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md).
- Document your client and server versions.
- Note whether your engine runs natively on Linux or inside a VM (macOS/WSL2).
- Paste the raw JSON output from `inspect_socket.py`.

## Questions for mastery
1. Why does `docker` CLI not require `sudo` on macOS, but often requires `sudo` on a fresh Linux install?
2. Could you run the Docker CLI on an M3 MacBook and control a Docker daemon running on an Ubuntu server in AWS? How?
3. If the Docker daemon crashes, what happens to existing running containers?

## What comes next
Now that we know the Docker CLI is an HTTP client speaking to a daemon managing Linux primitives, we must ask: **What does the daemon actually manage?**
Before understanding containers, we must understand processes. Proceed to **Phase 01: Processes Before Containers**.
