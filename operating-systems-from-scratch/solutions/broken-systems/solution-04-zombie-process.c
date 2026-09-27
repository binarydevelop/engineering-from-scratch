// Solution 04: Reap child process termination status using waitpid().
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    } else if (pid == 0) {
        printf("[Child %d] Exiting with code 42...\n", getpid());
        exit(42);
    } else {
        printf("[Parent %d] Waiting for child %d to terminate...\n", getpid(), pid);
        int status;
        waitpid(pid, &status, 0); // Fix: Reaps child, freeing its entry in process table
        if (WIFEXITED(status)) {
            printf("[Parent %d] Successfully reaped child %d (Exit code: %d).\n",
                   getpid(), pid, WEXITSTATUS(status));
        }
    }
    return 0;
}
