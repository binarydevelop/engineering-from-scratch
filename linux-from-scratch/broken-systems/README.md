# Broken Systems: 32 Realistic Linux Troubleshooting Scenarios

This directory contains **32 hands-on, realistic troubleshooting scenarios** spanning every layer of Linux system administration.

---

## Scenario Catalog

| ID | Title | Category | Severity |
| :---: | :--- | :--- | :---: |
| **01** | [Web Server Port Conflict](scenario-01-web-server-port-conflict/symptom.md) | Networking / Sockets | High |
| **02** | [Disk Full with Deleted Open Files](scenario-02-disk-full-deleted-file/symptom.md) | Storage / VFS | Critical |
| **03** | [Inode Exhaustion](scenario-03-inode-exhaustion/symptom.md) | Storage / Inodes | High |
| **04** | [Directory Traversal Permission Trap](scenario-04-directory-permission-traversal/symptom.md) | Permissions / DAC | Medium |
| **05** | [DNS Resolution Failure](scenario-05-dns-resolution-failure/symptom.md) | Networking / DNS | High |
| **06** | [Systemd Exit Status 203/EXEC](scenario-06-systemd-exec-format-error/symptom.md) | Services / systemd | High |
| **07** | [Out-of-Memory Killer Termination](scenario-07-oom-killer-termination/symptom.md) | Performance / Memory | Critical |
| **08** | [File Descriptor Exhaustion (EMFILE)](scenario-08-file-descriptor-exhaustion/symptom.md) | Resource Limits / VFS | High |
| **09** | [Zombie Process Accumulation](scenario-09-zombie-process-accumulation/symptom.md) | Processes / Lifecycle | Medium |
| **10** | [PATH Hijacking & Command Order](scenario-10-path-hijack-or-order/symptom.md) | Shell / Environment | High |
| **11** | [Stale /etc/hosts Override](scenario-11-corrupted-hosts-file/symptom.md) | Networking / NSS | High |
| **12** | [Read-Only Filesystem Remount](scenario-12-readonly-filesystem-recovery/symptom.md) | Storage / VFS | Critical |
| **13** | [Missing Default Gateway](scenario-13-missing-default-gateway/symptom.md) | Networking / Routing | High |
| **14** | [Systemd Missing Environment Variables](scenario-14-systemd-missing-env-var/symptom.md) | Services / Config | Medium |
| **15** | [Missing Shared Object Library](scenario-15-missing-shared-library/symptom.md) | Packages / Dynamic Linker | Medium |
| **16** | [DPKG Lock File Deadlock](scenario-16-dpkg-lock-held/symptom.md) | Package Management | Medium |
| **17** | [SUID Permission Stripped](scenario-17-suid-binary-permission-lost/symptom.md) | Security / Credentials | Medium |
| **18** | [Cron Minimal PATH Failure](scenario-18-cron-minimal-path-failure/symptom.md) | Automation / Cron | Medium |
| **19** | [Wrong Data Directory Ownership](scenario-19-wrong-user-data-ownership/symptom.md) | Permissions / DAC | High |
| **20** | [SSH Port Mismatch with Firewall](scenario-20-ssh-port-and-firewall/symptom.md) | Networking / SSH | Critical |
| **21** | [Runaway CPU Spin Loop](scenario-21-cpu-spin-runaway-loop/symptom.md) | Performance / CPU | Medium |
| **22** | [I/O Wait Saturation](scenario-22-io-wait-write-saturation/symptom.md) | Performance / Block I/O | High |
| **23** | [Loopback Interface Down](scenario-23-loopback-interface-down/symptom.md) | Networking / Interfaces | High |
| **24** | [Unrotated Gigantic Log File](scenario-24-unrotated-gigantic-log/symptom.md) | Storage / Logging | Critical |
| **25** | [Uninterruptible Sleep State (D)](scenario-25-uninterruptible-sleep-process/symptom.md) | Kernel / Task State | High |
| **26** | [Subnet IP Address Conflict](scenario-26-subnet-ip-conflict/symptom.md) | Networking / ARP | High |
| **27** | [System Clock Drift Breaking TLS](scenario-27-clock-drift-ssl-failure/symptom.md) | Time / Cryptography | High |
| **28** | [Circular Symbolic Link Recursion](scenario-28-circular-symlink-recursion/symptom.md) | Filesystem / Inodes | Medium |
| **29** | [Umask Breaking Web Server Access](scenario-29-umask-web-server-403/symptom.md) | Permissions / Web Server | Medium |
| **30** | [Firewall DROP Rule Blocking Traffic](scenario-30-firewall-drop-rule-blocking/symptom.md) | Networking / Netfilter | High |
| **31** | [Missing /tmp Sticky Bit](scenario-31-missing-tmp-sticky-bit/symptom.md) | Security / Permissions | High |
| **32** | [Core Dump Partition Saturation](scenario-32-core-dump-silent-disk-fill/symptom.md) | Storage / Core Dumps | High |

---

## Lab Protocol

1. Change directory to the scenario: `cd broken-systems/scenario-XX-...`
2. Run the safe setup script: `bash setup.sh`
3. Read `symptom.md` (Do NOT open the solutions guide yet!).
4. Use the diagnostic commands to inspect the system and isolate the root cause.
5. Apply the minimal permanent fix.
6. Verify your remediation: `bash verify.sh`
7. Check the official breakdown in [broken-systems/solutions/README.md](solutions/README.md).
