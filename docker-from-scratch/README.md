# docker-from-scratch

> **Understand it. Build it. Inspect it. Break it. Fix it. Ship it.**

An experimental, first-principles curriculum that demystifies Docker for software engineers. Instead of memorizing Docker CLI commands or copy-pasting Stack Overflow snippets, you will build, inspect, break, and debug containers from the ground up.

---

## The Core Philosophy

Most engineers treat Docker as a black box:

```text
                  THE BLACK BOX (Cargo Cult)
   ┌────────────────────────────────────────────────────────┐
   │  "docker compose up"                                   │
   │         │                                              │
   │         ▼                                              │
   │  ✨ Magic Container Land ✨                            │
   │  (Mini-VMs? Linux computers inside my laptop?)         │
   │         │                                              │
   │  Everything works until:                               │
   │  - Port conflict on 8080                               │
   │  - Service A cannot connect to Service B               │
   │  - Data vanishes after reboot                          │
   │  - Container exits with code 137                       │
   │         │                                              │
   │  Desperate solution: "docker system prune -a --force"  │
   └────────────────────────────────────────────────────────┘
```

This repository replaces that black box with an accurate, mechanical mental model:

```text
                THE FIRST-PRINCIPLES REALITY
   ┌────────────────────────────────────────────────────────┐
   │  Host Linux Kernel (or VM kernel on macOS/Windows)     │
   ├────────────────────────────────────────────────────────┤
   │  Standard Host Process (Python / Go / Node / Postgres) │
   │    ├── PID Namespace     --> Sees only its own process │
   │    ├── Net Namespace     --> Has dedicated eth0 & port │
   │    ├── Mount Namespace   --> Sees stacked Overlay2 dir │
   │    └── Cgroup Limits     --> Throttled RAM & CPU       │
   └────────────────────────────────────────────────────────┘
```

A container is not a virtual machine. **A container is a standard host process with isolated visibility (namespaces), bounded resources (cgroups), and a layered Copy-on-Write filesystem.**

---

## What You Will Master

By completing this curriculum, you will answer every one of these questions without guessing:

1. **The Core Lifecycle**: What actually happens under the hood when I type `docker run`?
2. **Process vs. Container**: How is a container fundamentally different from a process?
3. **The Image Anatomy**: What is an image, what are layers, and why are they immutable?
4. **Build Caching**: Why does changing line 2 of a Dockerfile bust the cache for every step after it?
5. **Registries**: How do images travel across the internet via the OCI Distribution API?
6. **Filesystem Isolation**: What happens to files written inside a container when the container stops or is deleted?
7. **The Localhost Trap**: Why does `curl localhost:8000` fail inside a container even when an app is running on port 8000?
8. **Port Forwarding**: What does `-p 8080:80` actually configure in kernel routing and iptables?
9. **Bridge Networks**: What is a virtual bridge, what is a `veth` pair, and how do packets move across them?
10. **Service Discovery**: How does Docker's embedded DNS (`127.0.0.11`) resolve service names like `redis` or `db`?
11. **Persistence**: What is the exact mechanical difference between an ephemeral layer, a named volume, and a bind mount?
12. **Signals & Shutdown**: Why does PID 1 matter, why does `docker stop` sometimes take 10 seconds, and how do you handle SIGTERM properly?
13. **Health Checks**: Why does a container being "running" not mean your service is ready to receive traffic?
14. **Docker Compose**: What does Compose actually do? (Hint: it's not a runtime; it's a DAG compiler calling the Engine API).
15. **Systematic Diagnostics**: How do you triage a broken multi-service system using an orderly 10-step protocol instead of guessing?

---

## Architectural Progression

```text
Processes Before Containers
            │
            ▼
    Your First Container
            │
            ▼
 Images & Layers (Overlay2)
            │
            ▼
   Filesystem & CoW State
            │
            ▼
    Dockerfile Primitives
            │
            ▼
 Container Networking & Ports
            │
            ▼
Bridges & Embedded Docker DNS
            │
            ▼
 Volumes & Host Bind Mounts
            │
            ▼
Namespaces & cgroup Throttling
            │
            ▼
Signals, PID 1, & stdstreams
            │
            ▼
 Docker Compose Specification
            │
            ▼
Multi-Stage Builds & Hardening
            │
            ▼
  8 Hands-On Debugging Labs
            │
            ▼
  Progressive 14-Step Capstone
 (App + Postgres + Redis + NATS
   + Prometheus + Grafana)
            │
            ▼
     The Final Mental Model
```

---

## Audience & Assumptions

**We assume you:**
- Can write basic Python scripts.
- Know how to run commands, pipe streams, and navigate directories in a terminal.
- Understand that software executes as processes in an operating system.
- Have used `docker run` or `docker compose up` at least once, even if as a complete black box.

**We do NOT assume prior knowledge of:**
- Linux namespaces (`CLONE_NEWPID`, `CLONE_NEWNET`, etc.)
- cgroups (v1 or v2 resource controllers)
- Overlay filesystems (`lowerdir`, `upperdir`, `merged`)
- Linux virtual bridges, `veth` pairs, or NAT routing
- OCI image specifications or Docker daemon architecture

