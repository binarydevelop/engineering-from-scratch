# Solutions: Track 5 Filesystems & Storage Exercises

### Solution 5.1: File Descriptor Lifecycle
```c
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

int main(void) {
    int fd = open("test_io.txt", O_RDWR | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) return 1;

    const char msg[] = "System Call I/O\n";
    write(fd, msg, strlen(msg));

    // Reposition cursor to beginning of file
    lseek(fd, 0, SEEK_SET);

    char buf[64];
    ssize_t bytes_read = read(fd, buf, sizeof(buf) - 1);
    buf[bytes_read] = '\0';
    printf("Read back: %s", buf);

    close(fd);
    unlink("test_io.txt");
    return 0;
}
```

### Solution 5.3: Hard Link vs Symlink Behavior
* **Hard link:** Points directly to the same Inode number. Deleting `original.txt` decrements `st_nlink` from 2 to 1, but the file data blocks and inode remain fully accessible via `hard.txt`.
* **Symlink (Soft link):** Contains a string path pointing to `original.txt`. Deleting `original.txt` turns `soft.txt` into a dangling symlink (reading returns `ENOENT`).

### Solution 5.5: File Redirection via `dup2`
```c
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main(void) {
    int fd = open("log.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) return 1;

    // Replace stdout (FD 1) with log.txt descriptor
    dup2(fd, STDOUT_FILENO);
    close(fd);

    printf("This message is written directly into log.txt via dup2!\n");
    fflush(stdout);
    return 0;
}
```

### Solution 5.9: Durability with `fsync`
```c
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <stdlib.h>

int main(void) {
    int fd = open("durability_test.tmp", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    char *buf = malloc(1024 * 1024 * 4); // 4 MB

    struct timespec s1, e1, s2, e2;

    // Buffered write to kernel page cache
    clock_gettime(CLOCK_MONOTONIC, &s1);
    write(fd, buf, 1024 * 1024 * 4);
    clock_gettime(CLOCK_MONOTONIC, &e1);

    // Synchronous flush to physical storage
    clock_gettime(CLOCK_MONOTONIC, &s2);
    fsync(fd);
    clock_gettime(CLOCK_MONOTONIC, &e2);

    close(fd);
    unlink("durability_test.tmp");
    free(buf);

    double write_ms = (e1.tv_sec - s1.tv_sec) * 1000.0 + (e1.tv_nsec - s1.tv_nsec) / 1000000.0;
    double fsync_ms = (e2.tv_sec - s2.tv_sec) * 1000.0 + (e2.tv_nsec - s2.tv_nsec) / 1000000.0;

    printf("write() to Page Cache: %.3f ms\n", write_ms);
    printf("fsync() down to Storage: %.3f ms\n", fsync_ms);
    return 0;
}
```

### Solution 5.18: Inode Addressing Capacity
1. **Direct Pointers:** 12 pointers $\times$ 4KB = 48 KB.
2. **Single-Indirect Pointer:** Points to a 4KB block of 32-bit (4-byte) block pointers $\rightarrow 4096 / 4 = 1024$ block pointers.
   Capacity: $1024 \times 4\text{KB} = 4\text{MB}$.
   Total with direct pointers: $4\text{MB} + 48\text{KB} = 4,144\text{ KB}$.
