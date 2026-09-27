# Curriculum Roadmap: docker-from-scratch

A comprehensive, first-principles progression from bare operating-system processes to full multi-container systems.

---

## Phase Overview

| Phase | Title | Goal | Prerequisites | Key Concepts | Final Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **00** | **Environment & Orientation** | Verify host engine, client, and client-server socket communication | Terminal basics | Client-Server split, `/var/run/docker.sock`, Darwin vs Linux | `scripts/verify_env.sh` & environment report |
| **01** | **Processes Before Containers** | Master host processes before introducing container abstractions | Python basics | PID, PPID, std streams, signals, exit codes, process states | Host process supervisor experiment |
| **02** | **Your First Container** | Dissect `hello-world` to prove container lifecycle vs process lifecycle | Phase 01 | Image vs Container, state lifecycle, exited containers | Inspection artifact & container lifecycle map |
| **03** | **Images From First Principles** | Explore image composition as immutable tarball layers + JSON metadata | Phase 02 | Content-addressable hashes, manifest, rootfs layers | Layer inspection script & image report |
| **04** | **Containers & Filesystems** | Prove isolation via the ephemeral Copy-on-Write writable layer | Phase 03 | Union mounts (`overlay2`), upperdir, lowerdir, CoW | Two-container isolated mutation experiment |
| **05** | **Building Images with Dockerfiles** | Translate manual container assembly into declarative Dockerfiles | Phase 04 | `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`, `ENTRYPOINT` | Custom Python HTTP service image |
| **06** | **Image Layers & Build Cache** | Optimize build caching by ordering Dockerfile instructions by volatility | Phase 05 | Build cache hashes, cache busting, dependency layering | Optimized caching benchmark report |
| **07** | **Registries, Tags, Pull & Push** | Understand how images travel across networks via the OCI Distribution API | Phase 06 | Registry, repository, mutable tags vs immutable SHA digests | Image provenance and pull verification script |
| **08** | **Networking: Start With localhost** | Break the "localhost = my computer" illusion | Phase 05 | Loopback interface, network namespace isolation, `0.0.0.0` | Localhost trap reproduction experiment |
| **09** | **Ports & Publishing** | Understand `-p` as host NAT / iptables forwarding rules | Phase 08 | `EXPOSE` vs `-p`, DNAT, packet routing, host port binding | Port forwarding diagnostic test |
| **10** | **Docker Bridge Networks** | Connect two isolated containers across a virtual Linux Ethernet bridge | Phase 09 | Software bridge, `veth` pairs, subnet allocation, packet flow | Multi-container manual ping/curl test |
| **11** | **DNS & Service Discovery** | Resolve service names dynamically without hardcoding volatile IP addresses | Phase 10 | Embedded DNS (`127.0.0.11`), user-defined vs default bridge | Dynamic service discovery verification |
| **12** | **Volumes & Persistence** | Decouple persistent data lifecycle from ephemeral container lifecycle | Phase 04 | Named volumes, `/var/lib/docker/volumes/`, data durability | Database crash & persistence test |
| **13** | **Bind Mounts & Workflows** | Mirror live host code into containers for real-time development | Phase 12 | Bind mounts, host inode sharing, permission mapping | Live-reload dev workflow experiment |
| **14** | **Environment Variables & Config** | Separate code from configuration across runtime environments | Phase 05 | 12-Factor config, `.env` files, `-e` injection, precedence | Multi-environment config switcher |
| **15** | **Resource Limits & cgroups** | Prevent rogue processes from exhausting host memory and CPU | Phase 01 | Linux cgroups, memory limits, CPU quotas, OOM-killer (137) | Controlled OOM crash & recovery lab |
| **16** | **Isolation & Namespaces** | Demystify how the kernel isolates PIDs, networks, and mount points | Phase 01 | PID, Net, Mount, UTS, IPC, User namespaces, `runc` | Namespace inspection audit |
| **17** | **Signals, PID 1, & Lifecycle** | Ensure graceful application shutdown without 10-second SIGKILL delays | Phase 01 | PID 1 responsibilities, shell vs exec form, SIGTERM trapping | Graceful shutdown verification test |
| **18** | **Logs & stdstreams** | Capture and route application output via standard streams | Phase 01 | `stdout`/`stderr` multiplexing, JSON logging driver, rotation | Container log streaming artifact |
| **19** | **Health Checks & Dependencies** | Distinguish between "process is alive" and "service is ready" | Phase 05 | `HEALTHCHECK`, probe intervals, retries, startup grace | Self-healing healthcheck probe lab |
| **20** | **Docker Compose From Scratch** | Replace fragile multi-step `docker run` scripts with declarative YAML | Phases 10-14 | Compose spec, services, declarative topology vs engine API | 3-service manual run vs Compose translation |
| **21** | **Under the Hood: `docker compose up`** | Trace the exact sequence of events during Compose execution | Phase 20 | YAML parsing, variable expansion, DAG resolution, resource creation | Step-by-step Compose execution tracer |
| **22** | **Compose Networking & DNS** | Master inter-service communication via automatic Compose networks | Phases 11, 21 | Default Compose bridge, automatic alias DNS, isolation | Multi-tier network isolation lab |
| **23** | **Compose Volumes & Persistent State** | Understand data survival across `down`, `up`, and `down -v` | Phases 12, 21 | Named volume lifecycle in Compose, project prefixes, `-v` | PostgreSQL persistence verification |
| **24** | **Debugging Containers Systematically** | Diagnose broken containers using structured symptom-based reasoning | Phases 08-19 | 10-step triage flowchart, inspecting state, log analysis | Broken container diagnostic report |
| **25** | **Docker Security Foundations** | Eliminate dangerous root privileges and understand Docker socket risks | Phase 16 | Non-root users, Linux capabilities (`cap-drop`), socket attacks | Hardened container security audit |
| **26** | **Image Optimization** | Shrink bloated multi-gigabyte images into lean, secure artifacts | Phase 06 | `.dockerignore`, minimal base images (alpine/distroless), layers | Before/after image optimization report |
| **27** | **Multi-Stage Builds** | Separate build tools/compilers from lightweight runtime containers | Phase 26 | Multi-stage `FROM ... AS`, artifact extraction, zero build bloat | 10x size reduction compiled app build |
| **28** | **Container Debugging Without Magic** | Solve 8 real-world broken infrastructure scenarios without hints | Phase 24 | Port mismatches, crashloops, missing envs, DNS, races | 8 completed diagnostic writeups |
| **29** | **Capstone: Rebuild the System Design Lab** | Progressively assemble a 6-service production architecture from scratch | All prior | App, Postgres, Redis, NATS, Prometheus, Grafana | Complete 14-step multi-tier system |
| **30** | **The Final Mental Model** | Trace a single `docker compose up` command down to kernel execution | All prior | CLI -> Daemon -> containerd -> runc -> Namespaces -> cgroups | Definitive end-to-end execution blueprint |
