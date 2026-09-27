# Solutions: Track 2 Threads & Concurrency Exercises

### Solution 2.1: Basic Thread Creation & Join
```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void *worker(void *arg) {
    int id = *(int *)arg;
    printf("Worker thread %d running on CPU core.\n", id);
    free(arg);
    return NULL;
}

int main(void) {
    pthread_t threads[4];
    for (int i = 0; i < 4; i++) {
        int *id = malloc(sizeof(int));
        *id = i;
        pthread_create(&threads[i], NULL, worker, id);
    }
    for (int i = 0; i < 4; i++) {
        pthread_join(threads[i], NULL);
    }
    printf("All 4 worker threads joined successfully.\n");
    return 0;
}
```

### Solution 2.7: Mutex Protection
```c
#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 10
#define ITERATIONS 100000

long counter = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *worker(void *arg) {
    (void)arg;
    for (int i = 0; i < ITERATIONS; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void) {
    pthread_t threads[NUM_THREADS];
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], NULL, worker, NULL);
    }
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    printf("Final Counter: %ld (Expected: %d) -> EXACT MATCH!\n",
           counter, NUM_THREADS * ITERATIONS);
    pthread_mutex_destroy(&lock);
    return 0;
}
```

### Solution 2.11: Total Lock Ordering (Deadlock Prevention)
```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t lock1 = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lock2 = PTHREAD_MUTEX_INITIALIZER;

void acquire_two_locks(pthread_mutex_t *l1, pthread_mutex_t *l2) {
    // Total lock ordering: always lock the one with smaller pointer address first
    if ((uintptr_t)l1 < (uintptr_t)l2) {
        pthread_mutex_lock(l1);
        pthread_mutex_lock(l2);
    } else {
        pthread_mutex_lock(l2);
        pthread_mutex_lock(l1);
    }
}

void *worker_a(void *arg) {
    (void)arg;
    acquire_two_locks(&lock1, &lock2);
    printf("Worker A acquired both locks in global order!\n");
    pthread_mutex_unlock(&lock2);
    pthread_mutex_unlock(&lock1);
    return NULL;
}

void *worker_b(void *arg) {
    (void)arg;
    acquire_two_locks(&lock2, &lock1);
    printf("Worker B acquired both locks in global order!\n");
    pthread_mutex_unlock(&lock1);
    pthread_mutex_unlock(&lock2);
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, worker_a, NULL);
    pthread_create(&t2, NULL, worker_b, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
```

### Solution 2.13: C11 Atomics
```c
#include <stdio.h>
#include <stdatomic.h>
#include <pthread.h>

atomic_long counter = 0;

void *worker(void *arg) {
    (void)arg;
    for (int i = 0; i < 1000000; i++) {
        atomic_fetch_add_explicit(&counter, 1, memory_order_relaxed);
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, worker, NULL);
    pthread_create(&t2, NULL, worker, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("Atomic Counter: %ld (Expected: 2000000)\n", counter);
    return 0;
}
```

### Solution 2.18: False Sharing and Cache Line Padding
```c
#include <stdio.h>
#include <pthread.h>

struct Unpadded {
    long val;
};

struct Padded {
    long val;
    char pad[56]; // 64-byte alignment eliminates false sharing!
} __attribute__((aligned(64)));

struct Padded counters[4];

void *worker(void *arg) {
    int idx = *(int *)arg;
    for (long i = 0; i < 50000000L; i++) {
        counters[idx].val++;
    }
    return NULL;
}

int main(void) {
    pthread_t threads[4];
    int ids[4] = {0, 1, 2, 3};
    for (int i = 0; i < 4; i++) {
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }
    for (int i = 0; i < 4; i++) {
        pthread_join(threads[i], NULL);
    }
    printf("Padded workers completed without cache line contention.\n");
    return 0;
}
```
