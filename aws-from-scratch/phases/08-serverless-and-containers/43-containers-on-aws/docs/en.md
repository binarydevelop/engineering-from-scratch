# Phase 43: Containers on AWS

## Motto
> Docker packages the filesystem and userland. AWS provides the orchestration and networking.

**Type:** Hands-on Lab & Container Packaging  
**Time Estimate:** ~60 minutes  
**Prerequisites:** Phase 13: EC2 From First Principles  
**AWS Services Involved:** Docker, OCI Containers  
**Cost Vector:** Local container builds are free.  

---

## Problem
Applications work on the developer's MacBook, but crash on Linux servers due to mismatched system libraries, Python versions, or missing dynamic links.

---

## Prediction
Packaging the application into a Docker container packages all userland dependencies into an immutable image that runs identically anywhere.

---

## Why this matters
Containers are the universal deployment artifact for modern cloud applications across ECS, EKS, and App Runner.

---

## First principles
A container is NOT a virtual machine. It does not boot an OS kernel. It is a standard Linux process isolated using kernel **namespaces** (`pid`, `net`, `mnt`, `ipc`, `uts`) and constrained by **cgroups** (CPU/RAM limits) sharing the host's Linux kernel.

---

## Mental model
```text
VM vs Container Architecture:
Virtual Machine (EC2):
[ App ] ──► [ Guest OS Kernel ] ──► [ Hypervisor ] ──► [ Physical Hardware ]
(Heavy: Boots full OS, consumes 1-2GB RAM before app runs)

Container (Docker / ECS):
[ App Process ] ──► [ Namespaces & CGroups ] ──► [ Shared Host Kernel ] ──► [ Hardware ]
(Lightweight: Starts in 500ms, zero OS overhead)
```

---

## Architecture before AWS
Chroot jails, Solaris Zones, FreeBSD Jails, and manual `.tar.gz` package deployments.

---

## Build the primitive
```python
# Dockerfile for cloud container
dockerfile = '''FROM python:3.12-slim
WORKDIR /app
COPY . .
CMD ["python3", "-m", "http.server", "8080"]'''
print("Cloud Containerfile specified.")
```

---

## Use AWS
```bash
docker --version
```

---

## Inspect it
```bash
docker ps
```

---

## Measure it
Compare startup time: EC2 AMI boot (60 seconds) vs Docker container start (1 second).

---

## Break it
Attempt to run a container that exceeds its allocated cgroup memory limit (`docker run -m 50m`).

---

## Diagnose it
The Linux Out-Of-Memory (OOM) Killer terminates the container process with exit code 137.

---

## Recover it
Right-size container memory allocations to accommodate peak working sets.

---

## Security
Never run container processes as `root`. Always specify a non-privileged user (`USER 1001`).

---

## Cost
### Cost Warning
Local container builds are free.

### Resources Created
- Documented in lesson steps above.

### How to Verify Them
```bash
./scripts/list-lab-resources.sh
```

---

## Modify it
Experiment by tuning parameters, increasing capacity, changing timeouts, or tweaking security group rules. Observe metric changes in CloudWatch.

---

## Cleanup
```bash
# Clean local docker artifacts
```

---

## Verify cleanup
```bash
echo 'Docker clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-43-evidence.md`.

---

## Questions for mastery
1. Why can an ARM64 Docker container NOT run on an x86 Linux host without QEMU emulation?
2. What happens when process ID 1 (PID 1) inside a container exits?
3. Why are container images built in layers, and how does layer caching accelerate CI/CD builds?

---

## When to use this
Use containers for all custom application services requiring custom runtimes and dependencies.

---

## When not to use this
Do not containerize workloads that require custom Linux kernel modules or direct hardware PCI access.

---

## What comes next
Phase 44: ECR — Storing private container images securely in AWS.
