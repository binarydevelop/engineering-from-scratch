// Symptom: Application crashes with EMFILE (Too many open files). No more files or sockets can be opened.
// Task: Trace open descriptors with 'lsof -p <PID>' or 'ls -l /proc/<PID>/fd', identify the missing close(), and fix.
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main(void) {
    printf("[Lab 05] File Descriptor Leak Demonstration (PID: %d)...\n", getpid());

    for (int i = 0; i < 2048; i++) {
        int fd = open("/dev/null", O_RDONLY);
        if (fd < 0) {
            printf("CRASH at iteration %d: %s (errno: %d)\n", i, strerror(errno), errno);
            printf("Hit descriptor limit! Check with: ulimit -n\n");
            return 1;
        }
        // BUG: close(fd) is missing! Descriptors leak until table is exhausted.
    }

    printf("[Lab 05] Finished.\n");
    return 0;
}
