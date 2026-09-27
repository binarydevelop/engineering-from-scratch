// Solution 17: Break livelock using randomized jitter / exponential backoff and lock hierarchy.
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t lock_a = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lock_b = PTHREAD_MUTEX_INITIALIZER;

void *worker_jitter(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < 5; i++) {
        // Fix: Use randomized delay when backing off
        while (1) {
            pthread_mutex_lock(&lock_a);
            if (pthread_mutex_trylock(&lock_b) == 0) {
                // Success!
                printf("[Worker %d] Acquired both locks!\n", id);
                usleep(1000);
                pthread_mutex_unlock(&lock_b);
                pthread_mutex_unlock(&lock_a);
                break;
            }
            pthread_mutex_unlock(&lock_a);
            // Add random jitter to desynchronize retry loops
            usleep((rand() % 500) + 100);
        }
    }
    return NULL;
}

int main(void) {
    printf("[Solution 17] Running Livelock-Free Workers with Jitter...\n");
    pthread_t t1, t2;
    int id1 = 1, id2 = 2;
    pthread_create(&t1, NULL, worker_jitter, &id1);
    pthread_create(&t2, NULL, worker_jitter, &id2);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("[Solution 17] Finished all work successfully.\n");
    return 0;
}
