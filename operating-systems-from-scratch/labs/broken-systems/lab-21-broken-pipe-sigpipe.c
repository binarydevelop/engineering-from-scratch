// Symptom: Process mysteriously terminates with exit status 141 (128 + 13 for SIGPIPE) without printing an error.
// Task: Trace with strace to detect EPIPE, understand SIGPIPE default termination, and handle with signal(SIGPIPE, SIG_IGN).
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    int p[2];
    if (pipe(p) < 0) return 1;

    // Close reading end immediately
    close(p[0]);

    printf("[Lab 21] Writing to a pipe with no active reader...\n");

    // BUG: Writing to a pipe with no readers raises SIGPIPE, killing the process!
    char byte = 'Z';
    ssize_t n = write(p[1], &byte, 1);

    printf("[Lab 21] Wrote %zd bytes.\n", n);
    close(p[1]);
    return 0;
}
