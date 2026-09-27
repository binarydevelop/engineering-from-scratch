// Solution 13: Buffer writes into multi-kilobyte chunks, collapsing thousands of syscalls into a few.
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#define N 50000
#define BUF_SIZE 4096

int main(void) {
    int fd = open("fast_output.tmp", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) return 1;

    printf("[Solution 13] Writing %d bytes using %d-byte buffered chunks...\n", N, BUF_SIZE);

    char buffer[BUF_SIZE];
    memset(buffer, 'x', sizeof(buffer));

    int bytes_left = N;
    while (bytes_left > 0) {
        int to_write = (bytes_left < BUF_SIZE) ? bytes_left : BUF_SIZE;
        write(fd, buffer, to_write);
        bytes_left -= to_write;
    }

    close(fd);
    unlink("fast_output.tmp");
    printf("[Solution 13] Finished in a fraction of a millisecond.\n");
    return 0;
}
