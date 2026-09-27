// Solution 01: Relieve CPU saturation by replacing busy loops with event notification or sleep.
#include <stdio.h>
#include <unistd.h>
#include <time.h>

int main(void) {
    printf("[Solution 01] Running CPU-friendly workload (PID: %d)...\n", getpid());

    // Fix: Perform work in chunks and yield CPU or sleep to prevent 100% spin
    for (int i = 0; i < 5; i++) {
        printf("Working tick %d/5...\n", i + 1);
        struct timespec ts = {0, 100000000L}; // 100 ms sleep
        nanosleep(&ts, NULL);
    }

    printf("[Solution 01] Finished with near 0%% CPU waste.\n");
    return 0;
}
