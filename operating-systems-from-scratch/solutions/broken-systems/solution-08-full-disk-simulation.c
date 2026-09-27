// Solution 08: Implement reliable write_all loop handling partial writes and ENOSPC.
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>

ssize_t write_all(int fd, const void *buf, size_t count) {
    size_t bytes_written = 0;
    const char *ptr = (const char *)buf;

    while (bytes_written < count) {
        ssize_t res = write(fd, ptr + bytes_written, count - bytes_written);
        if (res < 0) {
            if (errno == EINTR) continue; // Retry if interrupted by signal
            return -1; // Genuine error (e.g. ENOSPC)
        }
        if (res == 0) break;
        bytes_written += res;
    }
    return bytes_written;
}

int main(void) {
    const char *path = "safe_write.tmp";
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) return 1;

    char large_buf[1024 * 64];
    memset(large_buf, 'X', sizeof(large_buf));

    // Fix: Use robust write loop
    ssize_t res = write_all(fd, large_buf, sizeof(large_buf));
    if (res < 0) {
        perror("write_all failed");
    } else {
        printf("[Solution 08] Successfully and completely wrote %zd bytes.\n", res);
    }

    close(fd);
    unlink(path);
    return 0;
}