---

## Curriculum Structure

The curriculum is organized into **31 dependency-ordered phases**:

- **Phase 00**: Environment & Orientation (`scripts/verify_env.sh`, client-server split)
- **Phase 01**: Processes Before Containers (PID, PPID, signals, exit codes, stdin/stdout/stderr)
- **Phase 02**: Your First Container (`hello-world` dissected, container vs image lifecycle)
- **Phase 03**: Images From First Principles (Layers, content-addressable storage, JSON config)
- **Phase 04**: Containers & Filesystems (Copy-on-Write, ephemeral writable layers, `overlay2`)
- **Phase 05**: Building Images with Dockerfiles (`FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`, `ENTRYPOINT`)
- **Phase 06**: Image Layers & Build Cache (Instruction ordering, cache busting, dependency optimization)
- **Phase 07**: Registries, Tags, Pull & Push (OCI Distribution API, tags vs immutable SHA digests)
- **Phase 08**: Container Networking: Start With localhost (The loopback trap, `127.0.0.1` vs `0.0.0.0`)
- **Phase 09**: Ports & Publishing (`EXPOSE` vs `-p`, host NAT, iptables DNAT rules)
- **Phase 10**: Docker Bridge Networks (Virtual bridge `docker0`, `veth` pairs, subnet routing)
- **Phase 11**: Docker DNS & Service Discovery (Embedded DNS `127.0.0.11`, custom bridges vs default bridge)
- **Phase 12**: Volumes & Persistence (Decoupling data lifecycle from process lifecycle)
- **Phase 13**: Bind Mounts & Development Workflows (Host filesystem mirroring, live-reload)
- **Phase 14**: Environment Variables & Configuration (12-Factor config injection, defaults, `.env`)
- **Phase 15**: Resource Limits & cgroups (Memory limits, CPU shares, OOM-killer code 137)
- **Phase 16**: Isolation & Namespaces (PID, Mount, Net, UTS, IPC namespaces under the hood)
- **Phase 17**: Signals, PID 1, & Container Lifecycle (`SIGTERM`, grace periods, `SIGKILL`, exec vs shell form)
- **Phase 18**: Logs & stdstreams (`stdout`/`stderr` multiplexing, JSON logging driver)
- **Phase 19**: Health Checks & Dependencies (Process health vs application readiness, probe intervals)
- **Phase 20**: Docker Compose From First Principles (The pain of manual orchestration -> Compose specification)
- **Phase 21**: What Actually Happens During `docker compose up` (DAG compilation, API sequence)
- **Phase 22**: Compose Networking & DNS (Automatic bridge networks, service aliases, multi-tier isolation)
- **Phase 23**: Compose Volumes & Persistent State (Survival across `down`, `up`, and data wipe with `-v`)
- **Phase 24**: Debugging Containers (The 10-step diagnostic triage protocol)
- **Phase 25**: Docker Security Foundations (Non-root containers, dropped capabilities, socket risk)
- **Phase 26**: Image Optimization (Minimizing layers, `.dockerignore`, alpine vs debian)
- **Phase 27**: Multi-Stage Builds (Builder pattern, stripping build tools, zero-runtime bloat)
- **Phase 28**: Container Debugging Without Magic (8 real-world broken labs with symptoms, not solutions)
- **Phase 29**: Rebuild the System Design Lab (Progressive 14-step capstone architecture)
- **Phase 30**: The Final Mental Model (Complete execution trace from CLI keystroke to running process)

---

## How to Begin

Run the environment verification script to ensure your machine is ready:

```bash
# 1. Clone or navigate to the repository
cd docker-from-scratch

# 2. Verify your Docker engine and CLI
./scripts/verify_env.sh

# 3. Start Phase 00, Lesson 01
cd phases/00-environment-and-orientation/01-verify-engine-and-client
cat docs/en.md
```

---

## Platform Notes (macOS, Linux, Windows)

- **Native Linux**: The Docker daemon runs directly on your host kernel. Containers are real processes in your host's process tree (`ps aux`), and networks are real Linux bridges visible with `ip link`.
- **macOS with Docker Desktop**: macOS has a Darwin kernel (XNU), not Linux. Therefore, Docker Desktop transparently runs a lightweight virtualized Linux VM. When you type `docker run`, the container process runs inside that Linux VM.
- **Windows with WSL2**: Containers execute inside the WSL2 lightweight Linux utility VM.

Where kernel-specific commands (such as `lsns`, `iptables`, or direct `/proc` inspection) are used, lessons provide:
1. Native Linux execution commands.
2. VM inspection techniques for macOS/Windows Docker Desktop users.

---

> Docker is no longer magic.
>
> A container is a process with carefully constructed isolation, filesystem, networking, resources, and configuration.
>
> Now that we understand the machinery underneath our development environment, we can return to system design and reason about multi-service systems without treating the infrastructure as a black box.
