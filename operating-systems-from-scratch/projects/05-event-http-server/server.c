#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/select.h>

#define DEFAULT_PORT 8080
#define BUFFER_SIZE 4096
#define MAX_CLIENTS 128

static volatile int running = 1;

void sigint_handler(int sig) {
    (void)sig;
    running = 0;
}

int make_socket_non_blocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) return -1;
    return fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

void handle_http_request(int client_fd) {
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read = read(client_fd, buffer, sizeof(buffer) - 1);
    if (bytes_read <= 0) {
        close(client_fd);
        return;
    }
    buffer[bytes_read] = '\0';

    // Minimal HTTP 1.1 response
    const char *body = "{\"status\": \"ok\", \"server\": \"OS-From-Scratch-Event-HTTP\"}\n";
    char response[BUFFER_SIZE];
    int len = snprintf(response, sizeof(response),
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n"
        "Content-Length: %zu\r\n"
        "Connection: close\r\n"
        "\r\n"
        "%s", strlen(body), body);

    write(client_fd, response, len);
    close(client_fd);
}

// ==============================================================
// Architecture 1: Single-Threaded Sequential Blocking Server
// ==============================================================
void run_sequential_server(int server_fd) {
    printf("[Mode] Running Single-Threaded Sequential Server...\n");
    while (running) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) {
            if (errno == EINTR) break;
            perror("accept");
            continue;
        }
        handle_http_request(client_fd);
    }
}

// ==============================================================
// Architecture 2: Multi-Threaded Worker Pool Server
// ==============================================================
#define QUEUE_SIZE 256
#define THREAD_POOL_SIZE 4

typedef struct {
    int client_fds[QUEUE_SIZE];
    int head;
    int tail;
    int count;
    pthread_mutex_t lock;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} WorkQueue;

static WorkQueue g_queue;

void *worker_thread_func(void *arg) {
    (void)arg;
    while (running) {
        pthread_mutex_lock(&g_queue.lock);
        while (g_queue.count == 0 && running) {
            pthread_cond_wait(&g_queue.not_empty, &g_queue.lock);
        }
        if (!running) {
            pthread_mutex_unlock(&g_queue.lock);
            break;
        }
        int client_fd = g_queue.client_fds[g_queue.head];
        g_queue.head = (g_queue.head + 1) % QUEUE_SIZE;
        g_queue.count--;
        pthread_cond_signal(&g_queue.not_full);
        pthread_mutex_unlock(&g_queue.lock);

        handle_http_request(client_fd);
    }
    return NULL;
}

void run_threaded_pool_server(int server_fd) {
    printf("[Mode] Running Multi-Threaded Server (%d workers)...\n", THREAD_POOL_SIZE);
    pthread_t threads[THREAD_POOL_SIZE];
    g_queue.head = 0;
    g_queue.tail = 0;
    g_queue.count = 0;
    pthread_mutex_init(&g_queue.lock, NULL);
    pthread_cond_init(&g_queue.not_empty, NULL);
    pthread_cond_init(&g_queue.not_full, NULL);

    for (int i = 0; i < THREAD_POOL_SIZE; i++) {
        pthread_create(&threads[i], NULL, worker_thread_func, NULL);
    }

    while (running) {
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) {
            if (errno == EINTR) break;
            perror("accept");
            continue;
        }

        pthread_mutex_lock(&g_queue.lock);
        while (g_queue.count == QUEUE_SIZE && running) {
            pthread_cond_wait(&g_queue.not_full, &g_queue.lock);
        }
        if (!running) {
            pthread_mutex_unlock(&g_queue.lock);
            close(client_fd);
            break;
        }
        g_queue.client_fds[g_queue.tail] = client_fd;
        g_queue.tail = (g_queue.tail + 1) % QUEUE_SIZE;
        g_queue.count++;
        pthread_cond_signal(&g_queue.not_empty);
        pthread_mutex_unlock(&g_queue.lock);
    }

    pthread_cond_broadcast(&g_queue.not_empty);
    for (int i = 0; i < THREAD_POOL_SIZE; i++) {
        pthread_join(threads[i], NULL);
    }
}

// ==============================================================
// Architecture 3: Non-Blocking Event-Driven Server (select / readiness)
// ==============================================================
void run_event_driven_server(int server_fd) {
    printf("[Mode] Running Non-Blocking Event-Driven Server (select readiness)...\n");
    make_socket_non_blocking(server_fd);

    int client_sockets[MAX_CLIENTS];
    for (int i = 0; i < MAX_CLIENTS; i++) client_sockets[i] = 0;

    while (running) {
        fd_set read_fds;
        FD_ZERO(&read_fds);
        FD_SET(server_fd, &read_fds);
        int max_sd = server_fd;

        for (int i = 0; i < MAX_CLIENTS; i++) {
            int sd = client_sockets[i];
            if (sd > 0) FD_SET(sd, &read_fds);
            if (sd > max_sd) max_sd = sd;
        }

        struct timeval timeout;
        timeout.tv_sec = 1;
        timeout.tv_usec = 0;

        int activity = select(max_sd + 1, &read_fds, NULL, NULL, &timeout);
        if (activity < 0 && errno != EINTR) {
            perror("select error");
        }

        // 1. New incoming connection on listening socket
        if (FD_ISSET(server_fd, &read_fds)) {
            struct sockaddr_in client_addr;
            socklen_t client_len = sizeof(client_addr);
            int new_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
            if (new_fd >= 0) {
                make_socket_non_blocking(new_fd);
                int added = 0;
                for (int i = 0; i < MAX_CLIENTS; i++) {
                    if (client_sockets[i] == 0) {
                        client_sockets[i] = new_fd;
                        added = 1;
                        break;
                    }
                }
                if (!added) {
                    close(new_fd); // Max clients reached
                }
            }
        }

        // 2. Client I/O operations
        for (int i = 0; i < MAX_CLIENTS; i++) {
            int sd = client_sockets[i];
            if (sd > 0 && FD_ISSET(sd, &read_fds)) {
                handle_http_request(sd);
                client_sockets[i] = 0;
            }
        }
    }
}

int main(int argc, char **argv) {
    int port = DEFAULT_PORT;
    int mode = 3; // Default: Event-Driven

    if (argc > 1) {
        if (strcmp(argv[1], "--seq") == 0) mode = 1;
        else if (strcmp(argv[1], "--pool") == 0) mode = 2;
        else if (strcmp(argv[1], "--event") == 0) mode = 3;
    }
    if (argc > 2) {
        port = atoi(argv[2]);
    }

    struct sigaction sa;
    sa.sa_handler = sigint_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);

    // Ignore SIGPIPE so writing to disconnected client doesn't crash server
    signal(SIGPIPE, SIG_IGN);

    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) { perror("socket creation"); exit(1); }

    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        close(server_fd);
        exit(1);
    }

    if (listen(server_fd, 128) < 0) {
        perror("listen failed");
        close(server_fd);
        exit(1);
    }

    printf("================================================================\n");
    printf("Capstone 5: High-Performance HTTP Server (Port %d)\n", port);
    printf("================================================================\n");

    if (mode == 1) run_sequential_server(server_fd);
    else if (mode == 2) run_threaded_pool_server(server_fd);
    else run_event_driven_server(server_fd);

    printf("\nGraceful shutdown completed.\n");
    close(server_fd);
    return 0;
}
