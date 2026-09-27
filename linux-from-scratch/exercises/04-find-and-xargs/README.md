# Exercise Set 04: Find & Xargs

### Ex 4.1: Find by Modification Time
Find all files in `/var/log` that were modified within the last 24 hours.

### Ex 4.2: Find by File Size
Find all regular files in `/var` that are larger than 50 Megabytes.

### Ex 4.3: Find by Inode Permissions
Find all files under `/tmp/lfs-lab` that have world-writable permissions (`o+w` or `0777`).

### Ex 4.4: Safe Deletion with Null Delimiters
Files can have filenames containing spaces and newlines (`file one.txt`, `log\n2.txt`). Construct a safe `find` pipeline using `-print0` and `xargs -0` to delete all `.tmp` files under a lab directory.

### Ex 4.5: Find Executing External Command
Using `find`, find all `.log` files in a directory and run `stat -c "%n %s bytes"` on each matching file using `-exec ... {} +` (batch mode).

### Ex 4.6: Find Restricting Depth
Search `/etc` for files ending in `.conf`, restricting the traversal depth to exactly 1 subdirectory (`-maxdepth 2`).

### Ex 4.7: Find by Ownership
Find all files under `/var` owned by user `www-data` (or UID 33).

### Ex 4.8: Find Inverting Conditions
Find all directories under `/tmp/lfs-lab` whose permissions are NOT `0755`.

### Ex 4.9: Parallel Execution with Xargs
Use `xargs -P 4` to process a list of 20 simulated tasks in parallel across 4 worker processes.

### Ex 4.10: Finding Empty Files and Directories
Use `find` to locate and list all 0-byte regular files and empty directories in a sandbox.
