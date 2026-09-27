// Symptom: Worker 2 never acquires the lock or processes work because Worker 1 hogs the mutex in a tight loop.
// Task: Diagnose unfair lock contention, and introduce fairness through condition variables or yielding.
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
volatile int running = 1;

void *greedy_worker(void *arg) {
    (void)arg;
    int count = 0;
    while (running) {
        pthread_mutex_lock(&lock);
        count++;
        // BUG: Greedy worker unlocks and immediately relocks without yielding the CPU!
        pthread_mutex_unlock(&lock);
    }
    printf("[Greedy Worker] Completed %d iterations\n", count);
    return NULL;
}

void *starved_worker(void *arg) {
    (void)arg;
    int count = 0;
    while (running) {
        if (pthread_mutex_trylock(&lock) == 0) {
            count++;
            pthread_mutex_unlock(&lock);
        }
        usleep(100);
    }
    printf("[Starved Worker] Completed only %d iterations (STARVATION!)\n", count);
    return NULL;
}

int main(void) {
    printf("[Lab 16] Thread Starvation Lab...\n");
    pthread_t t1, t2;
    pthread_create(&t1, NULL, greedy_worker, NULL);
    pthread_create(&t2, NULL, starved_worker, NULL);

    sleep(1);
    running = 0;

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
