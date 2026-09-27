// Symptom: Shared counter output is far less than expected (e.g. 1,240,000 instead of 2,000,000).
// Task: Explain non-atomic read-modify-write CPU instructions, reproduce the race condition, and fix with a mutex.
#include <stdio.h>
#include <pthread.h>

#define ITERATIONS 1000000

long counter = 0;

void *worker(void *arg) {
    (void)arg;
    for (int i = 0; i < ITERATIONS; i++) {
        // BUG: Non-atomic increment (read -> add -> write) interleaved across CPU cores!
        counter++;
    }
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, worker, NULL);
    pthread_create(&t2, NULL, worker, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("[Lab 15] Final Counter: %ld (Expected: %d)\n", counter, ITERATIONS * 2);
    return 0;
}
