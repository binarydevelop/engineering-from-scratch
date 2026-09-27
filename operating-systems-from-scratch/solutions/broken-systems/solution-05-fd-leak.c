// Solution 05: Consistently close file descriptors after use to preserve kernel table slots.
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main(void) {
    printf("[Solution 05] Descriptor-safe loop (PID: %d)...\n", getpid());

    for (int i = 0; i < 2048; i++) {
        int fd = open("/dev/null", O_RDONLY);
        if (fd < 0) {
            perror("open failed");
            return 1;
        }
        // Fix: Close descriptor immediately after use
        close(fd);
    }

    printf("[Solution 05] Successfully completed 2048 iterations without leaking descriptors.\n");
    return 0;
}
