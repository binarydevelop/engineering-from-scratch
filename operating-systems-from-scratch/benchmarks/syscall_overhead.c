#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <time.h>

#define ITERATIONS 5000000

__attribute__((noinline))
int userspace_func(int x) {
    return x + 1;
}

int main(void) {
    struct timespec start, end;

    // 1. Measure Userspace Function Calls
    clock_gettime(CLOCK_MONOTONIC, &start);
    volatile int val = 0;
    for (int i = 0; i < ITERATIONS; i++) {
        val = userspace_func(val);
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    long long user_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);
    double user_call_ns = (double)user_ns / ITERATIONS;

    // 2. Measure Kernel System Calls (getpid)
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < ITERATIONS; i++) {
        val = getpid();
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    long long sys_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);
    double sys_call_ns = (double)sys_ns / ITERATIONS;

    printf("================================================================\n");
    printf("System Call vs Userspace Function Call Benchmark\n");
    printf("================================================================\n");
    printf("Iterations:                  %d\n", ITERATIONS);
    printf("Userspace Function Latency:  %.2f ns / call\n", user_call_ns);
    printf("Kernel System Call (getpid): %.2f ns / call\n", sys_call_ns);
    printf("Syscall Overhead Factor:     %.1fx slower\n", sys_call_ns / user_call_ns);
    printf("================================================================\n");
    return 0;
}
