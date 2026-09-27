# Diagnostic Command Map (Organized by Question)

> Never memorize commands alphabetically. When operating a Linux system, start with the **question**, identify the **Linux object** holding the answer, and execute the **targeted inspection tool**.

---

## 1. What distribution and kernel is running?
- **Object**: `/etc/os-release`, `/proc/version`, kernel release string.
- **Inspection Tools**:
  ```bash
  uname -a                    # Kernel release, build date, architecture
  uname -r                    # Exact kernel version string
  cat /etc/os-release         # Distribution name, version, ID, codename
  hostnamectl                 # Complete system summary (kernel, OS, architecture, chassis)
  ```

---

## 2. What processes are running and who owns them?
- **Object**: Kernel process table (`/proc/<pid>/`).
- **Inspection Tools**:
  ```bash
  ps aux                      # Full snapshot of all processes with CPU%, MEM%, user, PID
  ps -ef                      # Standard UNIX format showing PPID (parent PID)
  pstree -p                   # Visual process hierarchy showing tree relationships
  pgrep -l <name>             # Lookup PIDs matching process name
  pidstat 1                   # Real-time per-process CPU consumption
  ```

---

## 3. What is consuming CPU and Memory?
- **Object**: `/proc/stat`, `/proc/meminfo`, `/proc/<pid>/status`.
- **Inspection Tools**:
  ```bash
  top                         # Interactive system monitor (press 'M' for memory, 'P' for CPU)
  free -h                     # RAM and Swap summary (Focus on 'available', NOT 'free'!)
  vmstat 1 5                  # Virtual memory statistics (run queue 'r', blocked 'b', si/so)
  ps aux --sort=-%cpu | head -10 # Top 10 CPU-consuming processes
  ps aux --sort=-%mem | head -10 # Top 10 Memory-consuming processes
  ```

---

## 4. What ports are listening and who owns them?
- **Object**: Kernel TCP/UDP socket tables (`/proc/net/tcp`, `/proc/net/udp`).
- **Inspection Tools**:
  ```bash
  ss -lntp                    # Listening TCP ports with numeric IPs and owning Process/PID
  ss -lunp                    # Listening UDP ports with owning Process/PID
  ss -antp                    # All TCP connections (LISTEN, ESTABLISHED, TIME_WAIT)
  lsof -i :8080               # Find exact process holding port 8080 open
  ```

---

## 5. Why did a service fail?
- **Object**: systemd unit state, cgroup status, system journal logs.
- **Inspection Tools**:
  ```bash
  systemctl --failed          # List all units currently in failed state
  systemctl status <service>  # Exit code, status message, active PID, recent logs
  journalctl -u <service> -e  # Jump to latest logs for specific service
  journalctl -u <service> -b  # Logs for service since current system boot
  journalctl -u <service> -p err # Filter service logs by error priority or higher
  ```

---

## 6. Where is my disk space going?
- **Object**: Filesystem superblock (`df`), directory entries (`du`), unlinked open files (`lsof`).
- **Inspection Tools**:
  ```bash
  df -hT                      # Filesystem usage, mount points, and filesystem types
  df -i                       # Inode usage (catches 'No space left' when disk has MBs free!)
  du -ahx /var | sort -rh | head -20 # Top 20 largest directories/files on /var filesystem
  lsof +L1                    # Find open file descriptors to deleted files holding disk space
  ```

---

## 7. Why is access denied to a file or directory?
- **Object**: Inode mode bits (rwx), UID/GID ownership, directory traversal bits.
- **Inspection Tools**:
  ```bash
  ls -la /path/to/file        # Inspect file permissions, owner, and group
  ls -ld /path/to/directory   # Inspect directory permissions (requires 'x' to enter!)
  namei -l /full/path/to/file # Walk every parent directory verifying permissions at each level
  id                          # Check your current UID, GID, and supplementary groups
  stat /path/to/file          # Complete inode metadata (octal permissions, access/mod times)
  ```

---

## 8. Why can't this host reach another host?
- **Object**: Network interfaces, IP configuration, routing table, ARP cache, packet drops.
- **Inspection Tools**:
  ```bash
  ip link                     # Verify interface state (UP or DOWN) and MAC address
  ip addr                     # Verify assigned IP address and CIDR subnet mask
  ip route                    # Inspect routing table and default gateway ('default via ...')
  ip neigh                    # Inspect ARP table (resolved MAC addresses for neighbor IPs)
  ping -c 4 <ip>              # Test ICMP echo reachability and round-trip latency
  traceroute -n <ip>          # Trace network hops to destination
  curl -Iv https://<host>     # Test end-to-end DNS, TCP handshake, TLS, and HTTP response
  ```

---

## 9. Why is DNS resolution failing?
- **Object**: `/etc/resolv.conf`, `systemd-resolved`, `/etc/hosts`, `/etc/nsswitch.conf`.
- **Inspection Tools**:
  ```bash
  resolvectl status           # Inspect active DNS servers per interface in systemd-resolved
  dig <hostname> +trace       # Full DNS lookup trace from root servers to authoritative NS
  getent hosts <hostname>     # Test NSS resolver path (honors /etc/hosts and DNS)
  cat /etc/resolv.conf        # Check configured nameservers
  ```

---

## 10. Why are there "Too many open files"?
- **Object**: Process file descriptor table (`/proc/<pid>/fd/`), system limits (`ulimit`).
- **Inspection Tools**:
  ```bash
  ulimit -n                   # Current shell process file descriptor limit
  ls -l /proc/<pid>/fd | wc -l # Count open file descriptors held by specific process
  lsof -p <pid>               # List every file, socket, pipe opened by process
  cat /proc/sys/fs/file-nr    # System-wide allocated vs maximum file handles
  ```
