// Symptom: Application fails with EACCES (Permission denied) during file write.
// Task: Diagnose using 'ls -l', verify mode bits and UID/GID, and configure appropriate permissions.
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>

int main(void) {
    const char *readonly_file = "readonly_target.tmp";
    // Create read-only file
    int fd = open(readonly_file, O_WRONLY | O_CREAT | O_TRUNC, 0444);
    if (fd >= 0) close(fd);

    printf("[Lab 07] Created read-only file (mode 0444).\n");

    // BUG: Attempting write on read-only file without checking permissions
    int bad_fd = open(readonly_file, O_WRONLY);
    if (bad_fd < 0) {
        printf("Syscall open failed: %s (errno: %d)\n", strerror(errno), errno);
        printf("Diagnose with: stat %s\n", readonly_file);
    } else {
        close(bad_fd);
    }

    unlink(readonly_file);
    return 0;
}
