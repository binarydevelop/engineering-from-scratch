# Lesson: The Complete End-to-End Mental Model of Docker Execution

## Motto
"Docker is not an operating system inside a file; it is the coordination of Linux kernel namespaces, control groups, union filesystems, and virtual networking around a standard process."

## Problem
A software engineer types `docker compose up -d` or `docker run -d -p 8080:80 nginx`. In less than two seconds, a web server is answering requests on localhost. To the uninitiated engineer, this looks like magic: did Docker boot a virtual machine? Did it create a new operating system? Where are the files stored? How did port 8080 get mapped? What happens when a request arrives?

## Prediction
By tracing the lifecycle of `docker compose up` through all 14 layers—from the keystroke in the terminal down to kernel data structures—we will demystify the entire abstraction stack. We can answer precisely: "What exactly exists on my computer right now?"

## Why this matters
When production incidents strike, high-level abstractions dissolve. Knowing that a container is just a Linux process governed by `nsproxy` and `cgroup` structs in the kernel turns panic into methodical diagnostic engineering. You will never again wonder why a file disappeared, why a port was blocked, or why a container stopped responding to signals.

## First principles
Tracing `docker compose up` through all 14 layers:

1. **Terminal:** You execute `docker compose up -d`. The shell expands variables and invokes the Docker CLI client binary.
2. **CLI:** The Compose CLI parses `docker-compose.yml`, merges `.env` files, builds a Directed Acyclic Graph (DAG) of dependencies, and validates configuration schema.
3. **Engine API:** The CLI translates your declarative compose spec into a sequence of HTTP REST API calls transmitted across `/var/run/docker.sock` to `dockerd` (e.g. `POST /v1.45/networks/create`, `POST /v1.45/containers/create`).
4. **Images:** The daemon checks its local content-addressable store. If missing, it fetches the manifest list, config JSON, and diff layer tarballs indexed by immutable SHA-256 digests.
5. **Container:** The daemon constructs an OCI (Open Container Initiative) runtime bundle consisting of `config.json` and a root filesystem path, delegating execution to `containerd` and `runc`.
6. **Namespaces:** `runc` invokes the Linux `clone()` syscall with flags `CLONE_NEWPID`, `CLONE_NEWNS`, `CLONE_NEWNET`, `CLONE_NEWIPC`, `CLONE_NEWUTS`, `CLONE_NEWCGROUP`. The new process is given isolated views of process trees, mounts, networks, and hostnames.
7. **Control Groups (cgroups):** `runc` creates control group entries under `/sys/fs/cgroup/` to enforce resource bounds: `memory.max`, `cpu.max`, `pids.max`.
8. **OverlayFS (CoW):** The storage driver mounts immutable image layers as read-only `lowerdir` folders and mounts a thin read-write directory as `upperdir`, producing a unified `merged` root directory.
9. **Virtual Bridges:** The network subsystem creates a virtual ethernet pair (`veth`). One interface is moved into the container's network namespace as `eth0`; the other connects to the virtual bridge (`docker0` or `br-*`).
10. **Embedded DNS:** The daemon populates `/etc/resolv.conf` with `nameserver 127.0.0.11` on user-defined networks, routing hostname queries directly to the daemon's internal resolver.
11. **Volumes:** Stateful directories are bind-mounted directly from the host filesystem (`/var/lib/docker/volumes/...`), bypassing the OverlayFS copy-on-write overhead and surviving container deletion.
12. **Ports & NAT:** The daemon programs Linux kernel `iptables` / `nftables` DNAT rules and spawns `docker-proxy` userland processes to route traffic from host ports to private container IP addresses.
13. **PID 1:** Inside the container's PID namespace, the target application (or `tini` / `docker-init`) executes as PID 1, assuming responsibility for signal handling and orphan process reaping.
14. **Health & Logs:** The daemon attaches pipes to file descriptors 1 (stdout) and 2 (stderr), streaming log frames into rotation buffers while periodically executing healthcheck probes.

## Mental model
```
[Terminal CLI: docker compose up]
       | (Unix Domain Socket /var/run/docker.sock)
       v
[Docker Daemon (dockerd)]
       | (gRPC)
       v
[containerd] ---> [containerd-shim] ---> [runc]
                                            |
       +------------------------------------+------------------------------------+
       |                                    |                                    |
       v                                    v                                    v
[Linux Namespaces]                  [cgroups v2]                         [OverlayFS]
- PID: process is PID 1             - memory.max                         - lowerdir (read-only)
- NET: veth0 <-> br-custom          - cpu.max                            - upperdir (read-write)
- MNT: pivot_root to merged         - pids.max                           - merged (rootfs view)
```

## Build it
1. `code/trace_full_stack.py`: An inspection engine that walks through all 14 layers in real-time, verifying daemon sockets, content-addressable storage, namespaces, cgroups, OverlayFS directories, bridges, and DNS entries.
2. `experiments/run_experiment.sh`: Automated execution script running the full-stack audit.

## Run it
Run the trace script:
```bash
./phases/30-final-mental-model/01-end-to-end-execution-trace/experiments/run_experiment.sh
```

