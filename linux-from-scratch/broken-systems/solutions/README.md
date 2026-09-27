# Master Broken Systems Troubleshooting Solutions Guide

Comprehensive root-cause breakdowns, diagnostic command proofs, and permanent remediations for all 32 broken system scenarios.

---

## Web Server Fails to Bind: Address Already in Use (`scenario-01-web-server-port-conflict`)

- **Category**: Networking / Sockets
- **Severity**: High

### 1. Observable Symptom
The production API server fails to start with error: `[Errno 98] Address already in use: 0.0.0.0:8080`. No web server process appears in `ps aux | grep nginx`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Networking / Sockets`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ss -lntp '( sport = :8080 )' or lsof -i :8080
```

### 4. Root Cause Analysis
A forgotten background diagnostic script `lfs-rogue-listener` is holding socket `0.0.0.0:8080` open.

### 5. Targeted Permanent Fix
kill the PID owning port 8080 or stop its systemd service.

### 6. Verification
Run `bash broken-systems/scenario-01-web-server-port-conflict/verify.sh` to confirm resolution.

---

## Disk 100% Full But du Shows Empty Space (`scenario-02-disk-full-deleted-file`)

- **Category**: Storage / VFS
- **Severity**: Critical

### 1. Observable Symptom
Alert fires: `/tmp/lfs-lab/mnt` is 100% full (`df -h`). However, running `du -sh /tmp/lfs-lab/mnt` reports only 12KB of files! New file creation fails with `No space left on device`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Storage / VFS`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
lsof +L1 /tmp/lfs-lab/mnt
```

### 4. Root Cause Analysis
A running logger process holds an open file descriptor to a large log file that was deleted via `rm`. The directory entry is gone (invisible to `du`), but the kernel cannot free the data blocks until the process closes the file.

### 5. Targeted Permanent Fix
Terminate the process holding the unlinked file descriptor, or truncate it via `/proc/<pid>/fd/<fd>`.

### 6. Verification
Run `bash broken-systems/scenario-02-disk-full-deleted-file/verify.sh` to confirm resolution.

---

## No Space Left on Device Despite 50GB Free Space (`scenario-03-inode-exhaustion`)

- **Category**: Storage / Inodes
- **Severity**: High

### 1. Observable Symptom
Application crashes with `IOError: [Errno 28] No space left on device`. Running `df -h` shows 52GB of free disk space. Why is file creation failing?

### 2. Systematic Triage Workflow
1. Isolate the layer: `Storage / Inodes`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
df -i
```

### 4. Root Cause Analysis
An email queue or temporary cache script generated 500,000 zero-byte files, consuming 100% of the filesystem's available inodes.

### 5. Targeted Permanent Fix
Locate directory with excessive files (`find / -xdev -printf '%h\n' | sort | uniq -c | sort -nr | head -10`) and delete the orphaned files using `find -delete`.

### 6. Verification
Run `bash broken-systems/scenario-03-inode-exhaustion/verify.sh` to confirm resolution.

---

## Permission Denied Reading Existing File Owned by User (`scenario-04-directory-permission-traversal`)

- **Category**: Permissions / DAC
- **Severity**: Medium

### 1. Observable Symptom
User `deploy` tries to read `/data/apps/prod/settings.env`. The file permissions are `-rw-r--r-- deploy deploy`. Yet running `cat /data/apps/prod/settings.env` produces `cat: Permission denied`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Permissions / DAC`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
namei -l /data/apps/prod/settings.env
```

### 4. Root Cause Analysis
Parent directory `/data/apps` has permissions `drw-r--r--` (mode 0644). It lacks the execute (`+x`) traversal permission bit! Without `+x`, no user can traverse the directory to reach inodes inside.

### 5. Targeted Permanent Fix
chmod +x /data/apps

### 6. Verification
Run `bash broken-systems/scenario-04-directory-permission-traversal/verify.sh` to confirm resolution.

---

## Host Cannot Reach External APIs via Hostname (`scenario-05-dns-resolution-failure`)

- **Category**: Networking / DNS
- **Severity**: High

### 1. Observable Symptom
Curl command `curl https://api.stripe.com` fails immediately with `curl: (6) Could not resolve host: api.stripe.com`. However, `ping 8.8.8.8` works flawlessly!

