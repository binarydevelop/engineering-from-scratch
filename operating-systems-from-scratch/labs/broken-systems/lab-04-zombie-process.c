// Symptom: Terminated child processes linger in the process table marked as <defunct> or state 'Z'.
// Task: Identify zombie processes with 'ps aux | grep Z', explain why the kernel cannot free them, and fix with waitpid().
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // Child exits immediately
        printf("[Child %d] Exiting immediately with code 42...\n", getpid());
        exit(42);
    } else {
        // Parent sleeps without calling wait()
        printf("[Parent %d] Spawned child %d.\n", getpid(), pid);
        printf("Check zombie state now: ps aux | grep %d\n", pid);
        sleep(5); // During this window, child is a ZOMBIE
        printf("[Parent %d] Exiting without reaping child.\n", getpid());
    }
    return 0;
}
