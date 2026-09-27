# Core Mental Models: Docker From First Principles

Clear systems thinking requires replacing false analogies with accurate architectural mental models. This document details the 7 primary mental models of container engineering.

---

## 1. Container vs. Virtual Machine vs. Process

### Inaccurate Mental Model (The Cargo Cult)
> "A container is a mini-VM running a lightweight operating system inside a sandbox."

### Accurate First-Principles Mental Model
> A container is a standard host process wrapped in Linux kernel namespaces (which limit what it can *see*), cgroups (which limit what it can *consume*), and a union filesystem mount (which limits what files it can *touch*). There is no guest kernel.

```text
VIRTUAL MACHINE ARCHITECTURE:
┌─────────────────────────────────────────────────────────────┐
│  Host OS & Kernel (Linux / macOS / Windows)                 │
├─────────────────────────────────────────────────────────────┤
│  Hypervisor (Type 1 or Type 2: KVM, Hyper-V, VirtualBox)    │
├──────────────────────────────┬──────────────────────────────┤
│  Guest VM 1:                 │  Guest VM 2:                 │
│  ┌────────────────────────┐  │  ┌────────────────────────┐  │
│  │ Guest Linux Kernel     │  │  │ Guest Linux Kernel     │  │
│  ├────────────────────────┤  │  ├────────────────────────┤  │
│  │ Virtual Disk, vNIC     │  │  │ Virtual Disk, vNIC     │  │
│  ├────────────────────────┤  │  ├────────────────────────┤  │
│  │ User Processes (Python)│  │  │ User Processes (Node)  │  │
│  └────────────────────────┘  │  └────────────────────────┘  │
└──────────────────────────────┴──────────────────────────────┘

CONTAINER ARCHITECTURE (Native Linux):
┌─────────────────────────────────────────────────────────────┐
│             Single Shared Host Linux Kernel                 │
│   (Manages all CPU, RAM, Devices, Syscalls, Intercepts)     │
├──────────────────────────────┬──────────────────────────────┤
│  Container 1 (PID Namespace) │  Container 2 (PID Namespace) │
│  - PID 1 (Python app)        │  - PID 1 (Postgres)          │
│  - Net Namespace (eth0)      │  - Net Namespace (eth0)      │
│  - Mount Namespace (rootfs)  │  - Mount Namespace (rootfs)  │
│  - Cgroup (max 512MB RAM)    │  - Cgroup (max 2 CPUs)       │
└──────────────────────────────┴──────────────────────────────┘
```

> **Platform Note (macOS / Windows):**
> Because macOS and Windows kernels do not provide Linux namespaces and cgroups, Docker Desktop runs a tiny, optimized Linux VM under the hood (HyperKit, Virtualization.framework, or WSL2). The Docker daemon and all your containers execute on that single shared Linux VM kernel!

---

## 2. Image Layers and the Union Filesystem (`overlay2`)

An image is not a disk image. It is an immutable stack of compressed directory changes.

```text
RUNNING CONTAINER FILESYSTEM:
┌─────────────────────────────────────────────────────────────┐
│ Container Writable Layer (Read-Write)                       │
│ - New files created (/tmp/session.log)                     │
│ - Modified files (copied up via Copy-on-Write)              │
│ - Whiteout markers for deleted files (.wh.old_config)       │
├─────────────────────────────────────────────────────────────┤
│ Image Layer 3 (Read-Only): RUN pip install -r req.txt       │
│ - /usr/local/lib/python3.11/site-packages/...               │
├─────────────────────────────────────────────────────────────┤
│ Image Layer 2 (Read-Only): COPY app.py /app/app.py          │
│ - /app/app.py                                               │
├─────────────────────────────────────────────────────────────┤
│ Image Layer 1 (Read-Only): FROM python:3.11-slim            │
│ - Root filesystem: /bin, /lib, /etc, /usr                   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Merged View presented to Container
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ Process sees unified directory: /app, /usr, /etc, /tmp      │
└─────────────────────────────────────────────────────────────┘
```

- When the process **reads** a file: The kernel searches layers from top to bottom and returns the first instance found.
- When the process **modifies** a file from Layer 1: The kernel duplicates the file into the Container Writable Layer (Copy-on-Write) and edits it there. The original layer remains completely untouched.
- When the container is **deleted**: The Writable Layer is erased. The immutable image layers remain intact.

---

## 3. Container Networking: Port Publishing (`-p 8080:80`)

Containers get their own isolated network namespace. `localhost` inside a container refers to *that container's loopback interface*, not the host.

```text
HOST MACHINE (e.g. 192.168.1.50)
│
├── Port 8080 open (docker-proxy / iptables DNAT)
│     │
│     ▼ (Forward packets across virtual bridge)
├── Linux Bridge Interface (docker0 or br-xxx) (e.g., 172.18.0.1)
│     │
│     ├── veth pair (Virtual Ethernet cable)
│     │     │
│     │     ▼
│     └── CONTAINER A (Net Namespace)
│           ├── IP: 172.18.0.2
│           └── Listening on 127.0.0.1 & 0.0.0.0:80 (Nginx)
```

