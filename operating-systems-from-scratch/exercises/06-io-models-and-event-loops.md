# Track 6: I/O Models, Event Loops & Multiplexing Exercises

> **Motto:** The C10K problem is not a CPU bottleneck; it is an operating system synchronization and readiness notification problem.

All solutions are located in `solutions/exercises/06-io-models-and-event-loops-solutions.md`.

---

### Exercise 6.1: The Blocking I/O Bottleneck
Write a TCP server in C that processes one client at a time using blocking `accept()`, `read()`, and `write()`. Launch two client connections. Show that Client 2 is forced to wait indefinitely in the kernel listen queue while Client 1 stays connected.

### Exercise 6.2: Non-Blocking File Descriptors (`O_NONBLOCK`)
Set a socket or pipe to non-blocking mode using `fcntl(fd, F_SETFL, O_NONBLOCK)`. Attempt to `read()` when no data is present. Verify that `read()` returns `-1` immediately and sets `errno = EAGAIN` or `EWOULDBLOCK`.

### Exercise 6.3: I/O Multiplexing with `select()`
Implement an echo server supporting up to 10 concurrent clients on a single thread using `select()`. Manage an `fd_set` of active descriptors and process only those ready for reading.

### Exercise 6.4: The Linear Scan Limitation of `select()`
Explain why `select()` has $O(N)$ algorithmic complexity where $N$ is the highest file descriptor number (`max_fd`). How does `FD_SETSIZE` (typically 1024) limit scalability?

### Exercise 6.5: I/O Multiplexing with `poll()`
Rewrite the `select()` server using `poll()` and an array of `struct pollfd`. Demonstrate how `poll()` removes the rigid `FD_SETSIZE = 1024` ceiling while retaining $O(N)$ linear scans.

### Exercise 6.6: Linux Scalable Event Notification (`epoll`)
On Linux, implement an echo server using `epoll_create1()`, `epoll_ctl()`, and `epoll_wait()`. Explain why `epoll` achieves $O(1)$ readiness notification regardless of total connection count.

### Exercise 6.7: Level-Triggered (LT) vs Edge-Triggered (ET) Modes
In `epoll`, what is the difference between level-triggered (default) and edge-triggered (`EPOLLET`) notifications? Write an edge-triggered server that drains the read buffer in a `while (1)` loop until `EAGAIN` to prevent starving incoming bytes.

### Exercise 6.8: Building a Minimal Event Loop
In Python, implement a lightweight event loop using the `selectors` module (`selectors.DefaultSelector`). Register callbacks for read readiness on sockets and implement an asynchronous chat server.

### Exercise 6.9: Comparing Server Architectures
Benchmark three server architectures under 100 concurrent clients:
1. Architecture A: Sequential Blocking
2. Architecture B: Thread-per-connection (`pthread_create`)
3. Architecture C: Event-driven non-blocking (`select`/`epoll`)
Measure memory footprint and throughput (requests/sec).

### Exercise 6.10: Self-Pipe Trick for Signal Handling in Event Loops
In an event-driven server, how can an asynchronous signal (like `SIGTERM`) safely wake up a sleeping `select()` or `poll()` call? Implement the classic **self-pipe trick**: create a `pipe()`, write a single byte inside the signal handler, and monitor the pipe's read descriptor in the event loop.

### Exercise 6.11: Starvation in Level-Triggered Event Loops
Show what happens when one active client sends an endless stream of bytes in a single-threaded event loop. How do production event loops (e.g. Node.js, Nginx) enforce fair read limits per iteration?

### Exercise 6.12: BSD `kqueue` vs Linux `epoll`
Research and document the conceptual differences between Linux `epoll` and BSD/macOS `kqueue`. How does `kqueue` generalize event notification across files, sockets, signals, and process death?

### Exercise 6.13: Event Loop with Non-Blocking File I/O Trap
Explain why standard disk files cannot be multiplexed with `select()` or `epoll` on Linux (they always report ready!). How do modern runtimes handle disk I/O asynchronously (thread pools vs Linux `io_uring`)?

### Exercise 6.14: Introduction to Linux `io_uring`
Explain the architecture of Linux `io_uring`: two shared ring buffers (Submission Queue and Completion Queue) eliminating syscall overhead during high-throughput I/O.

### Exercise 6.15: Graceful Event-Driven Server Shutdown
Implement a clean shutdown sequence in an event-driven server: upon receiving `SIGINT`, stop accepting new connections on the listening socket, flush pending writes to active clients, close all descriptors, and terminate cleanly.
