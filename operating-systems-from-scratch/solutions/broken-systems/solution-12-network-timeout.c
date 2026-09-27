// Solution 12: Configure non-blocking connect with select() timeout to fail fast on unreachable hosts.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <fcntl.h>
#include <errno.h>

int main(void) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);

    // Fix: Make socket non-blocking for connect timeout
    int flags = fcntl(sock, F_GETFL, 0);
    fcntl(sock, F_SETFL, flags | O_NONBLOCK);

    struct sockaddr_in target;
    memset(&target, 0, sizeof(target));
    target.sin_family = AF_INET;
    inet_pton(AF_INET, "192.0.2.1", &target.sin_addr);
    target.sin_port = htons(81);

    printf("[Solution 12] Initiating non-blocking connect with 100ms select timeout...\n");
    int res = connect(sock, (struct sockaddr *)&target, sizeof(target));
    if (res < 0 && errno == EINPROGRESS) {
        fd_set wfds;
        FD_ZERO(&wfds);
        FD_SET(sock, &wfds);
        struct timeval tv = {0, 100000}; // 100 ms

        int ready = select(sock + 1, NULL, &wfds, NULL, &tv);
        if (ready == 0) {
            printf("[Solution 12] Connection timed out after 100ms (prevented 120s kernel hang!)\n");
        } else if (ready > 0) {
            int err = 0;
            socklen_t len = sizeof(err);
            getsockopt(sock, SOL_SOCKET, SO_ERROR, &err, &len);
            printf("[Solution 12] Connection failed with error: %s\n", strerror(err));
        }
    }

    close(sock);
    return 0;
}
