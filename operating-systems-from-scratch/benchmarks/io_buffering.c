#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>

#define TOTAL_BYTES (512 * 1024) // 512 KB
#define BLOCK_SIZE 4096

int main(void) {
    struct timespec start, end;
    const char *tmp_file = "io_bench_tmp.bin";

    // 1. Unbuffered: 1 byte per write() syscall
    int fd1 = open(tmp_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd1 < 0) { perror("open"); return 1; }

    clock_gettime(CLOCK_MONOTONIC, &start);
    char byte_val = 'A';
    for (int i = 0; i < TOTAL_BYTES; i++) {
        if (write(fd1, &byte_val, 1) != 1) { perror("write"); break; }
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    close(fd1);
    long long unbuf_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);

    // 2. Block-buffered: 4096 bytes per write() syscall
    int fd2 = open(tmp_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd2 < 0) { perror("open"); return 1; }

    char block[BLOCK_SIZE];
    for (int i = 0; i < BLOCK_SIZE; i++) block[i] = 'B';

    clock_gettime(CLOCK_MONOTONIC, &start);
    int blocks = TOTAL_BYTES / BLOCK_SIZE;
    for (int i = 0; i < blocks; i++) {
        if (write(fd2, block, BLOCK_SIZE) != BLOCK_SIZE) { perror("write"); break; }
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    close(fd2);
    unlink(tmp_file); // cleanup
    long long buf_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);

    printf("================================================================\n");
    printf("I/O Buffering Benchmark (Total Payload: %d KB)\n", TOTAL_BYTES / 1024);
    printf("================================================================\n");
    printf("Unbuffered (1 byte/write, %d syscalls):   %.3f ms\n", TOTAL_BYTES, unbuf_ns / 1000000.0);
    printf("Block Buffered (4KB/write, %d syscalls):   %.3f ms\n", blocks, buf_ns / 1000000.0);
    printf("Speedup with Buffering:                    %.1fx faster!\n", (double)unbuf_ns / (buf_ns > 0 ? buf_ns : 1));
    printf("================================================================\n");
    return 0;
}
