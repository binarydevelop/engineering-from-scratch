# Solutions: Track 7 Networking & Sockets Exercises

### Solution 7.1: TCP Echo Server
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main(void) {
    int sfd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK); // 127.0.0.1
    addr.sin_port = htons(8080);

    bind(sfd, (struct sockaddr *)&addr, sizeof(addr));
    listen(sfd, 10);
    printf("Echo server listening on 127.0.0.1:8080...\n");

    int cfd = accept(sfd, NULL, NULL);
    char buf[128];
    ssize_t n = read(cfd, buf, sizeof(buf));
    if (n > 0) {
        write(cfd, buf, n); // Echo back
    }
    close(cfd);
    close(sfd);
    return 0;
}
```

### Solution 7.3: Network Byte Order
```c
#include <stdio.h>
#include <arpa/inet.h>

int main(void) {
    uint16_t host_port = 8080; // 0x1F90
    uint16_t net_port = htons(host_port);

    uint8_t *h_bytes = (uint8_t *)&host_port;
    uint8_t *n_bytes = (uint8_t *)&net_port;

    printf("Host Port:    %d (0x%04X) -> Bytes in memory: %02X %02X (Little-Endian)\n",
           host_port, host_port, h_bytes[0], h_bytes[1]);
    printf("Network Port: %d (0x%04X) -> Bytes in memory: %02X %02X (Big-Endian)\n",
           net_port, net_port, n_bytes[0], n_bytes[1]);
    return 0;
}
```

### Solution 7.6: UNIX Domain Sockets
```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

int main(void) {
    const char *sock_path = "/tmp/test_uds.sock";
    unlink(sock_path);

    int sfd = socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, sock_path, sizeof(addr.sun_path) - 1);

    bind(sfd, (struct sockaddr *)&addr, sizeof(addr));
    listen(sfd, 5);
    printf("UNIX Domain Socket bound to path: %s\n", sock_path);

    close(sfd);
    unlink(sock_path);
    return 0;
}
```
