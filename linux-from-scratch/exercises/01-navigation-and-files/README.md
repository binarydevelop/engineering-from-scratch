# Exercise Set 01: Navigation & Files

### Ex 1.1: The Inode Identity
Create three files: `original.txt`, `hardlink.txt` pointing to `original.txt`, and `symlink.txt` pointing to `original.txt`. Use a single command to prove which two files share the exact same physical inode structure on the disk.

### Ex 1.2: Navigating Without CD
Without running `cd` or changing your current working directory, list all files (including hidden) in `/var/log` sorted by modification time in reverse order.

### Ex 1.3: Hidden Directory Secrets
Under `/tmp/lfs-lab/ex03`, create a nested directory structure containing normal files, hidden files (starting with `.`), and a hidden directory containing files. Write a command to display only the hidden entries at the top level without listing the current (`.`) or parent (`..`) directories.

### Ex 1.4: Safe Directory Tree Creation
Using a single `mkdir` invocation, construct the complete directory hierarchy:
`/tmp/lfs-lab/prod/{services,databases,configs}/{primary,secondary}/logs`. Verify the resulting tree with `find` or `tree`.

### Ex 1.5: Preserving Timestamps and Ownership
Create a file `/tmp/lfs-lab/source.bin` with specific permissions (`0640`). Copy it to `/tmp/lfs-lab/backup.bin` such that the modification time, access time, and permission mode bits are guaranteed to remain identical down to the nanosecond.

### Ex 1.6: Atomic Renames
In Linux, what system call enables atomic file swapping? Demonstrate how `mv` can be used to swap an active production configuration file with a new version without exposing a missing-file window to reader processes.

### Ex 1.7: Removing Difficult Filenames
Accidentally create a file named `-rf` and a file named `--help` in a sandbox directory. Demonstrate two different safe methods to delete these files using `rm` without triggering option parsing.

### Ex 1.8: Absolute vs Relative Path Proof
Write a command that displays the canonical absolute path of a deeply nested symlink chain, resolving every intermediate symbolic link to its final target.

### Ex 1.9: Distinguishing File Types via Inodes
Linux supports 7 distinct file types. Create examples in `/tmp/lfs-lab/types` of: a regular file, a directory, a symbolic link, a named pipe (FIFO), and a UNIX domain socket. Verify each type with `ls -l` and `stat`.

### Ex 1.10: Safe Recursive Removal
Why is running `rm -rf $DIR/*` catastrophic if `$DIR` is empty or unset? Write a safe shell pattern that ensures deletion occurs only if the variable is non-empty and points to a verified lab directory.