### 2. Systematic Triage Workflow
1. Isolate the layer: `Networking / DNS`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
resolvectl status or cat /etc/resolv.conf
```

### 4. Root Cause Analysis
The configured nameserver in `/etc/resolv.conf` points to an unreachable IP address (`192.0.2.1`), or `systemd-resolved` is stopped.

### 5. Targeted Permanent Fix
Restore a valid DNS nameserver (e.g. `nameserver 1.1.1.1` or `nameserver 8.8.8.8`) or restart `systemd-resolved`.

### 6. Verification
Run `bash broken-systems/scenario-05-dns-resolution-failure/verify.sh` to confirm resolution.

---

## Service Fails Instantly with Exit Code 203/EXEC (`scenario-06-systemd-exec-format-error`)

- **Category**: Services / systemd
- **Severity**: High

### 1. Observable Symptom
A newly deployed service `lfs-worker.service` fails to start. `systemctl status` reports: `Active: failed (Result: exit-code)` with `Process: 1421 ExecStart=/opt/worker.sh (code=exited, status=203/EXEC)`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Services / systemd`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
journalctl -u lfs-worker.service -e and ls -l /opt/worker.sh
```

### 4. Root Cause Analysis
The script `/opt/worker.sh` either lacks executable permission (`chmod +x`), has a missing interpreter path in the shebang (e.g. `#!/bin/bash` with Windows carriage returns), or points to a non-existent binary.

### 5. Targeted Permanent Fix
Fix shebang to `#!/usr/bin/env bash` and run `chmod +x /opt/worker.sh`.

### 6. Verification
Run `bash broken-systems/scenario-06-systemd-exec-format-error/verify.sh` to confirm resolution.

---

## Database Process Mysteriously Disappears without Trace (`scenario-07-oom-killer-termination`)

- **Category**: Performance / Memory
- **Severity**: Critical

### 1. Observable Symptom
A Redis or PostgreSQL server process unexpectedly vanished. No crash dump was generated, and no log was written to the application log. The service simply stopped.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Performance / Memory`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
dmesg -T | grep -i oom or journalctl -k | grep -i 'killed process'
```

### 4. Root Cause Analysis
The Linux kernel Out-Of-Memory (OOM) killer invoked `out_of_memory()`, selected the process based on high `oom_score`, and sent an uncatchable `SIGKILL`.

### 5. Targeted Permanent Fix
Add memory or configure swap, tune `vm.overcommit_memory`, or adjust `/proc/<pid>/oom_score_adj`.

### 6. Verification
Run `bash broken-systems/scenario-07-oom-killer-termination/verify.sh` to confirm resolution.

---

## Application Crashes with 'Too many open files' (`scenario-08-file-descriptor-exhaustion`)

- **Category**: Process Limits / VFS
- **Severity**: High

### 1. Observable Symptom
A high-throughput API gateway starts rejecting incoming client connections with `socket: too many open files` (error code EMFILE).

