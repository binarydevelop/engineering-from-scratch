/*
 * socket-programs/c/udp_echo_server.c
 * POSIX C UDP Echo Server.
 * Demonstrates: socket(AF_INET, SOCK_DGRAM), bind(), recvfrom(), sendto()
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 9999
#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    int sock_fd;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in servaddr, cliaddr;
    int port = (argc > 1) ? atoi(argv[1]) : PORT;

    if ((sock_fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));

    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);

    if (bind(sock_fd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        perror("bind failed");
        close(sock_fd);
        exit(EXIT_FAILURE);
    }

    printf("C UDP Echo Server listening on 0.0.0.0:%d\n", port);

    while (1) {
        socklen_t len = sizeof(cliaddr);
        ssize_t n = recvfrom(sock_fd, (char *)buffer, BUFFER_SIZE - 1, 0,
                             (struct sockaddr *)&cliaddr, &len);
        if (n > 0) {
            buffer[n] = '\0';
            char client_ip[INET_ADDRSTRLEN];
            inet_ntop(AF_INET, &cliaddr.sin_addr, client_ip, sizeof(client_ip));
            printf("Received %zd bytes from %s:%d: %s\n", n, client_ip, ntohs(cliaddr.sin_port), buffer);

            sendto(sock_fd, (const char *)buffer, n, 0,
                   (const struct sockaddr *)&cliaddr, len);
        }
    }

    close(sock_fd);
    return 0;
}
