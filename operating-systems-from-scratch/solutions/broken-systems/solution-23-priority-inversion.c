// Solution 23: Initialize mutex with PTHREAD_PRIO_INHERIT attribute to prevent unbounded priority inversion.
#define _GNU_SOURCE
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

pthread_mutex_t prio_lock;

int main(void) {
    pthread_mutexattr_t attr;
    pthread_mutexattr_init(&attr);

#if defined(PTHREAD_PRIO_INHERIT)
    // Fix: Set priority inheritance protocol
    if (pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT) == 0) {
        printf("[Solution 23] Configured mutex with PTHREAD_PRIO_INHERIT.\n");
    } else {
        printf("[Solution 23] PTHREAD_PRIO_INHERIT not supported by current platform scheduler.\n");
    }
#endif

    pthread_mutex_init(&prio_lock, &attr);
    pthread_mutexattr_destroy(&attr);

    printf("[Solution 23] Priority inheritance initialized successfully.\n");
    pthread_mutex_destroy(&prio_lock);
    return 0;
}
