// Solution 16: Introduce cooperative yielding (sched_yield) to ensure fair lock distribution.
#define _GNU_SOURCE
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <sched.h>

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
volatile int running = 1;

void *fair_worker_one(void *arg) {
    (void)arg;
    int count = 0;
    while (running) {
        pthread_mutex_lock(&lock);
        count++;
        pthread_mutex_unlock(&lock);
        // Fix: Explicitly yield the processor to give other waiting threads a chance
        sched_yield();
        usleep(10);
    }
    printf("[Worker 1] Fairly completed %d iterations\n", count);
    return NULL;
}

void *fair_worker_two(void *arg) {
    (void)arg;
    int count = 0;
    while (running) {
        pthread_mutex_lock(&lock);
        count++;
        pthread_mutex_unlock(&lock);
        sched_yield();
        usleep(10);
    }
    printf("[Worker 2] Fairly completed %d iterations\n", count);
    return NULL;
}

int main(void) {
    printf("[Solution 16] Running Fair Lock Distribution...\n");
    pthread_t t1, t2;
    pthread_create(&t1, NULL, fair_worker_one, NULL);
    pthread_create(&t2, NULL, fair_worker_two, NULL);

    sleep(1);
    running = 0;

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
