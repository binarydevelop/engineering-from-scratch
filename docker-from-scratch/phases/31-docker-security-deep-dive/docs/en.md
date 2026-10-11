# Phase 31: Container Security Hardening, Capabilities, and Seccomp

## 1. Why This Matters for MAANG & Senior/Staff Roles
Containers do NOT contain by default. A container is simply an isolated Linux process sharing the host kernel. Misconfigured containers with root privileges or excessive capabilities allow trivial container breakout and host takeover. Senior engineers must understand security boundaries, seccomp filters, capability drops, and image provenance.

---

## 2. Core Concepts & Architecture Deep-Dive
### Defense-in-Depth Container Security Architecture
1. **Rootless Containers**: Docker/Podman runs the daemon and container processes inside a user namespace without root privileges on the host. Even if escaped, attacker has zero host root privileges.
2. **Linux Capabilities (`cap_drop` / `cap_add`)**: Linux breaks root power into distinct privileges (`CAP_NET_ADMIN`, `CAP_SYS_ADMIN`, `CAP_CHOWN`). Best practice: Drop ALL capabilities and selectively grant only what is needed:
   `docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE ...`
3. **Seccomp (Secure Computing Mode)**: Restricts which kernel system calls a containerized process can invoke. Default Docker seccomp blocks ~44 dangerous syscalls (`reboot`, `kexec_load`, `ptrace`).
4. **AppArmor / SELinux**: Mandatory Access Control (MAC) policies restricting file paths, socket binding, and raw device access regardless of user privileges.
5. **Read-Only Root Filesystem**: `docker run --read-only --tmpfs /tmp` prevents attackers from downloading backdoors or altering binaries during remote code execution (RCE).

---

## 3. High-Value Interview Angle & Failure Modes
### Interview Questions & Attack Vectors
- **"Why is `--privileged` flag strictly forbidden in production?"**: `--privileged` disables all seccomp filters, AppArmor profiles, and adds all capabilities, giving the container direct access to all host devices (`/dev`). A single mount command (`mount /dev/sda1 /mnt`) grants complete host root takeover.
- **"How does `--security-opt=no-new-privileges:true` prevent privilege escalation?"**: It disables `setuid` and `setgid` bit execution, ensuring that an unprivileged user inside the container cannot execute binaries like `sudo` to gain root within the container.

---

## 4. Hands-On Practice & Implementation Drills
### Hardened Dockerfile & Runtime Flags Drill
```dockerfile
# Multi-stage build with distroless non-root image
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o server .

# Distroless contains only binary + glibc/ca-certificates; no shell, no package manager
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /
COPY --from=builder /app/server /server
USER nonroot:nonroot
ENTRYPOINT ["/server"]
```
```bash
# Secure runtime execution command
docker run -d \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  --security-opt=seccomp=/path/to/profile.json \
  --pids-limit=100 \
  --memory=512m \
  --cpus=1.0 \
  my-hardened-app:1.0.0
```

---

## 5. Key Takeaways & Cheat Sheet
- Containers share the host kernel; root in a container without user namespaces is dangerous.
- Drop all Linux capabilities by default (`--cap-drop=ALL`).
- Enforce read-only filesystems and non-root users (`USER nonroot`).
- Scan container images using Trivy/Snyk in CI before deployment.
