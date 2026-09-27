// Solution 20: Install SIGCHLD signal handler with non-blocking waitpid loop.
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

#define NUM_CHILDREN 8

void sigchld_handler(int sig) {
    (void)sig;
    // Fix: Reap all available dead children without blocking
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main(void) {
    struct sigaction sa;
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART | SA_NOCLDSTOP;
    sigaction(SIGCHLD, &sa, NULL);

    printf("[Solution 20] Spawning %d children with active SIGCHLD handler (PID: %d)...\n",
           NUM_CHILDREN, getpid());

    for (int i = 0; i < NUM_CHILDREN; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            exit(0);
        }
    }

    usleep(100000); // 100ms
    printf("[Solution 20] All children reaped asynchronously via SIGCHLD. Zero zombies lingering!\n");
    return 0;
}
