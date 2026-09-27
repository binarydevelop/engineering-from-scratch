#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>

#define ITERATIONS 25000

/*
 * Measures context switch latency between two processes communicating via pipes.
 * A 2-way pipe roundtrip forces 2 context switches per iteration.
 */
int main(void) {
    int p1[2], p2[2];
    if (pipe(p1) < 0 || pipe(p2) < 0) {
        perror("pipe");
        return 1;
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork");
        return 1;
    }

    if (pid == 0) {
        // Child: read from p1, write to p2
        close(p1[1]);
        close(p2[0]);
        char token;
        for (int i = 0; i < ITERATIONS; i++) {
            if (read(p1[0], &token, 1) != 1) break;
            if (write(p2[1], &token, 1) != 1) break;
        }
        close(p1[0]);
        close(p2[1]);
        exit(0);
    } else {
        // Parent: write to p1, read from p2
        close(p1[0]);
        close(p2[1]);

        char token = 'x';
        struct timespec start, end;
        clock_gettime(CLOCK_MONOTONIC, &start);

        for (int i = 0; i < ITERATIONS; i++) {
            if (write(p1[1], &token, 1) != 1) break;
            if (read(p2[0], &token, 1) != 1) break;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);
        wait(NULL);

        close(p1[1]);
        close(p2[0]);

        long long total_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);
        // Each iteration consists of 2 context switches: Parent -> Child -> Parent
        double ns_per_switch = (double)total_ns / (ITERATIONS * 2);

        printf("================================================================\n");
        printf("Process Context Switch Benchmark (Pipe Roundtrip)\n");
        printf("================================================================\n");
        printf("Iterations:                 %d (Total switches: %d)\n", ITERATIONS, ITERATIONS * 2);
        printf("Total Time Elapsed:         %.3f ms\n", total_ns / 1000000.0);
        printf("Estimated Latency / Switch: %.2f ns (%.3f µs)\n", ns_per_switch, ns_per_switch / 1000.0);
        printf("================================================================\n");
    }
    return 0;
}
