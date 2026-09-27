# Track 5: Filesystems, I/O & Storage Exercises

> **Motto:** To the operating system, a file is an inode with an array of block numbers. The filename is merely a label inside a directory table.

All solutions are located in `solutions/exercises/05-filesystems-and-storage-solutions.md`.

---

### Exercise 5.1: File Descriptor Lifecycle (`open`, `read`, `write`, `close`)
Write a C program that opens a file, writes `"System Call I/O\n"` using `write()`, repositions the file offset to 0 using `lseek()`, reads the bytes back using `read()`, and verifies the buffer.

### Exercise 5.2: Inspecting File Metadata via `stat`
Write a program that takes a filename as a CLI argument and invokes `stat()`. Print the file's:
* Inode number (`st_ino`)
* File size in bytes (`st_size`)
* Number of allocated 512-byte disk blocks (`st_blocks`)
* Access permissions in octal
* Hard link count (`st_nlink`)

### Exercise 5.3: Creating Hard Links vs Symbolic Links
Create a file `original.txt`.
1. Create a hard link `hard.txt` using `link()`
2. Create a symlink `soft.txt` using `symlink()`
Inspect the inode numbers with `stat`. Delete `original.txt`. What happens when you read `hard.txt` vs `soft.txt`?

### Exercise 5.4: File Holes and Sparse Files
Using `lseek(fd, 1024 * 1024 * 1024, SEEK_SET)` (1 GB offset), write a single byte `'X'`. Inspect the file with `ls -lh` (reports 1GB) and `du -h` or `stat -c %b` (reports near 0 physical blocks). Explain what a **sparse file** is.

### Exercise 5.5: File Descriptor Duplication (`dup` and `dup2`)
Write a program that opens `log.txt`, duplicates its file descriptor onto standard output (`STDOUT_FILENO`) using `dup2()`, and calls `printf("This message goes to log.txt!\n")`.

### Exercise 5.6: Shared File Offsets Across `fork()`
Open a file in a parent process. Call `fork()`. In the child, write 5 bytes. In the parent, write 5 bytes. Show that both writes are sequential and do not overwrite each other, because parent and child share the underlying open-file object in the kernel.

### Exercise 5.7: Independent File Offsets Across Separate `open()` Calls
Open the same file twice in the same process using two distinct `open()` calls, obtaining `fd1` and `fd2`. Write 5 bytes to `fd1`, then write 5 bytes to `fd2`. Show that `fd2` overwrites the first 5 bytes because each open-file object maintains its own independent cursor offset.

### Exercise 5.8: Directory Traversal (`opendir`, `readdir`)
Write a custom implementation of `ls` using `opendir()` and `readdir()`. Print the inode number, file type (`d_type`), and filename for every entry in the current directory.

### Exercise 5.9: Durability and `fsync`
Write 10MB of data to a file using `write()`. Measure how long `write()` takes (returns almost instantly because data is buffered in the kernel page cache). Then call `fsync(fd)` and measure how long it takes to flush dirty pages down to physical NVMe/SSD storage.

### Exercise 5.10: Data-Only Synchronization (`fdatasync`)
Research the difference between `fsync()` and `fdatasync()`. Why do high-throughput databases (PostgreSQL, SQLite) prefer `fdatasync()` when modifying existing data pages to avoid synchronous metadata disk writes?

### Exercise 5.11: Atomic File Replacement via `rename`
Write a program that writes new data to a temporary file `config.tmp`, calls `fsync()`, and atomically replaces `config.json` using `rename("config.tmp", "config.json")`. Explain why POSIX `rename()` is crash-atomic.

### Exercise 5.12: File Locking with `flock`
Write two processes that attempt to acquire an exclusive lock on `lockfile.lock` using `flock(fd, LOCK_EX | LOCK_NB)`. Demonstrate how one process succeeds while the second fails with `EWOULDBLOCK`.

### Exercise 5.13: File Deletion Mechanics (Unlinking Open Files)
Open a 10MB file for reading. While the file descriptor is open, call `unlink()` on the file path. Show that `ls` no longer lists the file, but `df` shows disk space is still consumed! Close the file descriptor and verify that the kernel finally reclaims the disk blocks.

### Exercise 5.14: Inode Exhaustion Simulation
In Python, simulate a tiny filesystem with 16 inodes and 1000 data blocks. Create 16 empty files (0 bytes each). Attempt to create a 17th file. Show that the filesystem returns `ENOSPC (No space left on device)` even though 99% of data blocks are free!

### Exercise 5.15: Direct I/O (`O_DIRECT`)
On Linux, open a file with `O_DIRECT`. Explain why buffers passed to `read()` and `write()` must be memory-aligned to the physical storage sector size (typically 4096 bytes). Why do database engines sometimes bypass the kernel page cache with `O_DIRECT`?

### Exercise 5.16: Monitoring Filesystem Events (`inotify`)
On Linux, write a program that uses `inotify_init()` and `inotify_add_watch()` to listen for file modifications and creation events in a directory.

### Exercise 5.17: The Linux Page Cache & Dirty Pages
Inspect `/proc/meminfo` (`Dirty:`, `Writeback:`). Write a program that dirty-marks 50MB of memory via buffered file writes. Observe `Dirty` memory climb, and watch the background kernel `flusher` threads flush the pages to disk.

### Exercise 5.18: Inode Indirection & Block Addressing
Given a classic Unix filesystem with 12 direct block pointers, 1 single-indirect pointer, and 1 double-indirect pointer with 4KB block size:
1. What is the maximum file size addressable using only direct pointers?
2. What is the maximum file size supported by single indirection?

### Exercise 5.19: Simulating Write-Ahead Logging (WAL)
Implement a small Python class `WALFile` that appends transactions to a log file before updating an in-memory database table. Simulate a crash and replay the WAL to reconstruct state.

### Exercise 5.20: Inspecting Open File Tables with `lsof`
Run a long-running process that opens 5 different files and pipes. Use `lsof -p <PID>` to inspect the descriptor number, file type (`REG`, `FIFO`), device, node number, and active file offset.
