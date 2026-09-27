// Symptom: Process becomes permanently stuck. 'strace' shows process blocked inside read() syscall.
// Task: Use 'strace -p <PID>' or 'cat /proc/<PID>/wchan' to detect blocked state, and fix using O_NONBLOCK or select() with timeout.
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

int main(void) {
    int p[2];
    if (pipe(p) < 0) return 1;

    printf("[Lab 11] Process %d waiting on empty pipe without writers...\n", getpid());
    printf("Inspect blocked syscall with: strace -p %d\n", getpid());

    // BUG: Blocking read on pipe when no data exists and write-end is still open
    char buf[128];
    ssize_t n = read(p[0], buf, sizeof(buf)); // BLOCKED INDEFINITELY!

    printf("[Lab 11] Read %zd bytes.\n", n);
    close(p[0]);
    close(p[1]);
    return 0;
}
