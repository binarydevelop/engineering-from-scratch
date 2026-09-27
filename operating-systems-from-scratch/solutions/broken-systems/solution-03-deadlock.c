// Solution 03: Enforce strict lock ordering across all threads (always lock A before B).
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t lock_a = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lock_b = PTHREAD_MUTEX_INITIALIZER;

void *worker_one(void *arg) {
    (void)arg;
    pthread_mutex_lock(&lock_a);
    pthread_mutex_lock(&lock_b);

    printf("[Worker 1] Acquired Lock A and Lock B cleanly!\n");
    pthread_mutex_unlock(&lock_b);
    pthread_mutex_unlock(&lock_a);
    return NULL;
}

void *worker_two(void *arg) {
    (void)arg;
    // Fix: Acquire Lock A first, then Lock B (same order as Worker 1!)
    pthread_mutex_lock(&lock_a);
    pthread_mutex_lock(&lock_b);

    printf("[Worker 2] Acquired Lock A and Lock B cleanly!\n");
    pthread_mutex_unlock(&lock_b);
    pthread_mutex_unlock(&lock_a);
    return NULL;
}

int main(void) {
    printf("[Solution 03] Running Deadlock-Free Workers...\n");
    pthread_t t1, t2;
    pthread_create(&t1, NULL, worker_one, NULL);
    pthread_create(&t2, NULL, worker_two, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("[Solution 03] Finished without deadlock.\n");
    return 0;
}
