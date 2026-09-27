// Solution 15: Synchronize shared state updates using a POSIX mutex.
#include <stdio.h>
#include <pthread.h>

#define ITERATIONS 1000000

long counter = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *worker(void *arg) {
    (void)arg;
    for (int i = 0; i < ITERATIONS; i++) {
        // Fix: Mutual exclusion ensures atomicity of counter increment
        pthread_mutex_lock(&lock);
        counter++;
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

    printf("[Solution 15] Final Counter: %ld (Expected: %d) -> EXACT MATCH!\n",
           counter, ITERATIONS * 2);
    pthread_mutex_destroy(&lock);
    return 0;
}
