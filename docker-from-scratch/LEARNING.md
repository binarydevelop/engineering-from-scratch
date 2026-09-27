# Learning Methodology: docker-from-scratch

Welcome to **docker-from-scratch**.

This repository is an **experimental curriculum**, not a command cheatsheet or documentation dump. It is designed for software engineers who can code and already use Docker, but currently treat it as a black box.

---

## The Core Philosophy

> **Understand it. Build it. Inspect it. Break it. Fix it. Ship it.**

Most developers interact with Docker through cargo-culting: copying a `Dockerfile` from Stack Overflow, pasting a `docker-compose.yml` snippet, and running `docker compose up`. When something breaks—ports conflict, volumes fail to persist, DNS cannot resolve a service name, or a container exits with code 137—they resort to blindly running `docker restart` or `docker system prune -a --volumes` without understanding what actually happened.

Here, you will not memorize commands. You will observe the operating system and container engine machinery from first principles.

---

## The 10 Invariant Rules of Study

1. **Never copy-paste blindly**: Type the commands. Reading a command does not build muscle memory or spatial intuition for what changes on your system.
2. **Predict before executing**: Before every single command, pause and answer:
   - *What state will change on disk?*
   - *What processes will start or stop?*
   - *What will appear on stdout/stderr?*
   - *What exit code will be returned?*
3. **Inspect after every creation**: Never trust that a command "worked" just because it returned code 0. Use `docker inspect`, `docker ps -a`, `netstat`, `curl`, and `ls` to verify the actual state changes.
4. **Intentionally break every working setup**: You do not understand a container until you have broken its network, starved its memory, cut off its dependencies, and observed how it fails.
5. **Never proceed while something feels magical**: If an abstraction works and you cannot explain *why* (e.g., why a container can reach `redis:6379` by hostname), stop. Peel back the layer until the mechanism is obvious.
6. **Compare prediction with reality**: When your prediction fails, treat it as a discovery of a gap in your mental model.
7. **Recreate without looking**: The ultimate test of mastery is starting from an empty directory with an empty terminal and building the system from memory.
8. **Collect evidence**: Fill out `outputs/evidence-template.md` for each lesson. Your evidence log is proof of understanding.
9. **Problem first, concept second, tool third**: Never introduce a tool (like Docker Compose or Volumes) before feeling the acute engineering pain it solves.
10. **Separate container lifecycle from host lifecycle**: Understand the boundary between your host OS, Docker daemon, VM (on macOS/Windows), and isolated container processes.

---

## The Learning Loop

Every lesson moves through this exact experimental cycle:

```text
       ┌───────────────────────────────┐
       │             READ              │
       │    (Problem & First Principle)│
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │            PREDICT            │
       │  (What will happen on disk/OS)│
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │             BUILD             │
       │  (Write the minimal code)     │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │             RUN               │
       │  (Execute & observe output)   │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │           INSPECT             │
       │  (Inspect inspect/ps/ip/ports)│
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │            EXPLAIN            │
       │ (State the mechanism clearly) │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │            MODIFY             │
       │ (Alter configuration & verify)│
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │            BREAK              │
       │   (Inject deliberate faults)  │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │            DEBUG              │
       │ (Diagnose symptom to cause)   │
       └──────────────┬────────────────┘
                      ▼
       ┌───────────────────────────────┐
       │           EVIDENCE            │
       │ (Log commands, outputs, proof)│
       └───────────────────────────────┘
```

---

## Prerequisites

- Ability to read and write basic Python (HTTP servers, socket basics, scripts).
- Comfort in a POSIX terminal (`zsh` or `bash`, pipes, redirection, signals).
- Basic understanding that programs execute as processes in an operating system.
- Docker Desktop or Docker Engine installed on your machine.
- No prior knowledge of Linux kernel namespaces, cgroups, overlayfs, or container networking is assumed. We build them from scratch.
