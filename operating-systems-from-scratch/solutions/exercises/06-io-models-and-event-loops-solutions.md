# Solutions: Track 6 I/O Models & Event Loops Exercises

### Solution 6.2: Non-Blocking File Descriptors
```c
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

int main(void) {
    int p[2];
    if (pipe(p) < 0) return 1;

    // Set read end to non-blocking
    int flags = fcntl(p[0], F_GETFL, 0);
    fcntl(p[0], F_SETFL, flags | O_NONBLOCK);

    char buf[32];
    ssize_t n = read(p[0], buf, sizeof(buf));
    if (n < 0) {
        if (errno == EAGAIN || errno == EWOULDBLOCK) {
            printf("Non-blocking read returned immediately with EAGAIN/EWOULDBLOCK!\n");
        } else {
            perror("read");
        }
    }
    close(p[0]);
    close(p[1]);
    return 0;
}
```

### Solution 6.3: Multiplexing with `select()`
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/select.h>

int main(void) {
    fd_set read_fds;
    FD_ZERO(&read_fds);
    FD_SET(STDIN_FILENO, &read_fds);

    struct timeval tv = {2, 0}; // 2-second timeout
    printf("Type something within 2 seconds...\n");

    int ready = select(STDIN_FILENO + 1, &read_fds, NULL, NULL, &tv);
    if (ready == 0) {
        printf("Timed out! No input detected.\n");
    } else if (ready > 0 && FD_ISSET(STDIN_FILENO, &read_fds)) {
        char buf[64];
        fgets(buf, sizeof(buf), stdin);
        printf("Received: %s", buf);
    }
    return 0;
}
```

### Solution 6.10: The Self-Pipe Trick
```c
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <sys/select.h>

static int self_pipe[2];

void sig_handler(int sig) {
    (void)sig;
    char token = 'X';
    // Async-signal-safe write
    write(self_pipe[1], &token, 1);
}

int main(void) {
    pipe(self_pipe);
    signal(SIGINT, sig_handler);

    fd_set rfds;
    FD_ZERO(&rfds);
    FD_SET(self_pipe[0], &rfds);

    printf("Waiting for event or Ctrl+C (PID: %d)...\n", getpid());
    select(self_pipe[0] + 1, &rfds, NULL, NULL, NULL);

    printf("Woken up cleanly by signal via self-pipe!\n");
    close(self_pipe[0]);
    close(self_pipe[1]);
    return 0;
}
```
