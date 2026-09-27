// Symptom: File writing throughput is 1000x slower than normal, CPU spends 95% of time in kernel space (sy).
// Task: Use 'strace -c' or '/usr/bin/time -v' to measure syscall count, and implement userspace buffering.
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

#define N 50000

int main(void) {
    int fd = open("slow_output.tmp", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) return 1;

    printf("[Lab 13] Writing %d bytes using 1-byte raw write() syscalls...\n", N);
    // BUG: 50,000 individual system calls to write 50 KB!
    for (int i = 0; i < N; i++) {
        char c = 'x';
        write(fd, &c, 1);
    }

    close(fd);
    unlink("slow_output.tmp");
    printf("[Lab 13] Finished.\n");
    return 0;
}
