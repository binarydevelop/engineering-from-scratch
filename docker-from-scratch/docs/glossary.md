# Glossary of Container Primitives & Concepts

In container engineering, vague language causes bugs. This glossary contrasts common industry misconceptions with actual operating system and container engine realities.

---

| Term | What People Say / Common Misconception | What It Actually Is Under the Hood |
| :--- | :--- | :--- |
| **Container** | "A lightweight virtual machine." | An isolated group of standard host processes restricted by Linux kernel **namespaces** (visibility), **cgroups** (resource limits), and a layered **root filesystem**. No hypervisor or separate kernel is booted. |
| **Image** | "A packaged operating system or virtual disk." | A read-only, content-addressable collection of tarballs (**layers**) plus a JSON configuration file specifying default commands, environment variables, and filesystem mount points. |
| **Layer** | "A snapshot of the whole container." | A tar archive representing only the filesystem delta (added, modified, or deleted files marked by whiteout markers) created by a single step in an image build. Stored once and shared across images. |
| **Writable Layer (CoW)** | "Where the container's hard drive lives." | A thin read-write layer placed on top of immutable image layers by a union filesystem (such as `overlay2`). When a file from an image layer is modified, it is copied up to this writable layer (**Copy-on-Write**). |
| **Docker Daemon (`dockerd`)** | "The container runtime that executes programs." | A persistent background service exposing a REST API. It manages high-level constructs (images, networks, volumes) and delegates execution to low-level runtimes (`containerd` and `runc`). |
| **`containerd`** | "Internal Docker code." | An industry-standard core container runtime that manages complete container lifecycles: image transfer, storage, and container supervision. |
| **`runc`** | "A Docker helper tool." | The reference OCI (Open Container Initiative) runtime. A CLI wrapper that talks directly to the Linux kernel to create namespaces, configure cgroups, pivot root, and execute the container binary, then exits. |
| **Namespace** | "Virtual hardware or a sandbox." | A Linux kernel feature that isolates system resources so that a process sees only its own dedicated instance (e.g., PID namespace isolates process IDs; Network namespace isolates interfaces, routes, and iptables). |
| **cgroup (Control Group)** | "Software that limits CPU speed." | A Linux kernel subsystem that tracks, meters, and limits physical hardware resource usage (CPU cycles, memory bytes, I/O bandwidth, process count) for groups of processes. |
| **PID 1** | "The process you launch." | The first process inside a PID namespace. In Unix, PID 1 has unique kernel responsibilities: it does not receive default signal handlers (like SIGTERM unless explicitly trapped) and must reap orphaned child processes (zombies). |
| **Bridge Network** | "A magical Docker internal LAN." | A software Linux Ethernet bridge (like a virtual network switch) on the host kernel. Containers connect to it via virtual Ethernet pair (`veth`) interfaces. |
| **Port Publishing (`-p`)** | "Exposing a port." | Configures DNAT (Destination Network Address Translation) rules in the host's `iptables`/`nftables` so incoming host traffic on port X is forwarded across the bridge to the container's private IP on port Y. |
| **`EXPOSE` (Dockerfile)** | "Opens the port on the host." | Pure metadata documentation. It does **not** publish or bind any port to the host machine. |
| **Docker DNS** | "Resolves any container on the machine." | An embedded DNS server running at `127.0.0.11` inside container network namespaces on **user-defined networks**. It resolves container names to private IP addresses dynamically. (Does not operate on the default bridge!) |
| **Volume** | "A folder shared with the container." | A directory managed exclusively by the Docker daemon inside `/var/lib/docker/volumes/` on the host/VM, mounted into the container. Its lifecycle is completely decoupled from the container's lifecycle. |
| **Bind Mount** | "Same as a volume." | A direct mount of an arbitrary user-specified host file or directory path into the container filesystem. Sensitive to host permissions and paths. |
| **Docker Compose** | "A container runtime or cluster manager." | A client-side orchestrator tool that reads a declarative YAML specification, calculates a dependency directed acyclic graph (DAG), and invokes the Docker API to create networks, volumes, and containers in order. |
| **Health Check** | "Checks if the container is running." | A command executed periodically *inside* the container process namespace by the daemon. Returns `0` (healthy) or `1` (unhealthy) based on application readiness, not mere process existence. |
| **Registry** | "Where Dockerfiles are stored." | A content-addressable HTTP service implementing the OCI Distribution Specification that stores and serves image manifests and compressed layer blobs. |
