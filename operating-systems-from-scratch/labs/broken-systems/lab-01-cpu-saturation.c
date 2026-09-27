// Symptom: Core pegged at 100% CPU utilization. Process is non-responsive to events.
// Task: Diagnose why CPU is pinned, measure with top/pidstat, and fix by adding proper scheduling yields or sleep.
#include <stdio.h>
#include <unistd.h>

int main(void) {
    printf("[Lab 01] Running CPU saturation workload (PID: %d)...\n", getpid());
    printf("Check CPU usage in another terminal with: top -p %d\n", getpid());

    // BUG: Busy-waiting loop without sleep or yield
    volatile long counter = 0;
    while (counter < 2000000000L) {
        counter++;
    }

    printf("[Lab 01] Workload finished.\n");
    return 0;
}