### 2. Systematic Triage Workflow
1. Isolate the layer: `Process Limits / VFS`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ulimit -n and ls -l /proc/<pid>/fd | wc -l
```

### 4. Root Cause Analysis
The process exceeded its soft file descriptor limit (`RLIMIT_NOFILE`), typically defaulting to 1024 for unprivileged users.

### 5. Targeted Permanent Fix
Increase limit via `prlimit --nofile=65535 --pid=<pid>` or configure `/etc/security/limits.conf` and systemd `LimitNOFILE=65535`.

### 6. Verification
Run `bash broken-systems/scenario-08-file-descriptor-exhaustion/verify.sh` to confirm resolution.

---

## Process Table Leaking Hundreds of Zombie Entries (`scenario-09-zombie-process-accumulation`)

- **Category**: Processes / Lifecycle
- **Severity**: Medium

### 1. Observable Symptom
Running `ps aux` shows hundreds of entries marked with `[app] <defunct>` in state `Z`. The system PID count is steadily climbing toward `/proc/sys/kernel/pid_max`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Processes / Lifecycle`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ps -eo pid,ppid,stat,comm | awk '$3 ~ /Z/'
```

### 4. Root Cause Analysis
The parent application forks child worker processes to perform asynchronous tasks, but fails to call `wait()` or `waitpid()` when children exit.

### 5. Targeted Permanent Fix
Fix the parent program code to handle `SIGCHLD` and reap child processes, or restart the parent process to let PID 1 reap the orphans.

### 6. Verification
Run `bash broken-systems/scenario-09-zombie-process-accumulation/verify.sh` to confirm resolution.

---

## Standard Linux Command Produces Unexpected Behavior (`scenario-10-path-hijack-or-order`)

- **Category**: Shell / PATH
- **Severity**: High

### 1. Observable Symptom
An operator types `uptime`, but instead of system load, the terminal prints `ERROR: License key required`. Running `which uptime` returns `/usr/local/bin/uptime`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Shell / PATH`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
type -a uptime and echo $PATH
```

### 4. Root Cause Analysis
A rogue or misconfigured script placed a script named `uptime` in `/usr/local/bin`, which appears before `/usr/bin` in the shell's `$PATH` resolution order.

### 5. Targeted Permanent Fix
Remove the shadowing file from `/usr/local/bin/uptime` or correct `$PATH` order in `/etc/environment`.

### 6. Verification
Run `bash broken-systems/scenario-10-path-hijack-or-order/verify.sh` to confirm resolution.

---

## Internal Microservice Connecting to Wrong Host (`scenario-11-corrupted-hosts-file`)

- **Category**: Networking / Name Resolution
- **Severity**: High

### 1. Observable Symptom
The billing backend cannot connect to `db.internal`. `ping db.internal` attempts to reach `10.99.99.99` instead of the actual database IP `10.0.1.50`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Networking / Name Resolution`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
getent hosts db.internal and cat /etc/hosts
```

### 4. Root Cause Analysis
A stale testing override entry in `/etc/hosts` is overriding DNS responses due to the default precedence order in `/etc/nsswitch.conf` (`files dns`).

### 5. Targeted Permanent Fix
Remove or update the stale entry in `/etc/hosts`.

### 6. Verification
Run `bash broken-systems/scenario-11-corrupted-hosts-file/verify.sh` to confirm resolution.

---

## Filesystem Suddenly Re-mounted as Read-Only (`scenario-12-readonly-filesystem-recovery`)

- **Category**: Storage / Recovery
- **Severity**: Critical

### 1. Observable Symptom
All disk write operations fail across `/var`: `Read-only file system`. `dmesg` shows I/O barrier errors.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Storage / Recovery`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
mount | grep ' / ' or dmesg -T | grep -i 'remounting filesystem read-only'
```

### 4. Root Cause Analysis
Filesystem driver encountered block layer inconsistencies or disk errors, triggering the ext4 `errors=remount-ro` safety fallback.

### 5. Targeted Permanent Fix
Unmount cleanly, execute filesystem check `fsck -fy /dev/<device>`, and remount `rw`.

### 6. Verification
Run `bash broken-systems/scenario-12-readonly-filesystem-recovery/verify.sh` to confirm resolution.

---

## Server Reaches Local Subnet but Cannot Reach Internet (`scenario-13-missing-default-gateway`)

- **Category**: Networking / Routing
- **Severity**: High

### 1. Observable Symptom
The server can ping other hosts on the `192.168.1.0/24` subnet, but pinging `8.8.8.8` returns `connect: Network is unreachable`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Networking / Routing`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ip route show
```

### 4. Root Cause Analysis
The kernel routing table has no `default via <gateway_ip>` route.

### 5. Targeted Permanent Fix
Add default gateway: `sudo ip route add default via 192.168.1.1 dev eth0`.

### 6. Verification
Run `bash broken-systems/scenario-13-missing-default-gateway/verify.sh` to confirm resolution.

---

## Service Works Manually But Fails Under Systemd (`scenario-14-systemd-missing-env-var`)

- **Category**: Services / Environment
- **Severity**: Medium

### 1. Observable Symptom
Running `/usr/local/bin/api_server` directly from the bash terminal succeeds. Starting it via `systemctl start api_server` fails immediately with `KeyError: 'DATABASE_URL'`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Services / Environment`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
systemctl show api_server -p Environment and journalctl -u api_server
```

### 4. Root Cause Analysis
Systemd does not inherit interactive shell environment variables from `~/.bashrc`. The service unit file lacks the `Environment=` or `EnvironmentFile=` directive.

### 5. Targeted Permanent Fix
Add `Environment="DATABASE_URL=postgres://..."` to the `[Service]` section of the unit file.

### 6. Verification
Run `bash broken-systems/scenario-14-systemd-missing-env-var/verify.sh` to confirm resolution.

---

## Binary Fails with 'error while loading shared libraries' (`scenario-15-missing-shared-library`)

- **Category**: Packages / Libraries
- **Severity**: Medium

### 1. Observable Symptom
Running a custom compiled binary `/opt/bin/fastcalc` returns: `error while loading shared libraries: libmkl.so: cannot open shared object file: No such file or directory`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Packages / Libraries`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ldd /opt/bin/fastcalc
```

### 4. Root Cause Analysis
The required shared library is installed under `/opt/intel/lib`, but that path is not in the dynamic linker cache `/etc/ld.so.cache` or `$LD_LIBRARY_PATH`.

### 5. Targeted Permanent Fix
Add `/opt/intel/lib` to `/etc/ld.so.conf.d/custom.conf` and run `sudo ldconfig`.

### 6. Verification
Run `bash broken-systems/scenario-15-missing-shared-library/verify.sh` to confirm resolution.

---

## Package Manager Blocked by Stale Lock File (`scenario-16-dpkg-lock-held`)

- **Category**: Package Management
- **Severity**: Medium

### 1. Observable Symptom
Running `apt-get install htop` fails with: `E: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 3241 (unattended-upgr)`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Package Management`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
lsof /var/lib/dpkg/lock-frontend or fuser /var/lib/dpkg/lock-frontend
```

### 4. Root Cause Analysis
An unattended upgrades background task or hung apt process is holding the frontend advisory lock.

### 5. Targeted Permanent Fix
Wait for unattended-upgrades to finish, or if hung, safely terminate the holding process and run `sudo dpkg --configure -a`.

### 6. Verification
Run `bash broken-systems/scenario-16-dpkg-lock-held/verify.sh` to confirm resolution.

---

## Regular Users Unable to Change Passwords (`scenario-17-suid-binary-permission-lost`)

- **Category**: Security / SUID
- **Severity**: Medium

### 1. Observable Symptom
A non-root user runs `passwd` to change their account password. The command returns: `passwd: Authentication token manipulation error`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Security / SUID`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ls -l /usr/bin/passwd
```

### 4. Root Cause Analysis
The SUID bit (`4755`) was stripped from `/usr/bin/passwd` during a reckless `chmod -R 755` command, leaving it as standard `0755`.

### 5. Targeted Permanent Fix
Restore SUID bit: `sudo chmod u+s /usr/bin/passwd` (mode 4755).

### 6. Verification
Run `bash broken-systems/scenario-17-suid-binary-permission-lost/verify.sh` to confirm resolution.

---

## Cron Job Fails Silently Due to Minimal PATH (`scenario-18-cron-minimal-path-failure`)

- **Category**: Automation / Cron
- **Severity**: Medium

### 1. Observable Symptom
A maintenance script runs perfectly when executed in bash, but fails every midnight under cron with `command not found: aws`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Automation / Cron`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
Inspect cron job environment: cron sets PATH to `/usr/bin:/bin` by default
```

### 4. Root Cause Analysis
The `aws` CLI is installed under `/usr/local/bin` or `~/.local/bin`, which is not included in cron's default minimal `$PATH`.

### 5. Targeted Permanent Fix
Explicitly define `PATH=/usr/local/bin:/usr/bin:/bin` at the top of the crontab, or use absolute paths inside the script.

### 6. Verification
Run `bash broken-systems/scenario-18-cron-minimal-path-failure/verify.sh` to confirm resolution.

---

## Application Fails to Write Database Files (`scenario-19-wrong-user-data-ownership`)

- **Category**: Permissions / Ownership
- **Severity**: High

### 1. Observable Symptom
Database engine runs as dedicated user `postgres`. On startup, it reports: `FATAL: could not create lock file 'postmaster.pid': Permission denied`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Permissions / Ownership`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ls -ld /var/lib/postgresql/data
```

### 4. Root Cause Analysis
The data directory is owned by `root:root` with permissions `0700` because an administrator manually copied files using `sudo cp`.

### 5. Targeted Permanent Fix
Restore correct ownership: `sudo chown -R postgres:postgres /var/lib/postgresql/data`.

### 6. Verification
Run `bash broken-systems/scenario-19-wrong-user-data-ownership/verify.sh` to confirm resolution.

---

## SSH Connection Refused After Port Change (`scenario-20-ssh-port-and-firewall`)

- **Category**: Networking / SSH
- **Severity**: Critical

### 1. Observable Symptom
An administrator edited `/etc/ssh/sshd_config` to change the port to `2222` and restarted `ssh`. Connecting via `ssh user@host` hangs and times out.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Networking / SSH`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ss -lntp | grep sshd and sudo iptables -L -n
```

### 4. Root Cause Analysis
The firewall (ufw / iptables) was configured to permit incoming port 22, but traffic to the new port 2222 is blocked by the default DROP policy.

### 5. Targeted Permanent Fix
Allow port 2222 in the firewall: `sudo ufw allow 2222/tcp` or add iptables rule.

### 6. Verification
Run `bash broken-systems/scenario-20-ssh-port-and-firewall/verify.sh` to confirm resolution.

---

## Single CPU Core Pinned at 100% Load (`scenario-21-cpu-spin-runaway-loop`)

- **Category**: Performance / CPU
- **Severity**: Medium

### 1. Observable Symptom
System load average spikes to 1.00 on a single-core VM. Top shows process `worker.py` consuming 99.8% CPU in user mode (`us`).

### 2. Systematic Triage Workflow
1. Isolate the layer: `Performance / CPU`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
top -b -n 1 | head -15 and strace -p <pid>
```

