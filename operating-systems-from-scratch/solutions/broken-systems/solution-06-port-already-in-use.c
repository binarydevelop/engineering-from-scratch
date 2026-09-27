// Solution 06: Apply SO_REUSEADDR and dynamically bind or properly release listening ports.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 9999

int main(void) {
    int fd = socket(AF_INET, SOCK_STREAM, 0);

    // Fix: Set SO_REUSEADDR so port can be immediately rebound after server restart
    int opt = 1;
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(PORT);

    if (bind(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind failed");
        close(fd);
        return 1;
    }

    listen(fd, 5);
    printf("[Solution 06] Successfully bound to port %d with SO_REUSEADDR enabled.\n", PORT);
    close(fd);
    return 0;
}
