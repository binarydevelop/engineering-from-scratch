# C for Systems Programming: The Minimal Practical Guide

> **Core Philosophy:** In systems programming, C is not an abstract programming language; it is a thin, typed notation directly over processor registers, stack frames, heap pointers, and operating system system calls.

You do not need 10 years of C experience to understand operating systems. You only need to master seven core concepts:
1. **Memory as an Array of Bytes** & Pointers
2. **Stack vs Heap Allocation** (`malloc` and `free`)
3. **Struct Layout and Memory Alignment**
4. **File Descriptors as Integer Handles**
5. **System Calls, Return Codes, and `errno`**
6. **POSIX Threads (`pthreads`) & Mutexes**
7. **POSIX Sockets and Byte Order**

---

## 1. Pointers: Memory Is Just a Giant Byte Array

To the CPU and the kernel, virtual memory is a continuous array of bytes indexed by address from `0x0000000000000000` to `0x7FFFFFFFFFFFFFFF`.

A **pointer** is simply an integer variable that holds the address of a specific byte in this array:

```c
#include <stdio.h>

int main(void) {
    int x = 42;          // 4 bytes allocated on the stack
    int *ptr = &x;       // ptr stores the memory address of x

    printf("Value of x:        %d\n", x);
    printf("Address of x (&x): %p\n", (void *)&x);
    printf("Value stored in ptr: %p\n", (void *)ptr);
    printf("Dereference (*ptr):  %d\n", *ptr);

    *ptr = 100;          // Directly modify the byte contents at that address
    printf("New value of x:    %d\n", x); // prints 100

    return 0;
}
```

### The Three Golden Rules of Pointers:
1. `&x` means: "What is the memory address of `x`?"
2. `*ptr` means: "Go to the address stored in `ptr` and read/write the bytes there."
3. `NULL` (address `0x0`) is intentionally unmapped. Dereferencing it will trigger an immediate hardware exception trapped by the kernel as a **Segmentation Fault** (`SIGSEGV`).

---

## 2. Stack vs Heap Memory

```text
High Addresses  ┌──────────────────────────────┐
                │ Stack (grows downward ↓)     │ Function local variables, return frames
                │                              │ Automatic lifetime
                ├──────────────────────────────┤
                │          ↓        ↑          │
                ├──────────────────────────────┤
                │ Heap (grows upward ↑)        │ Dynamic allocations via malloc()
                │                              │ Manual lifetime, persistent until free()
                ├──────────────────────────────┤
                │ BSS / Data                   │ Global and static variables
                ├──────────────────────────────┤
                │ Text (Code)                  │ Compiled machine instructions (Read-Only)
Low Addresses   └──────────────────────────────┘
```

### Code Example: Stack vs Heap
```c
#include <stdio.h>
#include <stdlib.h>

void stack_example(void) {
    int stack_var = 10; // Freed automatically when function returns
    printf("Stack variable address: %p\n", (void *)&stack_var);
}

void heap_example(void) {
    // Request 1024 bytes from the runtime heap manager (brk/mmap underneath)
    char *buffer = malloc(1024);
    if (buffer == NULL) {
        perror("malloc failed");
        return;
    }
    printf("Heap buffer address:    %p\n", (void *)buffer);
    free(buffer); // Must explicitly return bytes to allocator
}
```

---

## 3. System Calls, Return Codes, and `errno`

Userspace applications cannot directly touch disk heads or network cards. They must request kernel services via **System Calls** (e.g. `open`, `read`, `write`, `close`, `fork`).

