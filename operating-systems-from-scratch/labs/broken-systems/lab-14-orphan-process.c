// Symptom: Child process continues running in background even after launching terminal or parent dies.
// Task: Observe PPID changing to 1 using 'ps -ef', understand orphan reparenting, and use PR_SET_PDEATHSIG or proper parent supervision.
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    pid_t pid = fork();

    if (pid < 0) return 1;

    if (pid == 0) {
        // Child process
        printf("[Child %d] Spawned with Parent PID: %d\n", getpid(), getppid());
        sleep(2); // Wait for parent to die
        printf("[Child %d] Parent exited! New Parent PID: %d (Reparented to init!)\n",
               getpid(), getppid());
        exit(0);
    } else {
        // Parent exits immediately
        printf("[Parent %d] Exiting immediately, abandoning child %d...\n", getpid(), pid);
        exit(0);
    }
}
