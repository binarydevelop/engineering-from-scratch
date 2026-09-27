// Symptom: Process crashes abruptly with "Floating point exception (core dumped)".
// Task: Diagnose hardware exception trap in gdb, understand SIGFPE, and validate input to prevent zero division.
#include <stdio.h>
#include <unistd.h>

int compute_rate(int total, int count) {
    // BUG: Division by zero! Triggers hardware arithmetic trap -> kernel sends SIGFPE
    return total / count;
}

int main(void) {
    printf("[Lab 09] Running calculation...\n");
    int rate = compute_rate(100, 0);
    printf("Rate: %d\n", rate);
    return 0;
}