### 4. Root Cause Analysis
An infinite `while True:` loop without a `sleep()` or I/O yield inside an unthrottled background worker.

### 5. Targeted Permanent Fix
Fix application loop logic with proper poll intervals or terminate runaway process.

### 6. Verification
Run `bash broken-systems/scenario-21-cpu-spin-runaway-loop/verify.sh` to confirm resolution.

---

## System Sluggish with High %wa in Top (`scenario-22-io-wait-write-saturation`)

- **Category**: Performance / I/O
- **Severity**: High

### 1. Observable Symptom
The terminal feels unresponsive. Running `top` reveals CPU utilization is mostly `0.5% us, 1.2% sy, 89.4% wa`. Load average is climbing rapidly.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Performance / I/O`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
vmstat 1 5 and iostat -xz 1
```

### 4. Root Cause Analysis
A backup process is performing unbuffered synchronous writes (`dd` or `sync`), saturating disk I/O queues and blocking other processes in state `D`.

### 5. Targeted Permanent Fix
Throttle I/O with `ionice -c 3` (idle priority) or throttle throughput.

### 6. Verification
Run `bash broken-systems/scenario-22-io-wait-write-saturation/verify.sh` to confirm resolution.

---

## Local Sockets Fail with 'Network is unreachable' (`scenario-23-loopback-interface-down`)

