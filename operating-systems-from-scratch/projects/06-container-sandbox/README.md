# Capstone 6: Tiny Container-Like Sandbox

> **Motto:** Containers do not exist as physical or kernel objects. A container is simply a standard Linux host process wrapped in Namespaces (for isolation), Cgroups (for resource accounting), and Chroot/Pivot_root (for filesystem views).

---

## 1. Architectural Primitives

This capstone pulls back the curtain on container engines (Docker, Podman, runc, containerd) by assembling the five Linux kernel primitives:

1. **PID Namespace (`CLONE_NEWPID`):** The sandboxed process becomes PID 1 inside its private process tree.
2. **UTS Namespace (`CLONE_NEWUTS`):** Gives the process an isolated hostname and domain name.
3. **Mount Namespace (`CLONE_NEWNS`):** Allows private mount points invisible to the host.
4. **Network Namespace (`CLONE_NEWNET`):** Provides a clean, isolated network stack with its own loopback and routing table.
5. **Control Groups (`cgroups v2`):** Meters and caps memory consumption (`memory.max`) and CPU time slices (`cpu.max`).

---

## 2. Compiling and Running

```bash
make
./container-launcher /bin/echo "Hello from container"
```

On native Linux or WSL2 with administrative privileges:
```bash
sudo ./launch-sandbox.sh
```
