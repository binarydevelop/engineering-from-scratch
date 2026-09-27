# Exercise Set 08: Storage, Mounts & Filesystems

### Ex 8.1: Block Device Hierarchy with lsblk
Run `lsblk -f`. Identify the disk devices, partitions, filesystem types (ext4, xfs, btrfs), UUIDs, and mount points.

### Ex 8.2: Disk Space vs Inode Exhaustion
Explain the difference between `df -h` and `df -i`. Describe a scenario where a program crashes with `No space left on device` even though `df -h` shows 50GB of free space.

### Ex 8.3: The df vs du Discrepancy
Why do `df` and `du` often report completely different numbers for the same filesystem? What does `df` measure that `du` cannot see?

### Ex 8.4: Creating and Mounting a Loopback Filesystem
Create a 100MB blank image file using `dd` or `truncate`. Format it with an `ext4` filesystem using `mkfs.ext4`. Mount it to `/tmp/lfs-lab/mnt`. Verify with `findmnt`.

### Ex 8.5: The Deleted Open File Space Leak
Create a 200MB file on your loopback mount. Open a Python script holding that file open. Delete the file using `rm`. Observe that `du` shows 0MB used, but `df` shows 200MB used! Prove the file is still held open using `lsof +L1`.

### Ex 8.6: Read-Only Filesystem Remount
Mount a filesystem with the `ro` (read-only) mount option. Attempt to create a file inside. Observe the exact kernel error message.

### Ex 8.7: Inspecting Filesystem Superblocks
Use `tune2fs -l <device>` (or `dumpe2fs`) to inspect the superblock parameters of an ext4 filesystem: block size, inode count, and mount count.

### Ex 8.8: Hard Links vs Symbolic Links
Create a hard link and a symbolic link to the same target file. Delete the original target file. What happens when you read the hard link? What happens when you read the symbolic link?

### Ex 8.9: /etc/fstab Anatomy
Examine `/etc/fstab`. Explain the meaning of the 6 columns: `device/UUID`, `mount point`, `filesystem type`, `options`, `dump`, and `pass/fsck order`.

### Ex 8.10: Safe Unmounting and Busy Mounts
When attempting to `umount /mnt`, the kernel returns `target is busy`. What command identifies which processes are holding working directories or open files on that mount point?
