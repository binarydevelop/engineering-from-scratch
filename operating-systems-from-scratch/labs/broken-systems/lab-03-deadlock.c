// Symptom: Multi-threaded server hangs indefinitely with 0% CPU. Neither thread terminates.
// Task: Inspect hung threads using gdb (thread apply all bt), detect the circular mutex acquisition order, and fix by enforcing strict lock hierarchy.
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t lock_a = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lock_b = PTHREAD_MUTEX_INITIALIZER;

void *worker_one(void *arg) {
    (void)arg;
    printf("[Worker 1] Acquiring Lock A...\n");
    pthread_mutex_lock(&lock_a);
    usleep(10000); // 10ms delay to force race window

    printf("[Worker 1] Waiting for Lock B...\n");
    pthread_mutex_lock(&lock_b); // DEADLOCK!

    printf("[Worker 1] Acquired both locks!\n");
    pthread_mutex_unlock(&lock_b);
    pthread_mutex_unlock(&lock_a);
    return NULL;
}

void *worker_two(void *arg) {
    (void)arg;
    printf("[Worker 2] Acquiring Lock B...\n");
    pthread_mutex_lock(&lock_b);
    usleep(10000); // 10ms delay

    printf("[Worker 2] Waiting for Lock A...\n");
    pthread_mutex_lock(&lock_a); // DEADLOCK!

    printf("[Worker 2] Acquired both locks!\n");
    pthread_mutex_unlock(&lock_a);
    pthread_mutex_unlock(&lock_b);
    return NULL;
}

int main(void) {
    printf("[Lab 03] Demonstrating Thread Deadlock...\n");
    pthread_t t1, t2;
    pthread_create(&t1, NULL, worker_one, NULL);
    pthread_create(&t2, NULL, worker_two, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
