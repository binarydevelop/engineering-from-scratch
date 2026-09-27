# Lesson 25.1: Docker Security Foundations

## Motto
"Root inside a container is root on the host kernel; least privilege requires non-root users, dropped capabilities, and read-only filesystems."

## Problem
Many developers leave Dockerfiles with default settings:
The container runs as `root` (UID 0), mounts the root filesystem with write permissions, and retains default Linux kernel capabilities.
If an attacker discovers a vulnerability in your web application (such as an arbitrary file write or remote code execution), they operate with full root privileges.
Even worse, developers sometimes mount `/var/run/docker.sock` into containers to "trigger builds" without realizing that doing so provides instant, full root control over the host server.
How do we harden container runtimes using defense-in-depth?

## Prediction
1. If an application runs as `root` inside a container, what user ID (UID) executes on the host Linux kernel?
2. What happens if an attacker attempts to write to `/etc/hosts` in a container launched with `--read-only`?
3. Why is mounting `/var/run/docker.sock` considered equivalent to giving someone passwordless `sudo` on your server?

## Why this matters
Container escape vulnerabilities (like Dirty COW, runc CVE-2019-5736, and capability abuse) turn application vulnerabilities into host-level cluster compromises. Hardening your containers by dropping capabilities and running as non-root stops 90% of exploit chains cold.

## First principles
1. **The UID 0 Reality**:
   Unless Linux User Namespaces (`userns-remap`) are enabled, UID 0 inside a container is **literally UID 0 on the host kernel**. It is not a simulated root; it is the real root user restricted only by cgroups, namespaces, and dropped capabilities!
2. **Linux Capabilities (`cap-drop` / `cap-add`)**:
   In traditional Unix, root had absolute power. Modern Linux breaks root's privileges into distinct **capabilities**:
   - `CAP_NET_ADMIN`: Configure interfaces, routes, iptables.
   - `CAP_NET_BIND_SERVICE`: Bind to privileged ports (< 1024).
   - `CAP_SYS_ADMIN`: Mount filesystems, configure namespaces (almost equivalent to full root).
   - Best practice: Pass `--cap-drop ALL` and only re-add the exact capabilities your app requires.
3. **The Docker Socket Hazard (`/var/run/docker.sock`)**:
   The Docker socket is the REST API entrypoint to the Docker daemon, which runs as `root`.
   If a container has access to `docker.sock`, any process inside that container can issue an HTTP POST request to spawn a new container mounting the host's root filesystem:
   ```bash
   # Attacker inside container with docker.sock:
   docker run -v /:/host-root --privileged alpine chroot /host-root
   # Attacker is now root on the host machine!
   ```

## Mental model

```text
CONTAINER DEFENSE-IN-DEPTH:
┌────────────────────────────────────────────────────────┐
│  Application Process                                   │
│  ├── USER 10001:10001 (Non-root unprivileged)          │
├────────────────────────────────────────────────────────┤
│  Filesystem Layer:                                     │
│  ├── --read-only (Kernel blocks writes to rootfs)      │
│  └── --tmpfs /tmp (Temporary memory mount for caches)  │
├────────────────────────────────────────────────────────┤
│  Kernel Boundary:                                      │
│  ├── --cap-drop ALL (Strips all 40+ Linux capabilities)│
│  ├── --security-opt=no-new-privileges:true             │
│  └── Seccomp Profile: default syscall filter           │
└────────────────────────────────────────────────────────┘
```

## Build it
Review `Dockerfile.hardened` and `app.py` in `code/`.
Notice:
- `RUN groupadd -g 10001 ...` creates a dedicated system user.
- `USER 10001:10001` drops root privileges before executing `CMD`.

## Run it
Execute the experiment runner:

```bash
./phases/25-docker-security-foundations/01-rootless-capabilities-and-socket-risk/experiments/run_experiment.sh
```

## Inspect it
1. Observe Experiment 1: Running as default root allows writing to protected system paths.
2. Observe Experiment 2: The hardened container runs as UID 10001 and fails with `PermissionError`.
3. In Experiment 3, `--read-only` prevents even root from tampering with system binaries.
4. In Experiment 4, `--cap-drop ALL` prevents modifying network interfaces.

## Break it
Launch a container with `--read-only` and see what happens when an application tries to write temporary files to `/tmp`:
```bash
docker run --rm --read-only alpine:latest touch /tmp/session.tmp
```
Fails with `Read-only file system`!
To fix this while keeping the rootfs read-only, attach an in-memory tmpfs mount for temporary scratch files:
```bash
docker run --rm --read-only --tmpfs /tmp alpine:latest touch /tmp/session.tmp
```
The session file is successfully created in RAM, while the rest of the root filesystem remains locked and immutable.

## Debug it
When non-root containers fail to start with `Permission denied`:
1. Check directory permissions of your `WORKDIR`:
   Ensure `chown -R 10001:10001 /app` is executed during the image build *before* switching to `USER 10001`.
2. Check if the app tries to bind to port 80 (ports < 1024 require root or `CAP_NET_BIND_SERVICE`). Change the app port to 8080!

## Modify it
Add `--security-opt=no-new-privileges:true` to a `docker run` command to prevent processes from elevating privileges via `setuid` binaries like `sudo` or `su`.

## Evidence
Record your results in [evidence-template.md](../outputs/evidence-template.md):
- UID output of default vs hardened container.
- Exit code and error from `--read-only`.
- Error message observed when `--cap-drop ALL` blocked network manipulation.

## Questions for mastery
1. Why is running as non-root inside a container still safer even if the container is compromised?
2. What is the difference between `--privileged` and `--cap-add ALL`?
3. How can tools like Kaniko or Buildah build Docker images without mounting the Docker socket?

## What comes next
Now that our containers are secure, we examine performance: **How do we shrink multi-gigabyte images into lean, fast-downloading artifacts?** Proceed to **Phase 26: Image Optimization**.
