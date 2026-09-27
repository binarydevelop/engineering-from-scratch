// Solution 21: Ignore SIGPIPE so write() returns -1 with errno = EPIPE, allowing graceful handling.
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <errno.h>

int main(void) {
    // Fix: Ignore SIGPIPE
    signal(SIGPIPE, SIG_IGN);

    int p[2];
    if (pipe(p) < 0) return 1;
    close(p[0]); // No reader

    printf("[Solution 21] Writing to closed pipe with SIGPIPE ignored...\n");

    char byte = 'Z';
    ssize_t n = write(p[1], &byte, 1);
    if (n < 0 && errno == EPIPE) {
        printf("[Solution 21] Caught EPIPE gracefully without process crash!\n");
    }

    close(p[1]);
    return 0;
}
