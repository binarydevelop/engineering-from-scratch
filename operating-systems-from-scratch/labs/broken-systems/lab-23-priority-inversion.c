// Symptom: High-priority task experiences high latency because a low-priority task holds a shared lock,
//          while medium-priority tasks preempt the low-priority task (unbounded priority inversion).
// Task: Diagnose priority inversion conceptually and configure priority inheritance mutex attributes.
#define _GNU_SOURCE
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t shared_lock = PTHREAD_MUTEX_INITIALIZER;
volatile int low_holds_lock = 0;
volatile int high_finished = 0;

void *low_worker(void *arg) {
    (void)arg;
    pthread_mutex_lock(&shared_lock);
    low_holds_lock = 1;
    printf("[Low Priority] Acquired shared lock. Simulating critical section...\n");
    usleep(200000); // 200ms
    printf("[Low Priority] Releasing shared lock.\n");
    pthread_mutex_unlock(&shared_lock);
    return NULL;
}

void *high_worker(void *arg) {
    (void)arg;
    while (!low_holds_lock) usleep(1000);
    printf("[High Priority] Waiting for shared lock held by Low Priority task...\n");
    pthread_mutex_lock(&shared_lock);
    printf("[High Priority] Acquired shared lock!\n");
    pthread_mutex_unlock(&shared_lock);
    high_finished = 1;
    return NULL;
}

int main(void) {
    printf("[Lab 23] Demonstrating Priority Inversion Concept...\n");
    pthread_t t_low, t_high;
    pthread_create(&t_low, NULL, low_worker, NULL);
    pthread_create(&t_high, NULL, high_worker, NULL);

    pthread_join(t_low, NULL);
    pthread_join(t_high, NULL);
    printf("[Lab 23] Completed.\n");
    return 0;
}
