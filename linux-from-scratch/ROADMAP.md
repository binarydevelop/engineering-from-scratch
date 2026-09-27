# Curriculum Roadmap: linux-from-scratch

> **Understand it. Use it. Inspect it. Break it. Debug it. Automate it. Secure it. Operate it.**

A comprehensive, first-principles progression from raw terminal streams to production-grade Linux system administration and site reliability engineering.

---

## The 15 Thematic Curriculum Blocks

```text
1. Linux Orientation & Shell Foundations      (Phases 00 - 13)
2. Text Stream Processing & Pipelines         (Phases 14 - 20)
3. Users, Groups & Discretionary Access       (Phases 21 - 27)
4. Processes, Lifecycle & Virtual FS          (Phases 28 - 34)
5. Package Management & Shared Libraries      (Phases 35 - 38)
6. Services, systemd & Boot Sequence          (Phases 39 - 46)
7. Networking Stack, Sockets & Firewalls      (Phases 47 - 62)
8. Storage Stack, Filesystems & Inodes        (Phases 63 - 71)
9. Logs, Time Synchronization & Backups       (Phases 72 - 76)
10. Defensive Shell Scripting & Automation    (Phases 77 - 86)
11. Resource Limits & Performance Profiling   (Phases 87 - 95)
12. Security Hardening & Kernel Interfaces    (Phases 96 - 107)
13. Failure Injection & Debugging Labs        (Phases 108 - 120)
14. Practical Production Projects             (Phases 121 - 129)
15. Modern Architecture (Docker, K8s, Systems)(Phases 130 - 135)
```

---

## Detailed Syllabus (All 136 Phases)

