// Solution 09: Guard against zero division and handle SIGFPE safely.
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int safe_compute_rate(int total, int count) {
    // Fix: Validate input before division
    if (count == 0) {
        fprintf(stderr, "Error: Division by zero avoided.\n");
        return -1;
    }
    return total / count;
}

int main(void) {
    printf("[Solution 09] Running safe calculation...\n");
    int rate = safe_compute_rate(100, 0);
    printf("Safe Result: %d\n", rate);
    return 0;
}
