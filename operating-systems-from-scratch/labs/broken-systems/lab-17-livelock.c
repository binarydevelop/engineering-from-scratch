// Symptom: High CPU usage, threads are actively running and changing states, but zero work is ever completed.
// Task: Diagnose livelock where threads back off in lockstep, and resolve using randomized exponential backoff.
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t lock_a = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lock_b = PTHREAD_MUTEX_INITIALIZER;
volatile int running = 1;

void *polite_worker_one(void *arg) {
    (void)arg;
    int attempts = 0;
    while (running && attempts < 1000) {
        attempts++;
        pthread_mutex_lock(&lock_a);
        usleep(100);
        if (pthread_mutex_trylock(&lock_b) != 0) {
            // Politely back off and retry
            pthread_mutex_unlock(&lock_a);
            usleep(100); // BUG: Exact same backoff duration causes lockstep livelock!
            continue;
        }
        printf("[Worker 1] Acquired both!\n");
        pthread_mutex_unlock(&lock_b);
        pthread_mutex_unlock(&lock_a);
        break;
    }
    return NULL;
}

void *polite_worker_two(void *arg) {
    (void)arg;
    int attempts = 0;
    while (running && attempts < 1000) {
        attempts++;
        pthread_mutex_lock(&lock_b);
        usleep(100);
        if (pthread_mutex_trylock(&lock_a) != 0) {
            pthread_mutex_unlock(&lock_b);
            usleep(100); // BUG: Exact same backoff duration!
            continue;
        }
        printf("[Worker 2] Acquired both!\n");
        pthread_mutex_unlock(&lock_a);
        pthread_mutex_unlock(&lock_b);
        break;
    }
    return NULL;
}

int main(void) {
    printf("[Lab 17] Demonstrating Livelock (politely yielding in lockstep)...\n");
    pthread_t t1, t2;
    pthread_create(&t1, NULL, polite_worker_one, NULL);
    pthread_create(&t2, NULL, polite_worker_two, NULL);

    sleep(1);
    running = 0;

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("[Lab 17] Livelock demonstration complete.\n");
    return 0;
}