## Inspect it
Check the host process table to verify that container processes are visible from the host:
```bash
docker inspect <container> --format '{{.State.Pid}}'
ps -fp <PID>
```
Notice that from the host's perspective, the containerized application is just a regular Linux process running alongside all other system processes.

## Break it
Kill the host process directly:
```bash
kill -9 <host_pid>
docker ps
```
The container immediately transitions to `Exited (137)`. Docker did not keep running without the process—because the process *is* the container.

## Debug it
Whenever a container misbehaves, walk backwards up the 14 layers:
1. Is the process alive in the host process table?
2. Did it exceed cgroup memory limits (`OOMKilled`)?
3. Is OverlayFS full or out of inodes?
4. Is `iptables` forwarding packets to the correct bridge IP?
5. Is `/etc/resolv.conf` pointing to `127.0.0.11`?

## Modify it
Inspect `/proc/<host_pid>/status` and `/proc/<host_pid>/cgroup` inside the Docker VM or Linux host to see the exact kernel data structures governing container execution.

## Evidence
Running `run_experiment.sh` outputs:
```
================================================================================
PHASE 30: THE FINAL MENTAL MODEL - END-TO-END EXECUTION TRACE
================================================================================

[Layer 1: Terminal & CLI]
  Command: 'docker compose up -d' or 'docker run'
  Role: CLI parses flags, loads environment (.env), builds compose DAG model.

[Layer 2: Docker Engine REST API]
  Unix Socket: /var/run/docker.sock exists and is accessible.
  Protocol: HTTP/1.1 over AF_UNIX sockets (POST /v1.45/containers/create).

[Layer 3: Image Layers & Content-Addressable Storage]
  Content-Addressable Blobs: Registered image tags present.
  Storage: Rootfs tarballs hashed with SHA-256 and chained into immutable parent-child DAGs.

[Layer 4: Container Execution Spec (OCI Bundle)]
  Spec: Docker daemon passes an OCI bundle (config.json + rootfs) to containerd / runc.

[Layer 5: Linux Namespaces (The Isolation Illusion)]
  * PID     : Isolates process IDs; process sees itself as PID 1.
  * Mount   : Isolates mount points; process sees isolated root filesystem.
  * Net     : Isolates network devices, routing tables, port bindings, loopback.
  * IPC     : Isolates System V IPC and POSIX message queues.
  * UTS     : Isolates hostname and NIS domain name.
  * User    : Maps container UID/GID to different host UID/GID.
  * Cgroup  : Isolates cgroup root hierarchy view.

[Layer 6: Control Groups (cgroups v2 - Resource Governance)]
  Enforcement: Kernel throttles CPU, limits memory, and prevents fork-bombs.

[Layer 7: Storage Driver - OverlayFS (CoW)]
  lowerdir : Immutable read-only base layers stacked bottom-to-top.
  upperdir : Thin, read-write layer unique to this container instance.
  workdir  : Internal atomic transaction staging directory.
  merged   : Unified virtual directory presented to the container process.

[Layer 8: Virtual Network Bridges & veth Pairs]
  Plumbing: Linux kernel creates a virtual ethernet pair.
  Switching: Host end attaches to a virtual Linux bridge.

[Layer 9: Embedded DNS (127.0.0.11)]
  Interception: /etc/resolv.conf directs queries to internal daemon DNS.
  Resolution: Maps service names to dynamic container IPs.

[Layer 10: Persistent Volumes]
  Bypass: Volume directories completely bypass OverlayFS, writing directly to host storage.

[Layer 11: Ports & NAT Publishing]
  Mechanisms: iptables DNAT rules rewrite inbound packets from host ports.

[Layer 12: PID 1 & Signal Traps]
  Special Role: Reaps zombie orphan processes and traps POSIX signals.

[Layer 13: Health Probes]
  Reconciliation: Daemon polls test probes and gates startup dependencies.

[Layer 14: Logs & Standard Streams]
  Multiplexing: runc captures stdout and stderr, streaming into JSON logs.

================================================================================
WHAT EXACTLY EXISTS ON MY COMPUTER RIGHT NOW?
================================================================================
1. There is NO such physical object called a "container".
2. There are standard Linux processes executing code directly on CPU cores.
3. There are kernel data structures tagging those processes:
   - nsproxy struct: Points to namespaces defining what the process can SEE.
   - css_set struct: Points to cgroups defining what the process can USE.
4. There is a directory on disk mounted via overlayfs defining what the process can READ/WRITE.
5. There are virtual cables (veth pairs) defining how the process can COMMUNICATE.
================================================================================
```

## Questions for mastery
1. What is the fundamental difference between a virtual machine hypervisor and a container runtime?
2. If a container's filesystem is composed of stacked layers, why doesn't file reading suffer a performance penalty for each layer?
3. How does Docker Desktop on macOS differ from running Docker natively on a Linux host?

## What comes next
Docker is no longer magic.

A container is a process with carefully constructed isolation, filesystem, networking, resources, and configuration.

Now that we understand the machinery underneath our development environment, we can return to system design and reason about multi-service systems without treating the infrastructure as a black box.
