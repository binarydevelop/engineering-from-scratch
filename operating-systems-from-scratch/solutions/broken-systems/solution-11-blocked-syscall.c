// Solution 11: Configure O_NONBLOCK or select() with timeout to avoid unbounded blocking.
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

int main(void) {
    int p[2];
    if (pipe(p) < 0) return 1;

    // Fix: Make read-end non-blocking
    int flags = fcntl(p[0], F_GETFL, 0);
    fcntl(p[0], F_SETFL, flags | O_NONBLOCK);

    char buf[128];
    ssize_t n = read(p[0], buf, sizeof(buf));
    if (n < 0) {
        if (errno == EAGAIN || errno == EWOULDBLOCK) {
            printf("[Solution 11] Non-blocking read returned EAGAIN as expected (no data available, avoided hang!)\n");
        } else {
            perror("read");
        }
    }

    close(p[0]);
    close(p[1]);
    return 0;
}
