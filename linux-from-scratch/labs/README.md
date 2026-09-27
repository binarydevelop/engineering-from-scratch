# Hands-On Sandbox Laboratories

This directory provides isolated sandbox configurations and scripts for executing experiments that would otherwise be dangerous or impossible to perform directly on a host operating system.

---

## Laboratory Index

| Lab | Title | Target Subsystem | Isolation Mechanism |
| :---: | :--- | :--- | :--- |
| **01** | [Loopback Storage Lab](01-loopback-storage-lab/README.md) | Block devices, ext4, mounts | Sparse image file via `losetup` |
| **02** | [Network Namespace Lab](02-network-namespace-lab/README.md) | IP routes, veth pairs, firewalls | Linux network namespaces (`ip netns`) |
| **03** | [Systemd Service Lab](03-systemd-service-lab/README.md) | Service supervision, cgroups | Disposable user or system unit |
| **04** | [Cgroup Resource Limit Lab](04-cgroups-resource-limit-lab/README.md) | CPU quotas, Memory OOM | cgroups v2 (`/sys/fs/cgroup/`) |
| **05** | [Signal Handling Lab](05-signal-handling-lab/README.md) | Process lifecycle, traps | Python / Bash signal interceptors |

---

## Safety Protocol

Always verify that your lab actions are confined to the allocated sandbox before running commands that format disks or flush network routes. Run `bash scripts/cleanup.sh` to tear down any active lab resources.
