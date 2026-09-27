# Lab 01: Loopback Storage Sandbox

## Objective
Safely practice partitioning, formatting (`mkfs.ext4`), mounting, and filling filesystems without touching real physical storage drives.

## Setup Procedure
```bash
# 1. Create a 100MB sparse disk image file
truncate -s 100M /tmp/lfs-storage.img

# 2. Attach image to an available loopback block device
sudo losetup -fP /tmp/lfs-storage.img
LOOP_DEV=$(losetup -j /tmp/lfs-storage.img | cut -d: -f1)
echo "Attached as: $LOOP_DEV"

# 3. Format with ext4 filesystem
sudo mkfs.ext4 -L LFS_SANDBOX "$LOOP_DEV"

# 4. Create mount point and mount
mkdir -p /tmp/lfs-lab/mnt
sudo mount "$LOOP_DEV" /tmp/lfs-lab/mnt

# 5. Verify mount
findmnt /tmp/lfs-lab/mnt
```

## Teardown
```bash
sudo umount /tmp/lfs-lab/mnt
sudo losetup -d "$LOOP_DEV"
rm -f /tmp/lfs-storage.img
```
