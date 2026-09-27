# Capstone 4: Tiny Educational Filesystem (`TinyFS`)

> **Motto:** Files do not exist on disk; only sectors, bitmaps, and inode pointer trees exist. The filesystem creates the illusion of hierarchical named files out of flat numbered blocks.

---

## 1. Architectural Disk Layout

`TinyFS` stores data inside a raw binary file (`virtual_disk.img`) simulating a physical hard drive or SSD block device:

```text
┌──────────────┬──────────────┬──────────────┬─────────────────────────┬─────────────────────────┐
│ Block 0      │ Block 1      │ Block 2      │ Blocks 3..10            │ Blocks 11..127          │
│ Superblock   │ Inode Bitmap │ Block Bitmap │ Inode Table (64 Inodes) │ Data Blocks (64 KB)     │
└──────────────┴──────────────┴──────────────┴─────────────────────────┴─────────────────────────┘
```

* **Superblock:** Holds filesystem metadata (magic number `0x54494E59`, block count, inode count, geometry).
* **Inode Bitmap:** Tracks allocation state of all 64 inodes.
* **Block Bitmap:** Tracks allocation state of all 128 disk blocks.
* **Inode Table:** Stores 64-byte inodes containing file type, byte size, and 4 direct block pointers.
* **Data Blocks:** Hold raw file payload bytes and directory entry arrays.

---

## 2. Running and Testing

```bash
python3 tiny_fs.py
```