| Phase | Title | Category | Primary Focus & Abstraction | Core Tools |
| :---: | :--- | :--- | :--- | :--- |
| **00** | [Linux Orientation](phases/phase-00-linux-orientation/docs/en.md) | Fundamentals | Kernel vs user-space split, distribution compositi... | `uname -a, cat /etc/os-release,` |
| **01** | [Terminal, Shell, and Commands](phases/phase-01-terminal-shell-and-commands/docs/en.md) | Fundamentals | Terminal Emulator (PTY GUI) -> Shell (Bash parser)... | `echo, printf, date, whoami, ec` |
| **02** | [Command Structure & Tokenization](phases/phase-02-command-structure/docs/en.md) | Shell | Command Line -> Lexer (Whitespace Splitting) -> Ex... | `ls -lah, command --help, man l` |
| **03** | [Filesystem Mental Model](phases/phase-03-filesystem-mental-model/docs/en.md) | Filesystem | Root '/' -> Subdirectories: /etc (config), /var (v... | `ls -ld /, findmnt, df -hT /` |
| **04** | [Filesystem Navigation](phases/phase-04-navigation/docs/en.md) | Shell | Current Working Directory (CWD) stored in process ... | `pwd, ls -F, cd, cd -, cd ~` |
| **05** | [Files and Directories](phases/phase-05-files-and-directories/docs/en.md) | Filesystem | Directory entry (dentry) maps string filename -> I... | `touch, mkdir -p, cp -a, mv, rm` |
| **06** | [Wildcards and Globbing](phases/phase-06-wildcards-and-globbing/docs/en.md) | Shell | User types 'rm *.txt' -> Shell expands to 'rm a.tx... | `printf '%s\n' *, ls *.txt, ls ` |
| **07** | [Quoting Mechanics](phases/phase-07-quoting/docs/en.md) | Shell | Shell Parser: Whitespace splitting occurs on unquo... | `echo '$HOME', echo "$HOME", pr` |
| **08** | [Environment Variables](phases/phase-08-environment-variables/docs/en.md) | Shell & Processes | Process Address Space -> Environment Pointer (**en... | `env, export, printenv, echo $P` |
| **09** | [PATH and Command Resolution](phases/phase-09-path-and-command-resolution/docs/en.md) | Shell | $PATH -> Left-to-right directory traversal -> Inod... | `which, type -a, command -v, ha` |
| **10** | [Standard Streams (stdin, stdout, stderr)](phases/phase-10-stdin-stdout-stderr/docs/en.md) | Streams | Process -> File Descriptor Table [0: stdin, 1: std... | `ls -l /proc/$$/fd, echo 'hello` |
| **11** | [Redirection Mechanics](phases/phase-11-redirection/docs/en.md) | Streams | Shell dup2() system call adjusts file descriptor t... | `>, >>, <, 2>, 2>&1, &>, << 'EO` |
| **12** | [Pipes & Unix Composition](phases/phase-12-pipes/docs/en.md) | Streams | Process A (stdout) ===[ Kernel Circular Buffer (64... | `ps aux | grep python, cat /etc` |
| **13** | [Tee and Advanced Pipelines](phases/phase-13-tee-and-pipelines/docs/en.md) | Streams | Stdin -> tee process -> [stdout -> display] AND [f... | `tee, tee -a, command | tee out` |
| **14** | [Text Inspection (cat, less, head, tail, wc)](phases/phase-14-text-inspection/docs/en.md) | Text Tools | Direct terminal buffer rendering vs TTY paging buf... | `cat, less, head -n 20, tail -n` |
| **15** | [Pattern Searching with grep](phases/phase-15-grep/docs/en.md) | Text Tools | Finite Automata Regex Engine matching lines from s... | `grep, grep -i, grep -v, grep -` |
| **16** | [Stream Editing with sed](phases/phase-16-sed/docs/en.md) | Text Tools | Pattern Space (active line buffer) -> sed script i... | `sed 's/old/new/g', sed -i.bak ` |
| **17** | [Field-Oriented Processing with awk](phases/phase-17-awk/docs/en.md) | Text Tools | Input Record -> Field Splitting -> BEGIN block -> ... | `awk '{print $1}', awk -F: '$3 ` |
| **18** | [Data Processing Pipelines (sort, uniq, cut, tr)](phases/phase-18-sort-uniq-cut-tr/docs/en.md) | Text Tools | Stream -> Character Translation (tr) -> Field Slic... | `cut -d: -f1, sort -n -r -k2, u` |
| **19** | [Filesystem Searching with find](phases/phase-19-find/docs/en.md) | Text Tools & FS | Directory Tree Inode Traversal -> Stat Struct Insp... | `find /path -name '*.log', find` |
| **20** | [Converting Streams to Arguments with xargs](phases/phase-20-xargs/docs/en.md) | Text Tools & Shell | Stdin byte stream -> Tokenizer -> Argv batching ->... | `find -type f | xargs rm, xargs` |
| **21** | [User Identity & Credentials](phases/phase-21-users/docs/en.md) | Security | Kernel task_struct credentials (uid, gid, euid, eg... | `whoami, id, id -u, getent pass` |
| **22** | [Group Memberships & Collaboration](phases/phase-22-groups/docs/en.md) | Security | Kernel credential array: groups_alloc() stores sup... | `groups, id, getent group, grou` |
| **23** | [File Ownership & Inodes](phases/phase-23-file-ownership/docs/en.md) | Permissions | ext4 inode table entry -> i_uid (16/32 bit integer... | `chown user:group file, chown u` |
| **24** | [Discretionary Access Control (DAC)](phases/phase-24-permissions/docs/en.md) | Permissions | 16-bit inode mode: [File Type (4 bits)] [Special (... | `chmod u+x, chmod g-w, chmod o=` |
| **25** | [Directory Permissions & Traversal](phases/phase-25-directory-permissions/docs/en.md) | Permissions | Directory as an inode table index: 'r' reads the n... | `chmod 0755 dir, chmod 0644 dir` |
| **26** | [Octal Modes and Umask Calculation](phases/phase-26-chmod-and-umask/docs/en.md) | Permissions | Mode Calculation: New File = 0666 & ~umask; New Di... | `umask, umask 0022, umask 0077,` |
| **27** | [Privilege Escalation with sudo](phases/phase-27-sudo/docs/en.md) | Security | Normal Process (UID 1000) -> sudo binary (SUID roo... | `sudo command, sudo -u user, su` |
| **28** | [Processes, PIDs, and Process Trees](phases/phase-28-processes/docs/en.md) | Processes | Kernel task_struct linked list -> Process tree -> ... | `ps, ps aux, ps -ef, pstree -p,` |
| **29** | [Job Control (fg, bg, jobs, disown)](phases/phase-29-foreground-and-background-jobs/docs/en.md) | Processes | Shell Job Table -> Terminal Process Group Control ... | `command &, jobs -l, fg %1, bg ` |
| **30** | [Linux Signals (SIGINT, SIGTERM, SIGKILL, SIGHUP)](phases/phase-30-signals/docs/en.md) | Processes | Kernel Signal Delivery -> Process Pending Signal B... | `kill -l, kill -15 <pid>, kill ` |
| **31** | [Process Inspection & Metrics](phases/phase-31-process-inspection/docs/en.md) | Processes | Kernel task_struct CPU time accounting -> Jiffies ... | `top, ps aux --sort=-%cpu, pids` |
| **32** | [The /proc Virtual Filesystem](phases/phase-32-proc/docs/en.md) | Kernel Interfaces | Kernel Memory Data Structures <---> VFS /proc Inod... | `cat /proc/cpuinfo, cat /proc/m` |
| **33** | [Open Files and lsof](phases/phase-33-open-files-and-lsof/docs/en.md) | Processes & VFS | Process task_struct -> files_struct -> fd_array[] ... | `lsof -p <pid>, lsof -i :8080, ` |
| **34** | [Process Priorities & Niceness](phases/phase-34-process-priorities/docs/en.md) | Processes & Scheduler | Completely Fair Scheduler (CFS) -> Virtual Runtime... | `nice -n 10 command, renice -n ` |
| **35** | [Package Management Mental Model](phases/phase-35-package-management-mental-model/docs/en.md) | Packages | Remote Repository -> Packages/Release Index -> Pac... | `apt-cache search, apt show, dp` |
| **36** | [Installing & Removing Packages](phases/phase-36-installing-and-removing-packages/docs/en.md) | Packages | Metadata Sync -> Dependency Resolution -> Download... | `apt update, apt install -y, ap` |
| **37** | [Package Inspection & Reverse Lookups](phases/phase-37-package-inspection/docs/en.md) | Packages | Local Package Database (/var/lib/dpkg/info/) -> Fi... | `dpkg -S /path/to/file, dpkg -L` |
| **38** | [Shared Dynamic Libraries & ldd](phases/phase-38-shared-libraries/docs/en.md) | Packages & OS | ELF Binary -> .interp (dynamic linker /lib64/ld-li... | `ldd /bin/ls, ldconfig -p, objd` |
| **39** | [Background Daemons & Service Principles](phases/phase-39-services/docs/en.md) | Services | Traditional Double-fork Daemonization vs Modern Sy... | `ps -ef | grep daemon, nohup, s` |
| **40** | [systemd Architecture & systemctl](phases/phase-40-systemd/docs/en.md) | Services | systemd PID 1 -> cgroup hierarchy -> Unit Dependen... | `systemctl status, systemctl st` |
| **41** | [Authoring Service Units](phases/phase-41-service-units/docs/en.md) | Services | Unit file definition -> systemctl daemon-reload ->... | `systemctl daemon-reload, syste` |
| **42** | [The systemd Journal & journalctl](phases/phase-42-journalctl/docs/en.md) | Logging & Services | Process stdout -> socket /run/systemd/journal/stdo... | `journalctl, journalctl -u <ser` |
| **43** | [Linux Boot Sequence](phases/phase-43-boot-process-overview/docs/en.md) | Boot & Kernel | Firmware (UEFI) -> Bootloader (GRUB) -> Kernel + I... | `systemd-analyze, systemd-analy` |
| **44** | [systemd Targets & Dependencies](phases/phase-44-systemd-dependencies/docs/en.md) | Services | Dependency Graph -> Topological Sort -> Parallel S... | `systemctl list-dependencies, s` |
| **45** | [systemd Timers](phases/phase-45-timers/docs/en.md) | Services & Automation | Timer Unit (OnCalendar / OnBootSec) -> Kernel Time... | `systemctl list-timers, systemc` |
| **46** | [Cron Jobs and Scheduled Tasks](phases/phase-46-cron/docs/en.md) | Services & Automation | Crontab Syntax: [Minute Hour Day Month Weekday Com... | `crontab -e, crontab -l, cronta` |
| **47** | [Linux Networking Mental Model](phases/phase-47-networking-mental-model/docs/en.md) | Networking | Network Packet -> NIC -> Ring Buffer -> SoftIRQ ->... | `ip link, ip addr, ip route, ss` |
| **48** | [Network Interfaces & ip link](phases/phase-48-network-interfaces/docs/en.md) | Networking | Kernel struct net_device -> Device driver -> Hardw... | `ip link show, ip link set <dev` |
| **49** | [IP Routing & ip route](phases/phase-49-routes/docs/en.md) | Networking | Destination IP -> Routing Table Lookup -> Select I... | `ip route show, ip route get <i` |
| **50** | [Connectivity Testing with ping](phases/phase-50-connectivity-testing/docs/en.md) | Networking | User -> Raw Socket -> ICMP Packet (Type 8) -> Netw... | `ping -c 4 <ip>, ping -i 0.2 <i` |
| **51** | [DNS Resolution Architecture](phases/phase-51-dns/docs/en.md) | Networking & DNS | getaddrinfo() -> glibc resolver -> nsswitch.conf -... | `resolvectl status, dig +trace ` |
| **52** | [Listening Ports & Socket Inspection with ss](phases/phase-52-ports-and-sockets/docs/en.md) | Networking & Sockets | Application -> bind() -> listen() -> Kernel Socket... | `ss -lntp, ss -lunp, ss -antp, ` |
| **53** | [HTTP Diagnostics with curl](phases/phase-53-curl/docs/en.md) | Networking & Web | curl CLI -> DNS Lookup -> TCP Handshake -> TLS Neg... | `curl -Iv <url>, curl -s -w '%{` |
| **54** | [Raw TCP/UDP Experiments with netcat](phases/phase-54-netcat/docs/en.md) | Networking & Sockets | Stdin -> nc -> TCP Socket -> Network -> TCP Socket... | `nc -l -p 9000, nc <ip> 9000, n` |
| **55** | [Packet Capture & tcpdump](phases/phase-55-tcpdump/docs/en.md) | Networking | NIC -> Kernel Packet Filter (BPF) -> Ring Buffer -... | `tcpdump -i any -nn, tcpdump -i` |
| **56** | [The Complete Network Troubleshooting Tree](phases/phase-56-network-troubleshooting-workflow/docs/en.md) | Networking & Triage | OSI Layer 1 -> Layer 2 (ARP/MAC) -> Layer 3 (IP/Ro... | `ip link; ip addr; ip route; ip` |
| **57** | [Hosts File & Resolution Order](phases/phase-57-hosts-file-and-name-resolution/docs/en.md) | Networking & DNS | Application -> gethostbyname() -> /etc/nsswitch.co... | `cat /etc/hosts, getent hosts <` |
| **58** | [Firewall Fundamentals & Netfilter](phases/phase-58-firewall-concepts/docs/en.md) | Security & Networking | Network Packet -> Ingress Hook -> Netfilter Conntr... | `sudo iptables -L -n -v, sudo u` |
| **59** | [SSH Architecture & Remote Shells](phases/phase-59-ssh/docs/en.md) | Security & SSH | ssh client -> TLS-like asymmetric exchange -> Sess... | `ssh user@host, ssh -v user@hos` |
| **60** | [SSH Key Cryptography & authorized_keys](phases/phase-60-ssh-keys/docs/en.md) | Security & SSH | Private Key (~/.ssh/id_ed25519, mode 0600) <---> P... | `ssh-keygen -t ed25519, ssh-cop` |
| **61** | [SSH Client Configuration (~/.ssh/config)](phases/phase-61-ssh-configuration/docs/en.md) | Security & SSH | ssh alias -> ~/.ssh/config lookup -> Hostname, Por... | `ssh <alias>, cat ~/.ssh/config` |
| **62** | [File Transfer: SCP, SFTP, and rsync](phases/phase-62-scp-sftp-rsync/docs/en.md) | Networking & Automation | Local rsync process <== SSH Tunnel ==> Remote rsyn... | `rsync -avz --progress src/ des` |
| **63** | [Linux Storage Mental Model](phases/phase-63-storage-mental-model/docs/en.md) | Storage | NVMe SSD (/dev/nvme0n1) -> Partition (/dev/nvme0n1... | `lsblk, blkid, findmnt, df -hT` |
| **64** | [Block Devices & lsblk](phases/phase-64-block-devices/docs/en.md) | Storage | Block Device Inode -> Major Number (Driver) / Mino... | `lsblk, blkid, fdisk -l` |
| **65** | [Filesystems & Superblocks](phases/phase-65-filesystems/docs/en.md) | Storage & FS | Block Group -> Superblock -> Group Descriptors -> ... | `mkfs.ext4, tune2fs -l <dev>, f` |
| **66** | [Mounting Filesystems & /etc/fstab](phases/phase-66-mounting/docs/en.md) | Storage | Directory Dentry -> VFS Mount Structure -> Target ... | `mount, umount, mount -o loop, ` |
| **67** | [The df vs du Discrepancy](phases/phase-67-df-vs-du/docs/en.md) | Storage & Triage | df: Superblock -> Total allocated blocks. du: VFS ... | `df -h, du -sh /path/*, lsof +L` |
| **68** | [Inodes and Inode Exhaustion](phases/phase-68-inodes/docs/en.md) | Storage | Inode Table -> 256-byte Inode Structs -> Inode Bit... | `df -i, stat -c '%i' <file>, ls` |
| **69** | [Hard Links vs Symbolic Links](phases/phase-69-links/docs/en.md) | Storage & Inodes | Hard Link: Dentry A + Dentry B -> Inode 42 (i_nlin... | `ln target hardlink, ln -s targ` |
| **70** | [File Descriptors and Deleted Files](phases/phase-70-file-descriptors-and-deleted-files/docs/en.md) | Storage & Processes | VFS Inode -> i_count (open file handles) + i_nlink... | `lsof +L1, ls -l /proc/<pid>/fd` |
| **71** | [Disk Usage Troubleshooting Workflow](phases/phase-71-disk-usage-troubleshooting/docs/en.md) | Storage & Triage | Superblock Block Capacity -> Inode Capacity -> Dir... | `df -hT; df -i; du -ahx / | sor` |
| **72** | [Linux Logging Architecture & /var/log](phases/phase-72-logs/docs/en.md) | Logging | Application / Kernel -> syslog() syscall / /dev/lo... | `tail -f /var/log/syslog, grep ` |
| **73** | [Log Rotation with logrotate](phases/phase-73-log-rotation/docs/en.md) | Logging & Maintenance | log.log -> log.log.1 -> log.log.2.gz -> prune -> p... | `logrotate -d /etc/logrotate.co` |
| **74** | [System Time, Timezones & Chrony](phases/phase-74-time/docs/en.md) | Time & OS | NTP Server -> UDP Port 123 -> NTP Client -> Adjtim... | `date, timedatectl, timedatectl` |
| **75** | [Archives & Compression (tar, gzip, xz)](phases/phase-75-archives/docs/en.md) | Storage & Maintenance | Files + Inode Metadata -> tar (Archive Container) ... | `tar -czvf archive.tar.gz /path` |
| **76** | [Backups from First Principles](phases/phase-76-backups-from-first-principles/docs/en.md) | Maintenance & Reliability | Source Inodes -> Tar Compression -> SHA-256 Checks... | `tar, sha256sum, sha256sum -c` |
| **77** | [Defensive Shell Scripting Basics](phases/phase-77-shell-scripting-basics/docs/en.md) | Scripting | Shebang (#!) -> Kernel execve() reads interpreter ... | `chmod +x script.sh, ./script.s` |
| **78** | [Script Arguments & Positional Parameters](phases/phase-78-script-arguments/docs/en.md) | Scripting | Invocation Command -> Shell Argv Array -> Bash Pos... | `while [ $# -gt 0 ]; do case ..` |
| **79** | [Conditions & Tests ([ vs [[ ]])](phases/phase-79-conditions/docs/en.md) | Scripting | Bash Built-in [[ ]] Expression Evaluator vs POSIX ... | `[[ -f $FILE ]], [[ -d $DIR ]],` |
| **80** | [Safe Iteration with Loops](phases/phase-80-loops/docs/en.md) | Scripting | Loop Construct -> Array / Glob Expansion -> Safe I... | `for item in "${array[@]}"; do,` |
| **81** | [Functions & Scope in Bash](phases/phase-81-functions/docs/en.md) | Scripting | Function Call Stack -> Local Variable Symbol Table... | `my_func() { local var="$1"; ..` |
| **82** | [Defensive Error Handling (set -euo pipefail)](phases/phase-82-error-handling/docs/en.md) | Scripting | Bash Execution Flags -> Signal & Error Traps -> Re... | `set -euo pipefail, trap 'clean` |
| **83** | [Static Analysis with ShellCheck](phases/phase-83-shellcheck/docs/en.md) | Scripting & Quality | Script AST Parser -> Rule Engine (SC2086, SC2002, ... | `shellcheck script.sh, shellche` |
| **84** | [Server Health Audit Tool](phases/phase-84-practical-automation-project/docs/en.md) | Automation | System State Queries -> Metric Extraction -> Forma... | `bash scripts-examples/server-h` |
| **85** | [Shell Startup Files & Environments](phases/phase-85-environment-configuration/docs/en.md) | Shell & OS | Login Shell (SSH / console) -> /etc/profile -> ~/.... | `source ~/.bashrc, bash --login` |
| **86** | [Aliases, Shell Functions & Disguised Commands](phases/phase-86-aliases-and-functions/docs/en.md) | Shell | Interactive Lexer -> Alias Substitution Table -> C... | `alias, alias ll='ls -la', unal` |
| **87** | [Process Resource Limits with ulimit](phases/phase-87-process-limits/docs/en.md) | Performance & Limits | Kernel task_struct -> signal_struct -> rlim[] arra... | `ulimit -a, ulimit -n, ulimit -` |
| **88** | [CPU Debugging & Profiling](phases/phase-88-cpu-debugging/docs/en.md) | Performance & CPU | Kernel Jiffies Accounting -> /proc/stat -> Delta c... | `top, pidstat -u 1, mpstat -P A` |
| **89** | [Memory Debugging & Allocation](phases/phase-89-memory-debugging/docs/en.md) | Performance & Memory | Virtual Memory (Page Tables) <---> Physical RAM Pa... | `free -h, vmstat 1, pmap -x <pi` |
| **90** | [Page Cache, Buffers, and Reclaim](phases/phase-90-linux-memory-and-cache/docs/en.md) | Performance & Memory | Disk Blocks <===> Linux Page Cache (In-Memory Page... | `free -h, cat /proc/meminfo | g` |
| **91** | [Load Average Demystified](phases/phase-91-load-average/docs/en.md) | Performance | Load Average = Active CPU Consumers (State R) + Pr... | `uptime, cat /proc/loadavg, top` |
| **92** | [I/O Wait & Storage Bottlenecks](phases/phase-92-io-debugging/docs/en.md) | Performance & I/O | Process Syscall (write) -> Page Cache -> Block Lay... | `vmstat 1, iostat -xz 1, pidsta` |
| **93** | [System Call Tracing with strace](phases/phase-93-strace/docs/en.md) | Debugging & Syscalls | Process -> ptrace() breakpoint -> Kernel -> strace... | `strace command, strace -p <pid` |
| **94** | [strace Debugging Labs](phases/phase-94-strace-debugging-labs/docs/en.md) | Debugging | User Code -> glibc -> syscall (openat/connect/poll... | `strace -f -e trace=openat,conn` |
| **95** | [Performance Methodology (The USE Method)](phases/phase-95-performance-methodology/docs/en.md) | Performance | Resource -> Utilization (% busy) -> Saturation (Qu... | `uptime; free -m; vmstat 1; ios` |
| **96** | [Linux Security Foundations & Threat Modeling](phases/phase-96-security-foundations/docs/en.md) | Security | Threat Model -> Attack Surface Reduction -> DAC / ... | `ss -lntp, find / -perm -4000, ` |
| **97** | [Creating Secure Service Users](phases/phase-97-secure-service-user/docs/en.md) | Security | useradd -r -> System UID -> Shell /usr/sbin/nologi... | `sudo useradd -r -s /usr/sbin/n` |
| **98** | [SSH Hardening & Bastions](phases/phase-98-ssh-hardening-concepts/docs/en.md) | Security & SSH | Client Authentication Request -> sshd policy valid... | `sudo sshd -t, sudo systemctl r` |
| **99** | [File Permission Security Audits](phases/phase-99-file-permission-security-labs/docs/en.md) | Security & Auditing | Inode Mode Bits -> Security Scan -> Remediation (c... | `find / -perm -0002 -type f, fi` |
| **100** | [Linux Capabilities](phases/phase-100-linux-capabilities-intro/docs/en.md) | Security & Kernel | Kernel task_struct -> cap_effective, cap_permitted... | `getcap <binary>, sudo setcap c` |
| **101** | [Linux Namespaces Overview](phases/phase-101-namespaces-overview/docs/en.md) | Kernel & Containers | Kernel nsproxy structure -> PID NS, NET NS, MNT NS... | `lsns, unshare, ip netns` |
| **102** | [Control Groups (cgroups v2)](phases/phase-102-cgroups-overview/docs/en.md) | Kernel & Resources | /sys/fs/cgroup/ -> Unified Cgroup Hierarchy -> cpu... | `systemd-cgls, cat /sys/fs/cgro` |
| **103** | [The Container View of Linux](phases/phase-103-container-view-of-linux/docs/en.md) | Containers & OS | Host Kernel -> Host PID 14210 -> [PID NS: sees PID... | `docker ps, ps aux | grep <app>` |
| **104** | [Kernel Information & dmesg](phases/phase-104-kernel-information/docs/en.md) | Kernel | Kernel printk() -> Ring Buffer (RAM) -> /dev/kmsg ... | `dmesg -T, dmesg -l err,dmesg -` |
| **105** | [The /sys Virtual Filesystem (sysfs)](phases/phase-105-sys/docs/en.md) | Kernel Interfaces | Kernel Kobjects / Device Hierarchy <---> VFS sysfs... | `ls /sys/class/net, cat /sys/bl` |
| **106** | [Device Nodes in /dev](phases/phase-106-devices/docs/en.md) | Devices & Kernel | devtmpfs populated by udev daemon based on kernel ... | `ls -l /dev, head -c 16 /dev/ur` |
| **107** | [TTYs and Pseudo-Terminals (PTYs)](phases/phase-107-ttys-and-pseudo-terminals/docs/en.md) | Terminals & Shell | Terminal Emulator (PTY Master) <== Kernel PTY Driv... | `tty, ls -l /dev/pts/, w, who` |
| **108** | [Signals and Service Shutdown Lab](phases/phase-108-signals-and-service-shutdown/docs/en.md) | Debugging & Lifecycle | Supervisor sends SIGTERM -> Wait Timeout (TimeoutS... | `systemctl stop <service>, kill` |
| **109** | [Shared Library Failures Lab](phases/phase-109-shared-libraries-and-runtime-failures/docs/en.md) | Debugging & Libraries | Dynamic Linker -> Checks DT_RPATH -> LD_LIBRARY_PA... | `ldd <binary>, objdump -p <bina` |
| **110** | [PATH and Executable Debugging Lab](phases/phase-110-path-and-executable-debugging/docs/en.md) | Debugging & Shell | Shell Resolution -> PATH Traversal -> File Stat ->... | `type -a, which, file <binary>,` |
| **111** | [DNS Failure Lab](phases/phase-111-dns-failure-lab/docs/en.md) | Debugging & DNS | Resolver Configuration -> Port 53 Timeout -> Servf... | `resolvectl status, dig, ping, ` |
| **112** | [Port Conflict Lab](phases/phase-112-port-conflict-lab/docs/en.md) | Debugging & Sockets | Kernel Socket Bind Check -> INADDR_ANY vs Specific... | `ss -lntp '( sport = :8080 )', ` |
| **113** | [Permission Denied Lab](phases/phase-113-permission-denied-lab/docs/en.md) | Debugging & Permissions | Path Traversal -> Step-by-step Directory Inode Mod... | `namei -l /path/to/file, ls -ld` |
| **114** | [Disk Full Lab](phases/phase-114-disk-full-lab/docs/en.md) | Debugging & Storage | Filesystem Block Allocation -> Superblock Free Blo... | `df -hT, du -sh /*, find / -siz` |
| **115** | [Inode Exhaustion Lab](phases/phase-115-inode-exhaustion-lab/docs/en.md) | Debugging & Inodes | Inode Bitmap -> All Inode slots allocated -> Super... | `df -i, find / -type f | wc -l` |
| **116** | [Too Many Open Files Lab](phases/phase-116-too-many-open-files-lab/docs/en.md) | Debugging & Limits | Process File Descriptor Table -> Hits RLIMIT_NOFIL... | `ulimit -n, ls -l /proc/<pid>/f` |
| **117** | [Zombie Process Lab](phases/phase-117-zombie-process-lab/docs/en.md) | Debugging & Processes | Process exit() -> State Z (Zombie) -> Waits for Pa... | `ps -eo pid,ppid,stat,comm | gr` |
| **118** | [Failed Service Debugging Lab](phases/phase-118-failed-service-lab/docs/en.md) | Debugging & Services | systemd ExecStart -> Fork -> Setuid/Setgid -> Exec... | `systemctl status <service>, jo` |
| **119** | [Broken System Labs Catalog](phases/phase-119-broken-system-labs/docs/en.md) | Troubleshooting | Symptom -> Isolate Layer -> Read-only Inspection -... | `ls broken-systems/` |
| **120** | [The Repeatable Troubleshooting Methodology](phases/phase-120-troubleshooting-methodology/docs/en.md) | Troubleshooting | Define Symptom -> What Changed? -> Isolate Layer -... | `cat docs/troubleshooting.md` |
| **121** | [Project: Build a Linux Service](phases/phase-121-project-build-a-linux-service/docs/en.md) | Projects | systemd PID 1 -> cgroup -> unprivileged process fo... | `systemctl start lfs-api, syste` |
| **122** | [Project: Reverse Proxy Server](phases/phase-122-project-reverse-proxy-server/docs/en.md) | Projects | Client -> TCP Port 8000 -> Nginx epoll event loop ... | `nginx -t, systemctl reload ngi` |
| **123** | [Project: Multi-User Collaboration Server](phases/phase-123-project-multi-user-server/docs/en.md) | Projects | SGID on Directory (chmod 2770) -> Kernel forces ne... | `chmod 2770 /data/projects/core` |
| **124** | [Project: Backup Automation Suite](phases/phase-124-project-backup-automation/docs/en.md) | Projects | Source Inodes -> Tarball Compression -> Checksum V... | `bash scripts-examples/backup-r` |
| **125** | [Project: Server Health Monitor CLI](phases/phase-125-project-server-health-monitor/docs/en.md) | Projects | Kernel /proc & /sys virtual files -> String parsin... | `bash scripts-examples/server-h` |
| **126** | [Project: High-Performance Log Analysis Pipeline](phases/phase-126-project-log-analysis/docs/en.md) | Projects | Log Stream -> Token Slicing (cut/awk) -> Memory So... | `awk, sort, uniq, cut` |
| **127** | [Project: Troubleshoot a Broken Web Server](phases/phase-127-project-troubleshoot-broken-web-server/docs/en.md) | Projects | Systematic Layer Isolation: Network Port -> Filesy... | `Full diagnostic toolchain` |
| **128** | [Project: Harden a Small Server](phases/phase-128-project-harden-small-server/docs/en.md) | Projects | Defense in Depth: Packet Filtering (Netfilter) -> ... | `sshd -t, ufw status verbose, i` |
| **129** | [Project: Build a Linux Application Host (Capstone)](phases/phase-129-project-build-a-linux-application-host/docs/en.md) | Projects | The Complete Linux Machine: Kernel -> Virtual File... | `Complete curriculum toolchain` |
| **130** | [Linux and Docker](phases/phase-130-linux-and-docker/docs/en.md) | Modern Architecture | Docker Engine -> containerd -> runc -> clone(CLONE... | `docker run, ps aux | grep <app` |
| **131** | [Linux and Kubernetes](phases/phase-131-linux-and-kubernetes/docs/en.md) | Modern Architecture | Kubelet -> CRI -> OCI Runtime (runc) -> Pause Cont... | `crictl, ip link, iptables -L -` |
| **132** | [Linux and Databases](phases/phase-132-linux-and-databases/docs/en.md) | Modern Architecture | Database Query Engine -> Buffer Pool -> Linux Page... | `ps aux | grep postgres, ipcs -` |
| **133** | [Linux and Web Servers](phases/phase-133-linux-and-web-servers/docs/en.md) | Modern Architecture | Master Process (UID 0) -> Worker Processes (UID 33... | `ps -ef --forest | grep nginx, ` |
| **134** | [Linux and System Design](phases/phase-134-linux-and-system-design/docs/en.md) | Modern Architecture | Architectural Box -> Host Process (task_struct) | ... | `ps, ss, lsof, df, top` |
| **135** | [The Final Mental Model: Operating from Evidence](phases/phase-135-final-mental-model/docs/en.md) | Synthesis | The Unified Linux Machine: Hardware <-> Kernel (Sy... | `uname, ps, ss, df, journalctl,` |
