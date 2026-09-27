// Solution 14: Ensure parent supervises child lifecycle and reaps it before exiting.
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();
    if (pid < 0) return 1;

    if (pid == 0) {
        printf("[Child %d] Running work under supervision of Parent PID: %d...\n", getpid(), getppid());
        usleep(50000);
        printf("[Child %d] Finished task.\n", getpid());
        exit(0);
    } else {
        printf("[Parent %d] Waiting for child %d to finish...\n", getpid(), pid);
        waitpid(pid, NULL, 0); // Fix: Supervised lifecycle
        printf("[Parent %d] Child finished cleanly. Exiting together.\n", getpid());
    }
    return 0;
}
