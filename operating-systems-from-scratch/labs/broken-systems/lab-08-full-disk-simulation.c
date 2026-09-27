// Symptom: File corruption or silent truncation during large write operations.
// Task: Diagnose why blind write() calls cause data loss, and implement a robust full-write loop that checks return values.
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

int main(void) {
    const char *path = "partial_write.tmp";
    int fd = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) return 1;

    char large_buf[1024 * 64];
    memset(large_buf, 'X', sizeof(large_buf));

    // BUG: Blind write call! write() is NOT guaranteed to write all bytes in one syscall.
    // If interrupted by signal or buffer full, it returns fewer bytes or -1.
    ssize_t written = write(fd, large_buf, sizeof(large_buf));
    printf("[Lab 08] Attempted %zu bytes, wrote %zd bytes.\n", sizeof(large_buf), written);

    close(fd);
    unlink(path);
    return 0;
}
