# Track 3: Synchronization Primitives & Coordination Exercises

> **Motto:** A lock guarantees safety (nothing bad happens); a condition variable guarantees liveness (something good eventually happens).

All solutions are located in `solutions/exercises/03-synchronization-primitives-solutions.md`.

---

### Exercise 3.1: Counting Semaphore Resource Pool
Use POSIX semaphores (`sem_init`, `sem_wait`, `sem_post`) to model a pool of 3 database connection slots shared among 10 worker threads. Prove that no more than 3 threads can enter the critical section simultaneously.

### Exercise 3.2: Binary Semaphore as Mutex
Demonstrate that a semaphore initialized to 1 behaves identically to a mutual exclusion lock. Compare the performance between `sem_t` and `pthread_mutex_t`.

### Exercise 3.3: Condition Variable: Basic Wait and Signal
Write a program with two threads: a worker thread that waits for an `is_ready` boolean to become true, and a main thread that computes data, sets `is_ready = 1`, and signals the worker via `pthread_cond_signal()`.

### Exercise 3.4: The Spurious Wakeup Trap
Explain why condition variables must always be waited on inside a `while (!condition)` loop rather than an `if (!condition)` statement. Write a scenario where a spurious wakeup or racing consumer corrupts program state if `if` is used.

### Exercise 3.5: Bounded Producer-Consumer Queue (Single Item)
Implement a 1-item buffer using a mutex and two condition variables: `cond_empty` and `cond_full`. A producer thread deposits integers, and a consumer thread consumes them without busy-waiting.

### Exercise 3.6: Bounded FIFO Queue (Multi-Item Array)
Extend Exercise 3.5 to a circular array of size $K=8$. Ensure multiple concurrent producers and consumers correctly enqueue and dequeue items without data corruption or deadlocks.

### Exercise 3.7: `pthread_cond_broadcast`
Demonstrate `pthread_cond_broadcast()` by having 5 worker threads wait on a "race start" condition. When the main thread calls `broadcast()`, all 5 workers wake up simultaneously and begin execution.

### Exercise 3.8: Reader-Writer Lock (`pthread_rwlock_t`)
Implement a concurrent cache where 10 reader threads frequently read a data structure without blocking each other, while 1 writer thread periodically acquires an exclusive write lock. Compare throughput with a standard `pthread_mutex_t`.

### Exercise 3.9: Reader Starvation vs Writer Starvation
In a reader-writer lock, if readers arrive continuously, a writer may starve indefinitely. Write a test case demonstrating this behavior, and explain how writer-preference reader-writer locks resolve it.

### Exercise 3.10: Synchronization Barriers (`pthread_barrier_t`)
Use `pthread_barrier_init()` to coordinate 4 threads performing a multi-phase parallel computation. Ensure that all threads finish Phase 1 before any thread begins Phase 2.

### Exercise 3.11: Thread Rendezvous
Implement a 2-thread rendezvous using two counting semaphores: Thread A and Thread B must arrive at a designated point in code before either is allowed to proceed.

### Exercise 3.12: The Dining Philosophers Problem
Model 5 philosophers and 5 chopsticks. Demonstrate the classic deadlock where each philosopher picks up their left chopstick simultaneously. Fix the deadlock using an asymmetric philosopher rule (one philosopher picks up right first).

### Exercise 3.13: The Sleeping Barber Problem
Model a barber shop with 1 barber chair and 3 waiting chairs using semaphores and mutexes. If no customers exist, the barber sleeps; if a customer arrives and a chair is free, the barber wakes up; if all chairs are occupied, the customer leaves.

### Exercise 3.14: The Reader-Writer Problem with Mutexes & Condition Variables
Reconstruct the entire logic of `pthread_rwlock_t` from scratch using only a standard `pthread_mutex_t` and `pthread_cond_t`, tracking `active_readers`, `waiting_writers`, and `active_writers`.

### Exercise 3.15: Timed Condition Wait (`pthread_cond_timedwait`)
Use `pthread_cond_timedwait()` with `clock_gettime(CLOCK_REALTIME)` to implement a worker that waits for a task with a 500 ms timeout. If no task arrives, handle the `ETIMEDOUT` return code gracefully.

### Exercise 3.16: Event Notification / Wait Queue
Implement a reusable `Event` synchronization object with `event_set()`, `event_reset()`, and `event_wait()`, mimicking Python's `threading.Event`.

### Exercise 3.17: Multi-Threaded Barrier from Scratch
Build your own `barrier_t` struct using only a mutex, an integer counter, and a condition variable, without using `pthread_barrier_t`.

### Exercise 3.18: Token Bucket Rate Limiter
Implement a thread-safe token bucket rate limiter: a background thread generates 10 tokens per second, while worker threads call `consume_token()` which blocks on a condition variable if the bucket is empty.

### Exercise 3.19: Lock-Free Stack (Treiber Stack)
Implement a simple lock-free stack using `atomic_compare_exchange_weak()` to push and pop nodes from a singly linked list without any mutex.

### Exercise 3.20: Thread Pool Work Dispatcher
Implement a minimal thread pool with 4 persistent workers that continuously consume `Task` structs (function pointer + argument pointer) from a thread-safe task queue.
