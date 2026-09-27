# Platform Setup & Target Environment Strategy

Linux interacts directly with system hardware, kernel modules, virtual filesystems, and device nodes. Selecting the right learning environment is critical: you need a real Linux kernel with root access, but you must be able to break things without risking your primary operating system or personal data.

---

## Environment Comparison Matrix

| Environment | Kernel | systemd | Mounts / Loop | Raw Sockets / Net | Best Used For | Trade-offs & Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Linux VM (Multipass / UTM / VirtualBox)** | Dedicated Linux | Full (Native) | Full | Full | **Recommended default** for all 136 phases | Requires 2-4GB RAM host allocation; fast snapshot & revert. |
| **Disposable Cloud VM (Hetzner, DO, AWS)** | Dedicated Linux | Full (Native) | Full | Full | Excellent alternative | Small recurring cost ($4-$6/mo); requires internet & SSH key. |
| **Native Linux Machine** | Host Linux | Full (Native) | Full | Full | Advanced learners on secondary hardware | Extreme care required during failure injection; no instant revert. |
| **WSL2 (Windows Subsystem for Linux)** | Microsoft Custom | Supported (v0.67+) | Limited | Mostly Full | Shell, text tools, scripts, basic networking | Non-standard storage backend (VHDX); systemd requires config. |
| **Docker Container** | Shared Host Kernel | **None / Emulated** | **Restricted** | **Bridged / Virtual** | Fast shell syntax only (Phases 00-20) | **NOT suitable** for systemd, mounts, kernel interfaces, boot. |

---

## 1. Recommended Setup: Canonical Multipass (macOS, Windows, Linux)

Multipass provides instant, lightweight Ubuntu virtual machines using native hypervisors (Hyper-V, Hypervisor.framework, or KVM).

### Installation & Launch
```bash
# Install Multipass (macOS via Homebrew)
brew install --cask multipass

# Launch an Ubuntu 24.04 LTS instance with 2 CPUs, 4GB RAM, and 20GB disk
multipass launch 24.04 --name lfs-lab --cpus 2 --memory 4G --disk 20G

# Open an interactive shell inside the lab VM
multipass shell lfs-lab

# Inside the VM: install core diagnostic tools
sudo apt update && sudo apt install -y \
    coreutils iproute2 procps util-linux psmisc \
    lsof strace curl netcat-openbsd tcpdump \
    dnsutils jq build-essential git
```

### Snapshotting & Instant Recovery
```bash
# Take a clean snapshot before breaking things
multipass stop lfs-lab
multipass snapshot lfs-lab --name baseline

# Restore if an experiment destroys system state
multipass restore lfs-lab.snapshot.baseline
multipass start lfs-lab
```

---

## 2. UTM / VirtualBox Setup (GUI-based VM)

If you prefer a full graphical virtual machine manager:
1. Download [Ubuntu 24.04 Server ISO](https://ubuntu.com/download/server).
2. Create a VM with 2 vCPUs, 4GB RAM, 25GB virtual disk.
3. Use bridged networking or NAT with port forwarding for SSH (e.g. host `2222` -> guest `22`).
4. Take a snapshot named `clean-install` before beginning Lesson 00.

---

## 3. Windows Subsystem for Linux (WSL2)

If working on Windows 11:
```powershell
# Install Ubuntu 24.04 on WSL2
wsl --install -d Ubuntu-24.04
```
Ensure systemd is enabled in `/etc/wsl.conf`:
```ini
[boot]
systemd=true
```
Restart WSL from PowerShell: `wsl --shutdown`.

> **Note on WSL2 Limitations**: Storage block devices (`lsblk`), loopback mounting, and raw network packet captures behave differently under the Microsoft WSL2 kernel. For Phases 63-71 (Storage) and 43 (Boot), a dedicated VM is strongly advised.

---

## 4. Why Docker Containers Are NOT Sufficient

Many learners mistakenly believe running `docker run -it ubuntu:latest bash` provides a Linux computer. **It does not.**

```text
               DOCKER CONTAINER TRAP
   ┌────────────────────────────────────────────────────────┐
   │  NO real PID 1 (no systemd, systemctl fails instantly) │
   │  NO isolated kernel (shares your host/VM kernel)       │
   │  NO real block devices (cannot mount loop devices)     │
   │  NO /sys or /dev modifications (read-only kernel nodes)│
   │  NO native routing table or firewall control           │
   └────────────────────────────────────────────────────────┘
```

Treat containers as isolated processes running on Linux, not as Linux machines.