1. Browser on host sends request to `http://localhost:8080`.
2. Host kernel receives packet on TCP port 8080.
3. `iptables` NAT prerouting rule rewrites destination IP from `127.0.0.1:8080` to `172.18.0.2:80`.
4. Packet crosses virtual bridge interface into container's `eth0`.
5. Web server inside container reads packet on port 80.

---

## 4. Docker DNS and User-Defined Networks

Why does `curl http://api:5000` work inside a custom bridge network, but fail on the default bridge?

```text
                  ┌──────────────────────────────────────────────┐
                  │   User-Defined Bridge Network (app-network)  │
                  └──────┬────────────────────────────────┬──────┘
                         │                                │
        ┌────────────────▼───────────────┐ ┌──────────────▼──────────────┐
        │  Container: "web"              │ │  Container: "api"              │
        │  IP: 172.20.0.2                │ │  IP: 172.20.0.3                │
        │  /etc/resolv.conf:             │ │  Listening: 0.0.0.0:5000       │
        │    nameserver 127.0.0.11       │ └──────────────────────────────┘
        └──────────────┬─────────────────┘
                       │
                       │ 1. DNS Query: "Where is 'api'?"
                       ▼
        ┌────────────────────────────────┐
        │ Embedded Docker DNS Engine     │
        │ IP: 127.0.0.11:53              │
        │ Resolves "api" -> 172.20.0.3   │
        └────────────────────────────────┘
```

The Docker daemon intercepts DNS queries sent to `127.0.0.11` inside the container namespace and dynamically returns the IP of containers matching that service name.

---

## 5. Storage Primitives: Data vs. Container Lifecycle

```text
        ┌────────────────────────────────────────────────────────┐
        │                      HOST STORAGE                      │
        │                                                        │
        │   /var/lib/docker/volumes/my_db_data/_data  (Volume)   │
        │   /Users/tushar/projects/web/src            (Bind)     │
        └──────────┬───────────────────────────────┬─────────────┘
                   │                               │
       Volume Mount│                     Bind Mount│
                   ▼                               ▼
        ┌────────────────────────────────────────────────────────┐
        │                  CONTAINER FILESYSTEM                  │
        │                                                        │
        │   /var/lib/postgresql/data       /app/src              │
        │   (Persistent DB state)          (Live host code)      │
        │                                                        │
        │   /tmp (Ephemeral Writable Layer - destroyed on rm)   │
        └────────────────────────────────────────────────────────┘
```

- **Ephemeral Layer**: Tied to container lifecycle. Destroyed on `docker rm`.
- **Named Volume**: Managed by Docker Engine. Independent lifecycle. Survives container destruction. High performance across all platforms.
- **Bind Mount**: Tied directly to host path. Ideal for live reload during development.

---

## 6. Process Supervision: PID 1 and Signal Forwarding

In Unix, PID 1 (Init) is special:
1. It does not get default signal handlers. If a signal like `SIGTERM` arrives and PID 1 has not registered a handler, the kernel ignores it!
2. It must adopt and reap zombie child processes when parents terminate.

```text
CASE A: Shell Form in Dockerfile (BROKEN SIGNALS)
CMD python3 server.py
  Docker runs: /bin/sh -c "python3 server.py"
  PID 1 in container = /bin/sh
  PID 2 in container = python3 server.py
  --> "docker stop" sends SIGTERM to PID 1 (/bin/sh).
  --> /bin/sh does NOT forward SIGTERM to child!
  --> Application hangs for 10s until Docker sends SIGKILL!

CASE B: Exec Form in Dockerfile (CORRECT)
CMD ["python3", "server.py"]
  Docker runs: python3 server.py
  PID 1 in container = python3 server.py
  --> "docker stop" sends SIGTERM directly to python3!
  --> Python handles graceful shutdown immediately (<100ms).
```

---

## 7. Docker Engine Architecture: CLI to runc

What really executes your code?

```text
User Terminal: $ docker run -d -p 8080:80 nginx
     │
     │ 1. HTTP REST API over Unix Socket (/var/run/docker.sock)
     ▼
Docker Daemon (`dockerd`)
     │ (High-level coordination: images, routing, volumes)
     │
     │ 2. gRPC API
     ▼
containerd
     │ (Supervises containers, pulls image layers, manages snapshots)
     │
     │ 3. Exec CLI
     ▼
runc
     │ (OCI runtime: invokes kernel clone(), setns(), pivot_root, cgroups)
     ▼
Linux Kernel Process (Nginx) (Runs with isolated PID, Net, Mount namespaces)
```
Once the process is running, `runc` exits! The container is monitored by `containerd-shim`.