By convention in POSIX systems:
* Functions return `0` on success, or a non-negative integer (such as bytes transferred or a file descriptor).
* Functions return `-1` on error and populate the global thread-local integer `errno`.

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main(void) {
    // Attempt to open a non-existent file
    int fd = open("/nonexistent/file.txt", O_RDONLY);
    if (fd == -1) {
        printf("Error code (errno): %d\n", errno);
        printf("Human readable error: %s\n", strerror(errno));
        perror("open failed"); // Convenience wrapper printing to stderr
        return 1;
    }

    close(fd);
    return 0;
}
```

---

## 4. File Descriptors: Integer Indices into the Kernel Table

A **File Descriptor (FD)** is not a pointer, not a struct, and not a file. It is merely a non-negative integer index into your process's private open-file descriptor table maintained inside kernel memory.

Every standard process starts with three descriptors already open:
* `0`: Standard Input (`stdin`)
* `1`: Standard Output (`stdout`)
* `2`: Standard Error (`stderr`)

```c
#include <unistd.h>

int main(void) {
    const char msg[] = "Writing directly to FD 1 (stdout) via write syscall!\n";
    // ssize_t write(int fd, const void *buf, size_t count);
    write(1, msg, sizeof(msg) - 1);
    return 0;
}
```

---

## 5. Process Creation: `fork()`, `execvp()`, and `waitpid()`

A new process is created by cloning the calling process via `fork()`. The child then replaces its code segment with a new executable image via `exec()`. The parent waits for child termination via `waitpid()`.

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    } else if (pid == 0) {
        // --- CHILD PROCESS ---
        printf("[Child] PID = %d. Replacing image with /bin/ls...\n", getpid());
        char *args[] = {"ls", "-l", NULL};
        execvp(args[0], args);
        // If execvp returns, an error occurred
        perror("execvp failed");
        exit(1);
    } else {
        // --- PARENT PROCESS ---
        printf("[Parent] Spawned child with PID = %d. Waiting for exit...\n", pid);
        int status;
        waitpid(pid, &status, 0); // Reaps child, preventing zombie
        if (WIFEXITED(status)) {
            printf("[Parent] Child terminated with exit code %d\n", WEXITSTATUS(status));
        }
    }
    return 0;
}
```

---

## 6. POSIX Threads (`pthreads`) & Mutex Synchronization

Unlike processes, threads share the same virtual address space (heap, globals, open file descriptors), but maintain their own private stack and register states. Because memory is shared, unsynchronized concurrent writes cause **race conditions**, requiring **mutexes**.

```c
#include <stdio.h>
#include <pthread.h>

#define NUM_ITERATIONS 1000000

long counter = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *worker(void *arg) {
    (void)arg;
    for (int i = 0; i < NUM_ITERATIONS; i++) {
        pthread_mutex_lock(&lock);
        counter++; // Protected critical section
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, worker, NULL);
    pthread_create(&t2, NULL, worker, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Final Counter: %ld (Expected: %d)\n", counter, NUM_ITERATIONS * 2);
    pthread_mutex_destroy(&lock);
    return 0;
}
```

---

## 7. POSIX Sockets: Network Endpoints

A socket is an operating system abstraction representing an endpoint for bi-directional communication across a network or between local processes.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main(void) {
    // 1. Create socket file descriptor
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) { perror("socket"); exit(1); }

    // 2. Allow port reuse immediately upon restart
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    // 3. Bind address and port
    struct sockaddr_in address;
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY; // 0.0.0.0
    address.sin_port = htons(8080);       // Host to network short byte-order

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind"); exit(1);
    }

    // 4. Mark as listening
    listen(server_fd, 10);
    printf("Server listening on port 8080 (FD: %d)...\n", server_fd);

    close(server_fd);
    return 0;
}
```

---

## Compilation Flags for Systems Code

Throughout this curriculum, always compile C programs with warnings enabled and strict standard compliance:

```bash
gcc -Wall -Wextra -pedantic -std=c11 -pthread -O2 source.c -o binary
```

* `-Wall -Wextra`: Flags potential bugs, uninitialized variables, and type mismatches.
* `-pedantic`: Strictly verifies ISO C compliance.
* `-pthread`: Links the POSIX threads runtime.
* `-O2`: Enables reasonable optimizations without obscuring debug symbols.
* `-g`: Include during debugging sessions to attach source lines in `gdb`.
