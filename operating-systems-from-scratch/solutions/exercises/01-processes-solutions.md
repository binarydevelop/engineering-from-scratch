# Solutions: Track 1 Process Exercises

### Solution 1.1: Process Identity
```c
#include <stdio.h>
#include <unistd.h>

int main(void) {
    printf("PID:  %d\n", getpid());
    printf("PPID: %d\n", getppid());
    printf("UID:  %d\n", getuid());
    printf("GID:  %d\n", getgid());
    return 0;
}
```

### Solution 1.2: Predicting Fork Output
Output:
```text
Child: 15
Parent: 10
```
**Explanation:** `fork()` clones the address space. Although child and parent initially share physical pages via Copy-on-Write (COW), any write operation triggers a page fault that duplicates the physical frame. Changes in child memory do not propagate to the parent.

### Solution 1.3: Binary Fork Tree
* Total processes: $2^2 = 4$ processes.
* Child processes directly owned by the root parent: 2 processes.
Tree:
```text
Parent ──┬── Child 1 ──── Grandchild
         └── Child 2
```

### Solution 1.5: Program Replacement with `execvp`
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();
    if (pid == 0) {
        char *args[] = {"ls", "-la", "/usr", NULL};
        execvp(args[0], args);
        perror("execvp failed");
        _exit(1);
    }
    wait(NULL);
    printf("Child finished.\n");
    return 0;
}
```

### Solution 1.6: Evaluating `waitpid` Exit Status
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();
    if (pid == 0) {
        exit(77);
    }
    int status;
    waitpid(pid, &status, 0);
    if (WIFEXITED(status)) {
        printf("Recovered child exit code: %d\n", WEXITSTATUS(status));
    }
    return 0;
}
```

### Solution 1.9: Safe Zombie Reaping via `SIGCHLD`
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>

void sigchld_handler(int sig) {
    (void)sig;
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main(void) {
    struct sigaction sa;
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART | SA_NOCLDSTOP;
    sigaction(SIGCHLD, &sa, NULL);

    pid_t pid = fork();
    if (pid == 0) exit(0);

    sleep(1);
    printf("Child reaped asynchronously without lingering as zombie.\n");
    return 0;
}
```

### Solution 1.15: Intercepting `SIGINT`
```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void handle_sigint(int sig) {
    (void)sig;
    const char msg[] = "\nSIGINT received; cleaning up and exiting cleanly.\n";
    write(STDOUT_FILENO, msg, sizeof(msg) - 1);
    _exit(0);
}

int main(void) {
    struct sigaction sa;
    sa.sa_handler = handle_sigint;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);

    printf("Daemon running (PID %d). Press Ctrl+C to test graceful shutdown...\n", getpid());
    while (1) pause();
    return 0;
}
```