- **Category**: Networking / Interfaces
- **Severity**: High

### 1. Observable Symptom
Connecting to `localhost` or `127.0.0.1` fails instantly: `connect: Network is unreachable`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Networking / Interfaces`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ip link show lo
```

### 4. Root Cause Analysis
The loopback network interface `lo` was administratively brought down (`state DOWN`).

### 5. Targeted Permanent Fix
Bring loopback interface back up: `sudo ip link set lo up`.

### 6. Verification
Run `bash broken-systems/scenario-23-loopback-interface-down/verify.sh` to confirm resolution.

---

## Single Log File Saturates 100GB Root Partition (`scenario-24-unrotated-gigantic-log`)

- **Category**: Logging / Storage
- **Severity**: Critical

### 1. Observable Symptom
The root partition reached 100% capacity. `du -ahx /var/log | sort -rh | head -5` reveals `/var/log/app/trace.log` is 92 Gigabytes!

### 2. Systematic Triage Workflow
1. Isolate the layer: `Logging / Storage`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
cat /etc/logrotate.d/app
```

### 4. Root Cause Analysis
The logrotate configuration for `app` had a syntax error, or the `logrotate.timer` systemd timer was inactive.

### 5. Targeted Permanent Fix
Truncate log safely (`> /var/log/app/trace.log`), repair `/etc/logrotate.d/app`, and run `sudo logrotate -f /etc/logrotate.conf`.

### 6. Verification
Run `bash broken-systems/scenario-24-unrotated-gigantic-log/verify.sh` to confirm resolution.

---

## Process Cannot be Killed Even with kill -9 (`scenario-25-uninterruptible-sleep-process`)

- **Category**: Kernel / Process States
- **Severity**: High

### 1. Observable Symptom
An operator attempts `kill -9 4812`, but the process continues to appear in `ps aux`. State code is `D`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Kernel / Process States`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
cat /proc/4812/wchan and cat /proc/4812/stack
```

### 4. Root Cause Analysis
Process is in uninterruptible sleep state (`D`), blocked inside a kernel system call waiting for hardware disk response or a dead NFS network mount.

### 5. Targeted Permanent Fix
You cannot kill a process in state D from user space. You must recover the underlying storage or network mount, or reboot.

### 6. Verification
Run `bash broken-systems/scenario-25-uninterruptible-sleep-process/verify.sh` to confirm resolution.

---

## Intermittent Packet Loss and Flapping SSH Connections (`scenario-26-subnet-ip-conflict`)

- **Category**: Networking / ARP
- **Severity**: High

### 1. Observable Symptom
SSH connection disconnects every 30 seconds. Ping packet loss is ~50%. Running `arping` shows conflicting responses.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Networking / ARP`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ip neigh show and sudo tcpdump -i eth0 arp
```

### 4. Root Cause Analysis
Another host on the local Ethernet segment configured the same static IP address, causing ARP cache poisoning and flapping MAC entries in switches.

### 5. Targeted Permanent Fix
Change static IP to an unassigned IP in subnet, or coordinate with network administrator.

### 6. Verification
Run `bash broken-systems/scenario-26-subnet-ip-conflict/verify.sh` to confirm resolution.

---

## All HTTPS Connections Fail with SSL Certificate Errors (`scenario-27-clock-drift-ssl-failure`)

- **Category**: Time / TLS
- **Severity**: High

### 1. Observable Symptom
`curl https://github.com` fails with: `SSL certificate problem: certificate has expired or is not yet valid`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Time / TLS`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
timedatectl status and date -u
```

### 4. Root Cause Analysis
The virtual machine system clock drifted by several months (e.g. following VM pause/resume), placing the current timestamp outside valid certificate validity windows.

### 5. Targeted Permanent Fix
Synchronize system clock: `sudo timedatectl set-ntp true` or `sudo systemctl restart systemd-timesyncd`.

### 6. Verification
Run `bash broken-systems/scenario-27-clock-drift-ssl-failure/verify.sh` to confirm resolution.

---

## Find Command Hangs in Infinite Symlink Loop (`scenario-28-circular-symlink-recursion`)

- **Category**: Filesystem / Symlinks
- **Severity**: Medium

### 1. Observable Symptom
Application tree walker throws: `OSError: [Errno 40] Too many levels of symbolic links`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Filesystem / Symlinks`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ls -l on suspicious symlink path
```

### 4. Root Cause Analysis
A symlink points to a directory that contains a symlink pointing back to the parent, creating an infinite cycle.

### 5. Targeted Permanent Fix
Remove the recursive symlink and rebuild link with proper relative or absolute target.

### 6. Verification
Run `bash broken-systems/scenario-28-circular-symlink-recursion/verify.sh` to confirm resolution.

---

## Uploaded Files Result in HTTP 403 Forbidden (`scenario-29-umask-web-server-403`)

- **Category**: Permissions / Web Server
- **Severity**: Medium

### 1. Observable Symptom
Users upload images to `/var/www/uploads`. Nginx returns `403 Forbidden` when serving them. The directory permissions are `0755`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Permissions / Web Server`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ls -l /var/www/uploads/image.png and umask
```

### 4. Root Cause Analysis
The backend daemon saving files runs with umask `0077`, creating files with permissions `0600` (`-rw-------`). Web server user `www-data` has no read access.

### 5. Targeted Permanent Fix
Set umask to `0022` in backend service or configure default POSIX ACLs (`setfacl -d -m u:www-data:r /var/www/uploads`).

### 6. Verification
Run `bash broken-systems/scenario-29-umask-web-server-403/verify.sh` to confirm resolution.

---

## Web Server Running and Listening But Inaccessible (`scenario-30-firewall-drop-rule-blocking`)

- **Category**: Networking / Firewall
- **Severity**: High

### 1. Observable Symptom
`systemctl status nginx` is active. `ss -lntp` shows port 80 and 443 listening on `0.0.0.0`. Yet clients cannot connect.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Networking / Firewall`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
sudo nft list ruleset or sudo iptables -S
```

### 4. Root Cause Analysis
A firewall filter rule is dropping TCP SYN packets targeting port 80/443 in the `INPUT` chain.

### 5. Targeted Permanent Fix
Insert rule allowing traffic: `sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT` or update nftables.

### 6. Verification
Run `bash broken-systems/scenario-30-firewall-drop-rule-blocking/verify.sh` to confirm resolution.

---

## Users Able to Delete Other Users' Temporary Files (`scenario-31-missing-tmp-sticky-bit`)

- **Category**: Security / Permissions
- **Severity**: High

### 1. Observable Symptom
User `alice` creates `/tmp/alice_task.pid`. User `bob` is able to run `rm /tmp/alice_task.pid` and delete it without permission errors!

### 2. Systematic Triage Workflow
1. Isolate the layer: `Security / Permissions`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
ls -ld /tmp
```

