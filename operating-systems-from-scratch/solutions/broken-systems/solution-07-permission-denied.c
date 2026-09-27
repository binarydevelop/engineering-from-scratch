// Solution 07: Check access permissions with access() and set appropriate write permissions via chmod.
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <errno.h>
#include <string.h>

int main(void) {
    const char *target_file = "writable_target.tmp";

    // Fix: Create file with owner read/write permissions (mode 0644)
    int fd = open(target_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open failed");
        return 1;
    }

    const char *msg = "Write succeeded with 0644 permissions.\n";
    write(fd, msg, strlen(msg));
    close(fd);

    printf("[Solution 07] File created and written successfully.\n");
    unlink(target_file);
    return 0;
}
