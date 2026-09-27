// Symptom: Dozens of defunct child processes accumulate in process table, approaching ulimit -u.
// Task: Observe zombie accumulation in ps, install a SIGCHLD signal handler with waitpid(-1, &status, WNOHANG) to reap automatically.
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define NUM_CHILDREN 8

int main(void) {
    printf("[Lab 20] Spawning %d short-lived children without reaping (PID: %d)...\n",
           NUM_CHILDREN, getpid());

    for (int i = 0; i < NUM_CHILDREN; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            // Child exits immediately
            exit(0);
        }
    }

    printf("Check defunct process accumulation: ps -ef | grep defunct\n");
    sleep(3);
    printf("[Lab 20] Exiting.\n");
    return 0;
}
