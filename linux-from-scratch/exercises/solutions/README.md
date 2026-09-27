# Master Exercise Solutions & Diagnostic Guide

Complete, step-by-step technical solutions, explanations, and diagnostic principles for all 101 exercises in `linux-from-scratch`.

---

## Table of Contents
1. [Set 01: Navigation & Files (Ex 1.1 - 1.10)](#set-01-navigation--files)
2. [Set 02: Pipes & Redirection (Ex 2.1 - 2.10)](#set-02-pipes--redirection)
3. [Set 03: Text Processing Mastery (Ex 3.1 - 3.15)](#set-03-text-processing-mastery)
4. [Set 04: Find & Xargs (Ex 4.1 - 4.10)](#set-04-find--xargs)
5. [Set 05: Users, Groups & Permissions (Ex 5.1 - 5.10)](#set-05-users-groups--permissions)
6. [Set 06: Processes, Signals & Job Control (Ex 6.1 - 6.12)](#set-06-processes-signals--job-control)
7. [Set 07: Network Inspection & Sockets (Ex 7.1 - 7.12)](#set-07-network-inspection--sockets)
8. [Set 08: Storage, Mounts & Filesystems (Ex 8.1 - 8.10)](#set-08-storage-mounts--filesystems)
9. [Set 09: Services, systemd & Logging (Ex 9.1 - 9.10)](#set-09-services-systemd--logging)
10. [Set 10: Defensive Bash Scripting (Ex 10.1 - 10.12)](#set-10-defensive-bash-scripting)

---

## Set 01: Navigation & Files

### Ex 1.1: The Inode Identity
```bash
touch original.txt
ln original.txt hardlink.txt
ln -s original.txt symlink.txt
ls -li original.txt hardlink.txt symlink.txt
```
**Explanation**: The `-i` flag of `ls` displays the inode number (the first column). `original.txt` and `hardlink.txt` share the exact same integer inode number because a hard link is simply an additional directory entry pointing to the same filesystem inode. `symlink.txt` has a distinct inode number because a symbolic link is a distinct file whose contents are the string path of the target.

### Ex 1.2: Navigating Without CD
```bash
ls -latr /var/log
```
**Explanation**: `-l` produces long listing, `-a` includes hidden files, `-t` sorts by modification time (newest first), and `-r` reverses the order so the most recently modified files appear at the bottom of the screen.

### Ex 1.3: Hidden Directory Secrets
```bash
ls -d .!(|.)*
# Or using standard glob:
ls -d .[!.]*
```
**Explanation**: Running `ls -a` includes `.` (current directory) and `..` (parent directory). Matching `.[!.]*` matches any entry whose first character is a dot followed by any character other than a dot, effectively filtering out `.` and `..`.

### Ex 1.4: Safe Directory Tree Creation
```bash
mkdir -p /tmp/lfs-lab/prod/{services,databases,configs}/{primary,secondary}/logs
```
**Explanation**: The `-p` flag creates intermediate parent directories as needed without erroring if they exist. Bash brace expansion `{a,b}` generates the cartesian product of the paths.

### Ex 1.5: Preserving Timestamps and Ownership
```bash
cp -p /tmp/lfs-lab/source.bin /tmp/lfs-lab/backup.bin
# Or archive mode:
cp -a /tmp/lfs-lab/source.bin /tmp/lfs-lab/backup.bin
```
**Explanation**: Standard `cp` creates a new inode with the current user's default umask and current timestamp. `-p` (preserve) preserves mode, ownership, and timestamps. `-a` (archive) is equivalent to `-dR --preserve=all`.

### Ex 1.6: Atomic Renames
```bash
mv /tmp/lfs-lab/app.conf.new /tmp/lfs-lab/app.conf
```
**Explanation**: On POSIX filesystems, the `rename()` system call invoked by `mv` is atomic if both files reside on the same filesystem. Any process opening `/tmp/lfs-lab/app.conf` will see either the old file or the new file—never a missing or half-written file.

### Ex 1.7: Removing Difficult Filenames
```bash
# Method 1: Using the end-of-options delimiter '--'
rm -- -rf --help

# Method 2: Supplying a relative pathname prefix
rm ./-rf ./--help
```
**Explanation**: POSIX command utilities treat tokens starting with `-` as command-line flags. The double-dash `--` informs the argument parser that all subsequent tokens are operands, not flags. Alternatively, prefixing `./` ensures the token begins with a dot.

### Ex 1.8: Absolute vs Relative Path Proof
```bash
realpath -e /path/to/symlink
# Or using readlink:
readlink -f /path/to/symlink
```
**Explanation**: `realpath` resolves all symbolic links, relative segments (`.` and `..`), and outputs the canonical absolute path. `-e` verifies that all components must exist.

### Ex 1.9: Distinguishing File Types via Inodes
```bash
mkdir -p /tmp/lfs-lab/types && cd /tmp/lfs-lab/types
touch regular.txt                 # '-' Regular file
mkdir mydir                       # 'd' Directory
ln -s regular.txt mylink          # 'l' Symbolic link
mkfifo mypipe                     # 'p' Named pipe (FIFO)
python3 -c "import socket as s; sock = s.socket(s.AF_UNIX); sock.bind('mysock')" # 's' Socket
ls -l
```
**Explanation**: The first character of `ls -l` indicates the file type: `-` for regular file, `d` for directory, `l` for symlink, `p` for FIFO, `s` for socket, `b` for block device, and `c` for character device.

### Ex 1.10: Safe Recursive Removal
```bash
# Catastrophic: if TARGET_DIR is empty, 'rm -rf /*' is executed!
# Safe pattern:
if [ -n "${TARGET_DIR:-}" ] && [ -d "$TARGET_DIR" ]; then
    rm -rf "${TARGET_DIR:?}/"*
fi
```
**Explanation**: Using `${VAR:?Error message}` causes the shell to abort immediately with an error if the variable is unset or null.

---

## Set 02: Pipes & Redirection

### Ex 2.1: Separating Streams
```bash
command > /tmp/lfs-lab/out.log 2> /tmp/lfs-lab/err.log
```
**Explanation**: `>` is shorthand for `1>` (stdout). `2>` targets file descriptor 2 (stderr).

### Ex 2.2: Merging Diagnostic Streams
```bash
command > /tmp/lfs-lab/combined.log 2>&1
# Or modern Bash syntax:
command &> /tmp/lfs-lab/combined.log
```
**Explanation**: `2>&1` duplicates file descriptor 1 to file descriptor 2. The order matters: `> file 2>&1` first points FD 1 to `file`, then points FD 2 to where FD 1 is pointing.

### Ex 2.3: Discarding Noise Completely
```bash
command 2> /dev/null
```
**Explanation**: Data written to `/dev/null` is immediately discarded by the kernel's null character driver.

### Ex 2.4: Append vs Truncate Hazard
```bash
# Truncate (wipes file first):
echo "audit line" > /var/log/audit.log

# Append (adds to end of file):
echo "audit line" >> /var/log/audit.log
```
**Explanation**: `>` opens the target file with the `O_TRUNC` flag (emptying it). `>>` opens with `O_APPEND`.

### Ex 2.5: The Tee Diagnostic Tap
```bash
command | tee -a /tmp/lfs-lab/persistent.log
```
**Explanation**: `tee` copies standard input to standard output and simultaneously writes to one or more files. `-a` appends instead of overwriting.

### Ex 2.6: Input Redirection via Here-Doc
```bash
cat << 'EOF' > /tmp/lfs-lab/service.conf
[Service]
Port=8080
Workers=4
EOF
```

### Ex 2.7: Heredoc with Variable Interpolation
```bash
# Interpolation active (unquoted EOF):
cat << EOF
User: $USER
Host: $HOSTNAME
EOF

# Literal string preserved (quoted 'EOF'):
cat << 'EOF'
Var: $USER (literal)
EOF
```

### Ex 2.8: Pipeline Exit Codes and PIPESTATUS
```bash
false | true | cat
echo "$?"               # Outputs 0 (exit code of cat)
echo "${PIPESTATUS[@]}" # Outputs "1 0 0" (exit codes of false, true, cat)
```
**Explanation**: In standard POSIX shells, `$?` captures only the exit status of the *last* command in a pipeline. Bash maintains the `PIPESTATUS` array tracking each command in the chain.

### Ex 2.9: Process Substitution
```bash
diff -u <(ls /etc/pam.d) <(ls /etc/security)
```
**Explanation**: `<(command)` runs `command` asynchronously and connects its stdout to a named pipe or `/dev/fd/N` file descriptor, allowing commands expecting file paths to read command outputs directly.

### Ex 2.10: Custom File Descriptors
```bash
exec 3> /tmp/lfs-lab/custom.log
echo "Log message 1" >&3
echo "Log message 2" >&3
exec 3>&-   # Close FD 3
```
**Explanation**: `exec N> file` allocates file descriptor N for the duration of the current shell session. `exec N>&-` closes the file descriptor.

---

## Set 03: Text Processing Mastery

### Ex 3.1: Grep Inverting & Counting
```bash
grep -v -c "HTTP/1.1" 200" /var/log/nginx/access.log
```
**Explanation**: `-v` inverts the match (selects non-matching lines); `-c` prints only the count of matched lines.

### Ex 3.2: Regex Extraction with Egrep
```bash
grep -E -o '[0-9]{1,3}(\.[0-9]{1,3}){3}' /var/log/syslog
```
**Explanation**: `-E` enables Extended Regular Expressions; `-o` prints only the exact matched substring.

### Ex 3.3: Case-Insensitive Recursive Search
```bash
grep -rnI "PermitRootLogin" /etc 2>/dev/null
```
**Explanation**: `-r` is recursive, `-n` prints line numbers, `-I` skips binary files, and `2>/dev/null` discards permission denied warnings.

### Ex 3.4: Stream Editing: In-Place Safe Replacement
```bash
sed -i.bak 's/8080/9090/g' /tmp/lfs-lab/server.conf
```
**Explanation**: `-i.bak` creates `/tmp/lfs-lab/server.conf.bak` containing the original content before rewriting `server.conf` in place.

### Ex 3.5: Sed Address Ranges
```bash
sed -n '15,35p' /var/log/syslog
```
**Explanation**: `-n` suppresses default printing of every line; `'15,35p'` prints only lines within range 15 to 35.

### Ex 3.6: Sed Line Deletion
```bash
sed -E '/^[[:space:]]*($|#)/d' /etc/ssh/sshd_config
```
**Explanation**: Matches lines that contain only whitespace or begin with `#` (after optional whitespace) and deletes (`d`) them.

### Ex 3.7: Awk Column Extraction
```bash
awk -F: '{printf "%-20s\t%s\n", $1, $7}' /etc/passwd
```
**Explanation**: `-F:` specifies colon as field separator; `$1` is username, `$7` is shell.

### Ex 3.8: Awk Filtering by Numeric Threshold
```bash
awk -F: '$3 >= 1000 && $3 != 65534 {print $1, $3, $7}' /etc/passwd
```
**Explanation**: `$3` represents UID; filters for UIDs >= 1000 while excluding user `nobody`.

### Ex 3.9: Awk Summation & Averages
```bash
ls -l /var/log | awk '/^-/ {sum += $5} END {printf "Total Size: %.2f MB\n", sum / (1024 * 1024)}'
```
**Explanation**: Matches regular files (`/^-/`), accumulates byte size from column 5 (`$5`), and formats total in megabytes in the `END` block.

### Ex 3.10: Sort by Numeric Key
```bash
ps aux | sort -k3 -nr | head -10
```
**Explanation**: `-k3` specifies sorting on column 3 (CPU%), `-n` sorts numerically, `-r` reverses (descending).

### Ex 3.11: Finding Unique IP Frequencies
```bash
awk '{print $1}' access.log | sort | uniq -c | sort -nr | head -5
```
**Explanation**: `uniq -c` counts consecutive identical lines (which requires input to be sorted first). The second `sort -nr` sorts counts descending.

### Ex 3.12: Cut Field Extraction
```bash
cut -d',' -f2,4 data.csv
```
**Explanation**: `-d','` sets delimiter to comma; `-f2,4` extracts columns 2 and 4.

### Ex 3.13: Tr Character Translation & Deletion
```bash
cat file.txt | tr '[:lower:]' '[:upper:]'
tr -d '\r' < dosfile.txt > unixfile.txt
```
**Explanation**: `tr` operates purely on character streams without regular expressions.

### Ex 3.14: Line, Word, and Byte Auditing with WC
```bash
grep -c '/bin/bash$' /etc/passwd
# Or using wc:
grep '/bin/bash$' /etc/passwd | wc -l
```

### Ex 3.15: Combining the Pipeline
```bash
grep "Failed password for" /var/log/auth.log | awk '{for(i=1;i<=NF;i++) if($i=="for") print $(i+1)}' | sort | uniq -c | sort -nr
```
**Explanation**: Finds failed SSH logins, extracts the username following the word "for", aggregates frequency with `uniq -c`, and displays ranked list.

---

## Set 04: Find & Xargs

### Ex 4.1: Find by Modification Time
```bash
find /var/log -type f -mtime -1
```
**Explanation**: `-mtime -1` matches files modified strictly less than 24 hours ago.

### Ex 4.2: Find by File Size
```bash
find /var -type f -size +50M
```
**Explanation**: `-size +50M` matches files strictly greater than 50 Megabytes (units: `k`, `M`, `G`).

### Ex 4.3: Find by Inode Permissions
```bash
find /tmp/lfs-lab -type f -perm -0002
# Or exact 777:
find /tmp/lfs-lab -type f -perm 0777
```
**Explanation**: `-perm -0002` matches any file where the "other write" bit is set.

### Ex 4.4: Safe Deletion with Null Delimiters
```bash
find /tmp/lfs-lab -type f -name "*.tmp" -print0 | xargs -0 rm -f
```
**Explanation**: `-print0` separates filenames with null bytes (`\0`), which cannot exist in Linux filenames. `xargs -0` splits strictly on null bytes, neutralizing spaces and newlines.

### Ex 4.5: Find Executing External Command
```bash
find /var/log -type f -name "*.log" -exec stat -c "%n %s bytes" {} +
```
**Explanation**: Ending with `+` aggregates filenames into a single command invocation (like `xargs`), avoiding spawning a separate process per file.

### Ex 4.6: Find Restricting Depth
```bash
find /etc -maxdepth 2 -name "*.conf"
```
**Explanation**: `-maxdepth 2` prevents `find` from traversing past 1 level of subdirectories.

### Ex 4.7: Find by Ownership
```bash
find /var -user www-data
```

### Ex 4.8: Find Inverting Conditions
```bash
find /tmp/lfs-lab -type d ! -perm 0755
```
**Explanation**: The exclamation mark `!` negates the succeeding predicate.

### Ex 4.9: Parallel Execution with Xargs
```bash
printf '%s\n' {1..20} | xargs -P 4 -n 1 -I {} bash -c 'sleep 1; echo "Task {} done on $(date +%T)"'
```
**Explanation**: `-P 4` spawns up to 4 concurrent worker processes; `-n 1` passes one argument per invocation.

### Ex 4.10: Finding Empty Files and Directories
```bash
find /tmp/lfs-lab -empty
```
**Explanation**: `-empty` matches 0-byte regular files or directories containing zero entries.

---

## Set 05: Users, Groups & Permissions

### Ex 5.1: Inspecting User & Group Identity
```bash
id
```
**Explanation**: Displays current user `uid`, primary `gid`, and all supplementary groups `groups=...`.

### Ex 5.2: The Directory Traversal Trap
```bash
mkdir /tmp/lfs-lab/private
chmod 0644 /tmp/lfs-lab/private
cd /tmp/lfs-lab/private
# Result: bash: cd: /tmp/lfs-lab/private: Permission denied
```
**Explanation**: On directories, the execute (`x`) permission bit does NOT mean executing a program. It grants **directory traversal** (permission to `cd` into the directory or access inodes inside it). The read (`r`) bit only allows listing file names with `ls`. Without `+x`, you cannot read metadata or open files inside!

### Ex 5.3: Symbolic vs Numeric chmod
```bash
chmod g+r,o+r file.txt   # Symbolic
chmod 644 file.txt       # Numeric octal (4+2=6 for user, 4 for group, 4 for other)
```

### Ex 5.4: Umask Calculation
Standard base permissions:
- Files: `0666` (`rw-rw-rw-`)
- Directories: `0777` (`rwxrwxrwx`)
With `umask 0022`:
- New File: `0666 - 0022 = 0644` (`rw-r--r--`)
- New Directory: `0777 - 0022 = 0755` (`rwxr-xr-x`)

### Ex 5.5: Setting a Restrictive Umask
```bash
umask 0077
touch secret.txt && mkdir secretdir
ls -ld secret.txt secretdir
# secret.txt: -rw------- (0600)
# secretdir:  drwx------ (0700)
```

### Ex 5.6: The Setgid Directory for Shared Teams
```bash
mkdir /tmp/lfs-lab/team_share
chgrp developers /tmp/lfs-lab/team_share
chmod 2775 /tmp/lfs-lab/team_share  # 2 is the SGID bit
touch /tmp/lfs-lab/team_share/newfile
ls -l /tmp/lfs-lab/team_share/newfile
```
**Explanation**: When the SGID bit (`2000`) is set on a directory, any file created inside automatically inherits the **group owner** of the parent directory rather than the primary group of the creating user.

### Ex 5.7: The Sticky Bit on Shared Directories
```bash
ls -ld /tmp
# drwxrwxrwt 15 root root ...
```
**Explanation**: Mode `1777` (`t`). On a world-writable directory (`0777`), any user could delete any other user's files. The sticky bit restricts file deletion and renaming: only the file owner, the directory owner, or root can delete files inside.

### Ex 5.8: SUID Binary Audit
```bash
find / -perm -4000 -type f 2>/dev/null
```
**Explanation**: When an executable has the SUID bit (`4000`), the kernel executes it with the privileges of the file's owner (root). `/usr/bin/passwd` must be SUID root because regular users need to update `/etc/shadow`, which is readable and writable only by root.

### Ex 5.9: Sudo Command Restriction
In `/etc/sudoers`:
```text
operator ALL=(root) NOPASSWD: /bin/systemctl restart nginx, /bin/systemctl status nginx
```
**Explanation**: Allows user `operator` to run only those specific commands with root privileges without password authentication.

### Ex 5.10: Diagnosing Multi-Level Access Denials
```bash
namei -l /data/apps/service/config.yaml
```
**Explanation**: `namei` walks each path component from `/` down to the target file, printing the exact permission bits and ownership at every step, immediately revealing which parent directory lacks execute traversal (`x`).

---

## Set 06: Processes, Signals & Job Control

### Ex 6.1: Program vs Process Distinction
A **program** is an inert ELF binary file residing on secondary storage. A **process** is an active execution context instantiated in memory by the kernel, containing virtual address space mappings, execution threads, open file descriptors, credentials (UID/GID), and environment variables tracked via `task_struct`.

### Ex 6.2: Inspecting Process Lineage
```bash
sleep 100 &
ps -ef | grep "[s]leep 100"
echo "My Shell PID: $$"
```

### Ex 6.3: Foreground to Background Job Control
```bash
sleep 300
# Press Ctrl-Z -> [1]+ Stopped sleep 300
jobs
bg %1
jobs          # Shows Running
fg %1
# Press Ctrl-C -> Terminates process
```

### Ex 6.4: Signals: SIGTERM vs SIGKILL
```bash
sleep 500 & PID1=$!
sleep 500 & PID2=$!
kill -15 $PID1   # SIGTERM: Request graceful termination (can be caught)
kill -9  $PID2   # SIGKILL: Immediate unconditional termination by kernel (cannot be caught)
```

### Ex 6.5: SIGHUP and Hangup Immunity
When an interactive terminal closes, the kernel sends `SIGHUP` (Signal 1) to all foreground and background processes in that session. Using `nohup command &` or `disown -h %1` blocks SIGHUP delivery.

### Ex 6.6: Exploring /proc/<pid>/ Internals
```bash
PID=$(pgrep -f "python3 -m http.server" | head -1)
cat /proc/$PID/cmdline | tr '\0' ' '; echo ""
ls -l /proc/$PID/cwd
ls -l /proc/$PID/fd
cat /proc/$PID/status | head -15
```

### Ex 6.7: Process States
- `R`: Running or runnable (on CPU run queue)
- `S`: Interruptible sleep (waiting for event or timer)
- `D`: Uninterruptible sleep (usually waiting on disk I/O; cannot be killed!)
- `Z`: Zombie (terminated but un-reaped by parent)
- `T`: Stopped (by signal e.g. Ctrl-Z or debugger)

### Ex 6.8: Trapping Signals in Bash
```bash
#!/usr/bin/env bash
TMP_FILE=$(mktemp /tmp/lfs-app.XXXXXX)
cleanup() {
    echo "Caught signal! Cleaning up $TMP_FILE..."
    rm -f "$TMP_FILE"
    exit 0
}
trap cleanup SIGINT SIGTERM
echo "Running (PID: $$). Press Ctrl-C to test trap."
while true; do sleep 1; done
```

### Ex 6.9: Auditing Open File Descriptors with lsof
```bash
lsof -p <PID>
```

### Ex 6.10: Process Priorities with Nice and Renice
```bash
nice -n 19 dd if=/dev/zero of=/dev/null &
PID=$!
renice -n 0 -p $PID
kill -9 $PID
```
**Explanation**: `nice` ranges from `-20` (highest priority) to `19` (lowest priority). Unprivileged users can only lower their priority (increase nice number).

### Ex 6.11: Inspecting Thread Trees
```bash
ps -T -p <PID>
```

### Ex 6.12: Identifying Zombie Processes
A zombie process has exited and released its memory and open files, but its PID and exit status remain in the kernel process table until its parent calls `wait()` or `waitpid()`. You cannot kill a zombie with `kill -9` because it is already dead. You must terminate the neglectful parent process, causing the zombie to be adopted by PID 1 (systemd), which immediately reaps it.

---

## Set 07: Network Inspection & Sockets

### Ex 7.1: Network Interface Status
```bash
ip link show
```
**Explanation**: `lo` is loopback (`127.0.0.1`). Physical or virtual NICs appear as `eth0`, `enp3s0`, etc.

### Ex 7.2: IP and Subnet Mask Inspection
```bash
ip -4 -br addr
```

### Ex 7.3: Default Gateway and Routing Table
```bash
ip route show
# 'default via 192.168.1.1 dev eth0 proto dhcp metric 100'
```

### Ex 7.4: Listening TCP Ports with ss
```bash
ss -lntp
```
**Explanation**: `-l` lists listening sockets, `-n` prevents slow DNS port lookups (shows raw numbers), `-t` restricts to TCP, `-p` displays process name and PID.

### Ex 7.5: The Localhost Binding Trap
A socket bound to `127.0.0.1` binds exclusively to the loopback interface (`lo`). The kernel drops packets arriving on physical interfaces (`eth0`) addressed to loopback. To accept connections from outside hosts, the application must bind to `0.0.0.0` (all IPv4 interfaces) or the specific public IP.

### Ex 7.6: Testing Port Reachability with Netcat
```bash
nc -zv 127.0.0.1 8080
```

### Ex 7.7: Verbose HTTP Inspection with Curl
```bash
curl -Iv https://example.com
```

### Ex 7.8: Tracing DNS Resolution with Dig
```bash
dig +trace example.com
```

### Ex 7.9: The /etc/hosts Override
Edit `/etc/hosts` to add:
```text
127.0.0.1 test.internal
```
Verify with `getent hosts test.internal`.

### Ex 7.10: Capturing Packets with tcpdump
```bash
sudo tcpdump -i lo -nn "port 8080"
```

### Ex 7.11: Identifying Socket Owning Processes
```bash
sudo ss -lntp '( sport = :5432 )'
sudo lsof -i :5432
```

### Ex 7.12: Testing UDP vs TCP Connectivity
ICMP (used by `ping`) operates at the Network Layer (Layer 3) without ports. TCP/UDP operate at the Transport Layer (Layer 4). A server can respond to ICMP pings while its web server application is dead, or a firewall may block ICMP while permitting TCP port 443.

---

## Set 08: Storage, Mounts & Filesystems

### Ex 8.1: Block Device Hierarchy with lsblk
```bash
lsblk -f
```

### Ex 8.2: Disk Space vs Inode Exhaustion
Every regular file and directory requires an **inode** to store its metadata. If an application creates millions of 0-byte log files, all filesystem inodes are consumed (`df -i` shows 100%). Any subsequent attempt to create a file fails with `No space left on device`, despite `df -h` showing gigabytes of unused storage blocks.

### Ex 8.3: The df vs du Discrepancy
`df` queries the filesystem superblock for total allocated vs unallocated block counts. `du` walks the active directory hierarchy, summing file sizes. When a file is deleted with `rm` while a running process holds its file descriptor open, its directory entry is removed (invisible to `du`), but the kernel cannot free its disk blocks until the process closes the file (tracked by `df`).

### Ex 8.4: Creating and Mounting a Loopback Filesystem
```bash
dd if=/dev/zero of=/tmp/lfs-storage.img bs=1M count=100
mkfs.ext4 /tmp/lfs-storage.img
mkdir -p /tmp/lfs-lab/mnt
sudo mount -o loop /tmp/lfs-storage.img /tmp/lfs-lab/mnt
findmnt /tmp/lfs-lab/mnt
```

### Ex 8.5: The Deleted Open File Space Leak
```bash
# In shell 1:
python3 -c 'f=open("/tmp/lfs-lab/mnt/large.bin", "w"); f.write("0"*150000000); f.flush(); import time; time.sleep(60)' &
# In shell 2:
rm /tmp/lfs-lab/mnt/large.bin
du -sh /tmp/lfs-lab/mnt         # Shows ~0MB
df -h /tmp/lfs-lab/mnt          # Shows 150MB used!
lsof +L1 /tmp/lfs-lab/mnt       # Shows deleted file held by Python PID
```

### Ex 8.6: Read-Only Filesystem Remount
```bash
sudo mount -o remount,ro /tmp/lfs-lab/mnt
touch /tmp/lfs-lab/mnt/test.txt
# Output: touch: cannot touch '/tmp/lfs-lab/mnt/test.txt': Read-only file system
```

### Ex 8.7: Inspecting Filesystem Superblocks
```bash
sudo tune2fs -l /tmp/lfs-storage.img | grep -E "Block size|Inode count|Mount count"
```

### Ex 8.8: Hard Links vs Symbolic Links
When the original target of a symbolic link is deleted, the symlink becomes a **dangling (broken) symlink** pointing to non-existent target. When the target of a hard link is deleted, the file data remains intact and fully readable because the hard link still points directly to the inode (the inode's link count is simply decremented from 2 to 1).

### Ex 8.9: /etc/fstab Anatomy
Column layout:
1. `Device / UUID`: Filesystem identifier
2. `Mount Point`: Target directory
3. `Type`: ext4, xfs, nfs
4. `Options`: defaults, noatime, ro
5. `Dump`: 0 (disabled backup flag)
6. `Pass`: fsck order at boot (1 for root, 2 for other, 0 to skip)

### Ex 8.10: Safe Unmounting and Busy Mounts
```bash
fuser -vm /tmp/lfs-lab/mnt
# Or:
lsof +D /tmp/lfs-lab/mnt
```

---

## Set 09: Services, systemd & Logging

### Ex 9.1: Systemd Service States
- `loaded`: Unit configuration file parsed and loaded in memory
- `active (running)`: Daemon process is active and running
- `active (exited)`: One-shot service executed successfully and finished
- `failed`: Process crashed, returned non-zero exit code, or timed out

### Ex 9.2: Starting, Stopping, and Reloading
`restart` shuts down the process (`SIGTERM`/`SIGKILL`) and starts a fresh instance, dropping active client connections. `reload` sends `SIGHUP` instructing the master process to re-parse config files while maintaining client sockets without downtime.

### Ex 9.3: Enabling Services at Boot
`systemctl enable <service>` creates a symbolic link in `/etc/systemd/system/multi-user.target.wants/` pointing to the unit file in `/lib/systemd/system/`.

### Ex 9.4: Writing a Minimal Service Unit
```ini
[Unit]
Description=LFS Demo Service
After=network.target

[Service]
Type=simple
User=nobody
ExecStart=/usr/bin/python3 -m http.server 8080
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

### Ex 9.5: Systemd Unit Reload Mechanics
systemd caches unit definitions in memory for performance. When a file on disk is altered, systemd continues using the cached version until instructed to re-read files via `systemctl daemon-reload`.

### Ex 9.6: Journalctl Service Filtering
```bash
journalctl -u lfs-demo.service -f
```

### Ex 9.7: Journalctl Time Windows and Priority
```bash
journalctl -p err --since "1 hour ago"
```

### Ex 9.8: Systemd Timers vs Cron
`lfs-backup.timer`:
```ini
[Unit]
Description=Nightly Backup Timer

[Timer]
OnCalendar=*-*-* 02:00:00 UTC
Persistent=true

[Install]
WantedBy=timers.target
```
Inspect with `systemctl list-timers`.

### Ex 9.9: Debugging a Service with Exit Code 203/EXEC
Exit code 203 indicates that systemd failed to execute the command specified in `ExecStart` (e.g. file missing, wrong path, missing `+x` executable permission, or invalid shebang line `#!/bin/bash`).

### Ex 9.10: Inspecting Service Cgroups and Resource Limits
```bash
systemctl show lfs-demo.service -p MemoryCurrent,CPUUsageNSec
systemd-cgls
```

---

## Set 10: Defensive Bash Scripting

### Ex 10.1: The Defensive Preamble
- `-e`: Abort script if any command exits non-zero (prevents runaway errors).
- `-u`: Treat unset variables as an error and exit immediately (prevents `rm -rf $UNSET/*`).
- `-o pipefail`: Return exit code of the last failing command in a pipeline, rather than only the final command.

### Ex 10.2: Safe Variable Quoting
```bash
FILE="my report.txt"
# Dangerous: rm $FILE (attempts to delete 'my' and 'report.txt')
# Safe:
rm "$FILE"
```

### Ex 10.3: Exit Codes and Conditional Execution
```bash
[ -d "/tmp/lfs-lab" ] || mkdir -p "/tmp/lfs-lab" || { echo "Failed to create dir" >&2; exit 1; }
```

### Ex 10.4: Safe Iteration Over Files
```bash
shopt -s nullglob
for logfile in /var/log/*.log; do
    echo "Processing $logfile"
done
```
**Explanation**: `nullglob` ensures that if no files match, the loop executes zero times instead of receiving the literal string `/var/log/*.log`.

### Ex 10.5: Processing Input Line by Line
```bash
while IFS= read -r line || [ -n "$line" ]; do
    echo "Line: $line"
done < input.txt
```
**Explanation**: `IFS=` prevents trimming leading/trailing whitespace; `-r` prevents backslash interpretation; `|| [ -n "$line" ]` ensures the final line is processed even if it lacks a trailing newline.

### Ex 10.6: Bash Script Arguments and Shifts
```bash
while [ $# -gt 0 ]; do
    case "$1" in
        -u|--user) USER="$2"; shift 2 ;;
        -d|--dir)  DIR="$2"; shift 2 ;;
        -h|--help) echo "Usage: $0 -u <user> -d <dir>"; exit 0 ;;
        *) echo "Unknown flag: $1" >&2; exit 1 ;;
    esac
done
```

### Ex 10.7: Trap for Guaranteed Resource Cleanup
```bash
TMP_DIR=$(mktemp -d /tmp/lfs-clean.XXXXXX)
trap 'echo "Cleaning $TMP_DIR"; rm -rf "$TMP_DIR"' EXIT
# Script operations...
```

### Ex 10.8: Bash Functions and Local Scope
```bash
get_disk_usage() {
    local target_mount="$1"
    local usage
    usage=$(df --output=pcent "$target_mount" | tail -1 | tr -dc '0-9')
    echo "$usage"
}
```

### Ex 10.9: Integer Arithmetic vs External Tools
```bash
COUNT=10
TOTAL=$(( (COUNT * 5) + 20 ))
echo "$TOTAL" # 70
```

### Ex 10.10: String Manipulation Without Sed/Awk
```bash
PATHNAME="/var/log/nginx/access.log"
FILENAME="${PATHNAME##*/}"   # access.log
BASENAME="${FILENAME%.*}"     # access
EXT="${FILENAME##*.}"         # log
```

### Ex 10.11: Atomic Locking with Flock
```bash
#!/usr/bin/env bash
exec 200>/var/lock/lfs-script.lock
flock -n 200 || { echo "Another instance is already running!" >&2; exit 1; }
# Critical section...
```

### Ex 10.12: ShellCheck Linting
Refactoring code flagged by ShellCheck ensures compliance with POSIX and Bash standards, preventing word splitting (SC2086), useless cats (SC2002), and unassigned return codes (SC2181).