### 4. Root Cause Analysis
The sticky bit on `/tmp` was removed, changing permissions from `1777` (`drwxrwxrwt`) to `0777` (`drwxrwxrwx`).

### 5. Targeted Permanent Fix
Restore sticky bit: `sudo chmod +t /tmp` (mode 1777).

### 6. Verification
Run `bash broken-systems/scenario-31-missing-tmp-sticky-bit/verify.sh` to confirm resolution.

---

## Silent Disk Saturation in /var/lib/systemd/coredump (`scenario-32-core-dump-silent-disk-fill`)

- **Category**: Storage / Systemd
- **Severity**: High

### 1. Observable Symptom
Disk space is dwindling by 2GB every hour. No large log files are visible in `/var/log`.

### 2. Systematic Triage Workflow
1. Isolate the layer: `Storage / Systemd`.
2. Run read-only diagnostic inspection before altering configuration.
3. Formulate the root-cause hypothesis.

### 3. Decisive Diagnostic Command
```bash
coredumpctl list and du -sh /var/lib/systemd/coredump
```

### 4. Root Cause Analysis
A crashing C/C++ microservice is segfaulting repeatedly in a restart loop, generating massive core dumps on disk.

### 5. Targeted Permanent Fix
Disable core dump accumulation or fix segfaulting binary; configure `Storage=none` in `/etc/systemd/coredump.conf`.

### 6. Verification
Run `bash broken-systems/scenario-32-core-dump-silent-disk-fill/verify.sh` to confirm resolution.

---
