# Track 2: Threads & Concurrency Exercises

> **Motto:** Concurrency is not parallelism. Parallelism is doing multiple things at the same physical instant; concurrency is managing the structure of multiple executing paths.

All solutions are located in `solutions/exercises/02-threads-concurrency-solutions.md`.

---

### Exercise 2.1: Basic Thread Creation & Join
Write a C program using `pthread_create()` that spawns 4 worker threads. Pass each thread its integer index $(0, 1, 2, 3)$ via pointer arguments. Use `pthread_join()` to wait for all 4 to finish.

### Exercise 2.2: Memory Sharing Between Threads
Demonstrate that threads share heap and global variables: write a program where Thread 1 updates a global array and allocates a struct on the heap, and Thread 2 reads those exact values after a synchronization barrier or join.

### Exercise 2.3: Private Stack Isolation
Prove that threads have private stacks: declare a local variable inside each thread function, print its address, and verify that the stack addresses are separated by approximately the thread stack size (typically 8MB or 2MB).

### Exercise 2.4: Measuring Thread Creation Overhead
Benchmark the time required to spawn and join 1,000 POSIX threads. Compare with the time required to fork and reap 1,000 processes. Explain why thread creation is faster.

### Exercise 2.5: The Classic Race Condition
Write a program with a global counter initialized to 0. Spawn 10 threads, each performing `for (int i=0; i<100000; i++) counter++;`. Run the program and observe the non-deterministic output below 1,000,000.

### Exercise 2.6: Dissecting Non-Atomicity in Assembly
Compile a single `counter++` line to assembly using `gcc -S -O0`. Identify the 3 discrete CPU instructions:
1. `mov [addr], %eax` (Load)
2. `add $1, %eax` (Modify)
3. `mov %eax, [addr]` (Store)
Draw an execution interleaving showing how two concurrent threads both read 0 and both write 1, losing an update.

### Exercise 2.7: Mutex Protection
Fix Exercise 2.5 by wrapping the increment in `pthread_mutex_lock(&lock)` and `pthread_mutex_unlock(&lock)`. Verify that the final counter matches 1,000,000 exactly across 100 consecutive runs.

### Exercise 2.8: Mutex Overhead Measurement
Measure the execution time of 10,000,000 increments in a single thread:
1. Without a mutex
2. With an uncontended mutex lock/unlock per increment
Calculate the nanosecond cost of a modern uncontended lock (e.g. futex in user space).

### Exercise 2.9: Non-blocking Mutex Trylock
Write a worker thread that uses `pthread_mutex_trylock()`. If the lock is held, it increments a `busy_spins` counter and does background work before trying again.

### Exercise 2.10: Deadlock Reproduction
Write a program with two mutexes (`lock_X`, `lock_Y`) and two threads. Thread A acquires X then Y; Thread B acquires Y then X. Add a `usleep(1000)` between the locks to guarantee a deadlock hang.

### Exercise 2.11: Deadlock Prevention via Total Lock Ordering
Fix Exercise 2.10 by assigning unique integer IDs to each mutex and enforcing the rule: *Always acquire locks in strictly increasing order of their ID*.

### Exercise 2.12: Recursive Mutexes
Configure a mutex with `PTHREAD_MUTEX_RECURSIVE` using `pthread_mutexattr_settype()`. Demonstrate that a thread can recursively lock the same mutex multiple times without self-deadlocking.

### Exercise 2.13: C11 Atomics vs Mutexes
Rewrite the concurrent counter using C11 `<stdatomic.h>` and `atomic_fetch_add()`. Compare the throughput of hardware atomic instructions vs pthread mutexes.

### Exercise 2.14: Thread Return Values
Use `pthread_exit()` in a worker to return a dynamically allocated result struct. Retrieve and free this struct in the parent thread via the second argument of `pthread_join()`.

### Exercise 2.15: Thread Detachment
Use `pthread_detach()` on a long-running background worker thread. Explain why calling `pthread_join()` on a detached thread fails with `EINVAL`, and verify that detached threads automatically free their resources upon exit.

### Exercise 2.16: Thread-Specific Data (`pthread_key_create`)
Create a thread-local storage key using `pthread_key_create()`. Set a unique identifier for each thread with `pthread_setspecific()`, and read it from deep nested helper functions with `pthread_getspecific()`.

### Exercise 2.17: Thread Cancellation
Spawn a worker executing an infinite loop. Use `pthread_cancel()` from the main thread to terminate it. Configure cancellation points using `pthread_testcancel()`.

### Exercise 2.18: False Sharing Demonstration
Allocate an array of 4 integers. Have 4 threads increment their own distinct array index $0, 1, 2, 3$ concurrently 100,000,000 times. Observe slowdown due to cache-line bouncing. Pad each integer with 64 bytes and measure the speedup!

### Exercise 2.19: Lock Contention Profiling
Write a benchmark where $N$ threads compete for a single mutex. Plot execution time as $N$ scales from 1 to 16 cores. Identify the point of diminishing returns.

### Exercise 2.20: Building a Spinlock
Implement a user-space spinlock using atomic test-and-set:
`while (__atomic_test_and_set(&lock, __ATOMIC_ACQUIRE)) { /* spin */ }`
Compare CPU consumption between a spinlock and a sleeping `pthread_mutex_t`.
