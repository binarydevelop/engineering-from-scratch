# Solutions: Track 3 Synchronization Primitives Exercises

### Solution 3.1: Counting Semaphore Resource Pool
```c
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define TOTAL_SLOTS 3
#define TOTAL_WORKERS 8

sem_t db_pool;

void *worker(void *arg) {
    int id = *(int *)arg;
    printf("[Worker %d] Requesting database connection slot...\n", id);
    sem_wait(&db_pool); // Decrements semaphore; blocks if 0

    printf("[Worker %d] >>> ACQUIRED DB SLOT. Querying...\n", id);
    usleep(50000); // 50ms query simulation
    printf("[Worker %d] <<< Releasing DB slot.\n", id);

    sem_post(&db_pool); // Increments semaphore, waking a waiting worker
    return NULL;
}

int main(void) {
    sem_init(&db_pool, 0, TOTAL_SLOTS);
    pthread_t threads[TOTAL_WORKERS];
    int ids[TOTAL_WORKERS];

    for (int i = 0; i < TOTAL_WORKERS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }
    for (int i = 0; i < TOTAL_WORKERS; i++) {
        pthread_join(threads[i], NULL);
    }
    sem_destroy(&db_pool);
    return 0;
}
```

### Solution 3.5: Bounded Producer-Consumer Single Item
```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

int buffer = 0;
int has_data = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_empty = PTHREAD_COND_INITIALIZER;
pthread_cond_t cond_full = PTHREAD_COND_INITIALIZER;

void *producer(void *arg) {
    (void)arg;
    for (int i = 1; i <= 5; i++) {
        pthread_mutex_lock(&lock);
        while (has_data) {
            pthread_cond_wait(&cond_empty, &lock);
        }
        buffer = i * 10;
        has_data = 1;
        printf("[Producer] Deposited: %d\n", buffer);
        pthread_cond_signal(&cond_full);
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

void *consumer(void *arg) {
    (void)arg;
    for (int i = 1; i <= 5; i++) {
        pthread_mutex_lock(&lock);
        while (!has_data) {
            pthread_cond_wait(&cond_full, &lock);
        }
        int item = buffer;
        has_data = 0;
        printf("[Consumer] Consumed:  %d\n", item);
        pthread_cond_signal(&cond_empty);
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void) {
    pthread_t p, c;
    pthread_create(&p, NULL, producer, NULL);
    pthread_create(&c, NULL, consumer, NULL);
    pthread_join(p, NULL);
    pthread_join(c, NULL);
    return 0;
}
```

### Solution 3.8: Reader-Writer Lock (`pthread_rwlock_t`)
```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

int shared_data = 100;
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

void *reader(void *arg) {
    int id = *(int *)arg;
    for (int i = 0; i < 3; i++) {
        pthread_rwlock_rdlock(&rwlock);
        printf("[Reader %d] Read shared data: %d\n", id, shared_data);
        usleep(10000);
        pthread_rwlock_unlock(&rwlock);
        usleep(5000);
    }
    return NULL;
}

void *writer(void *arg) {
    (void)arg;
    for (int i = 1; i <= 2; i++) {
        pthread_rwlock_wrlock(&rwlock);
        shared_data += 50;
        printf("[Writer] Updated shared data to: %d\n", shared_data);
        usleep(20000);
        pthread_rwlock_unlock(&rwlock);
        usleep(20000);
    }
    return NULL;
}

int main(void) {
    pthread_t r[4], w;
    int ids[4] = {1, 2, 3, 4};
    for (int i = 0; i < 4; i++) pthread_create(&r[i], NULL, reader, &ids[i]);
    pthread_create(&w, NULL, writer, NULL);

    for (int i = 0; i < 4; i++) pthread_join(r[i], NULL);
    pthread_join(w, NULL);
    pthread_rwlock_destroy(&rwlock);
    return 0;
}
```
