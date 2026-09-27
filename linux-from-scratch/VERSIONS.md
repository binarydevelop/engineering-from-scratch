# Environment & Tool Versions

This curriculum is developed and validated against a standardized, long-term support Linux reference platform.

---

## Primary Reference Distribution

- **Distribution**: Ubuntu 24.04 LTS (Noble Numbat) / Debian 12 (Bookworm)
- **Kernel**: Linux 6.8.0-generic (x86_64 and aarch64)
- **Init System**: systemd 255.4
- **Primary Shell**: GNU Bash 5.2.21
- **C Library**: GNU C Library (glibc) 2.39

---

## Core Tool Versions Tested

| Tool Suite | Representative Tools | Tested Version | Upstream Package |
| :--- | :--- | :--- | :--- |
| **GNU Coreutils** | `ls`, `cp`, `mv`, `rm`, `cat`, `head`, `tail`, `wc`, `stat`, `chown`, `chmod` | 9.4 | `coreutils` |
| **iproute2** | `ip addr`, `ip route`, `ip link`, `ss` | 6.8.0 | `iproute2` |
| **procps-ng** | `ps`, `top`, `free`, `vmstat`, `sysctl`, `pidstat` | 4.0.4 | `procps` |
| **systemd** | `systemctl`, `journalctl`, `timedatectl`, `resolvectl` | 255 | `systemd` |
| **GNU Findutils**| `find`, `xargs` | 4.9.0 | `findutils` |
| **GNU Grep** | `grep`, `egrep`, `fgrep` | 3.11 | `grep` |
| **GNU Sed** | `sed` | 4.9 | `sed` |
| **GNU Awk** | `gawk` / `awk` | 5.2.1 | `gawk` |
| **util-linux** | `lsblk`, `blkid`, `mount`, `umount`, `lscpu`, `dmesg`, `flock` | 2.39.3 | `util-linux` |
| **OpenSSH** | `ssh`, `sshd`, `ssh-keygen`, `scp`, `sftp` | 9.6p1 | `openssh-client`, `openssh-server` |
| **Netcat** | `nc` (OpenBSD variant) | 1.226 | `netcat-openbsd` |
| **curl** | `curl` | 8.5.0 | `curl` |
| **strace** | `strace` | 6.8 | `strace` |
| **lsof** | `lsof` | 4.98.0 | `lsof` |

---

## Distribution Translation Matrix

While exact commands in this curriculum target Debian/Ubuntu syntax, the underlying Linux kernel abstractions remain identical across all distributions. Here is how key administration commands map to other popular families:

| Task | Debian / Ubuntu | Fedora / RHEL / Rocky | Arch Linux |
| :--- | :--- | :--- | :--- |
| **Package search** | `apt search <pkg>` | `dnf search <pkg>` | `pacman -Ss <pkg>` |
| **Package install** | `apt install -y <pkg>` | `dnf install -y <pkg>` | `pacman -S <pkg>` |
| **File to package** | `dpkg -S /path/to/file` | `rpm -qf /path/to/file` | `pacman -Qo /path/to/file` |
| **List package files** | `dpkg -L <pkg>` | `rpm -ql <pkg>` | `pacman -Ql <pkg>` |
| **Network config** | Netplan (`/etc/netplan/`) | NetworkManager (`nmcli`) | systemd-networkd |
| **Firewall frontend** | `ufw` / `nftables` | `firewalld` (`firewall-cmd`) | `nftables` |
| **Service manager** | `systemctl` | `systemctl` | `systemctl` |
| **Kernel messages** | `dmesg -T` | `dmesg -T` | `dmesg -T` |
| **Security module** | AppArmor | SELinux | None / AppArmor |
