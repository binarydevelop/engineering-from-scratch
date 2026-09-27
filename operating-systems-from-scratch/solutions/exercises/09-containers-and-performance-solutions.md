# Solutions: Track 9 Containers & Performance Exercises

### Solution 9.1 & 9.2: PID & Mount Namespaces
When `unshare --pid --fork bash` is executed, the newly spawned child receives a fresh PID namespace, where its own thread group leader is assigned PID 1.
However, `/proc` is still the host's `/proc` mounted on the parent filesystem! `ps` inspects `/proc`, not the kernel's active task table directly.
To complete container process isolation:
```bash
# In mount namespace:
mount -t proc proc /proc
ps -ef
# Now ps only displays processes residing in the container's PID namespace!
```

### Solution 9.6: Cgroups v2 CPU Throttling
```bash
# Set 50ms quota per 100ms period (50% of one core)
echo "50000 100000" > /sys/fs/cgroup/test_limit/cpu.max
# Add PID 1234 to cgroup
echo 1234 > /sys/fs/cgroup/test_limit/cgroup.procs
```
When PID 1234 executes a tight infinite loop, the CFS (Completely Fair Scheduler) tracks consumed runtime ticks. Once 50ms of CPU time is consumed within the 100ms period window, the scheduler moves the task off the runqueue until the period expires, enforcing strict hardware CPU limits.

### Solution 9.13: Branch Prediction Penalty
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 1000000

int compare(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

int main(void) {
    int *data = malloc(SIZE * sizeof(int));
    for (int i = 0; i < SIZE; i++) data[i] = rand() % 256;

    // Unsorted run
    struct timespec s1, e1;
    clock_gettime(CLOCK_MONOTONIC, &s1);
    long long sum1 = 0;
    for (int i = 0; i < SIZE; i++) {
        if (data[i] > 128) sum1 += data[i]; // Unpredictable branch!
    }
    clock_gettime(CLOCK_MONOTONIC, &e1);

    // Sorted run
    qsort(data, SIZE, sizeof(int), compare);
    struct timespec s2, e2;
    clock_gettime(CLOCK_MONOTONIC, &s2);
    long long sum2 = 0;
    for (int i = 0; i < SIZE; i++) {
        if (data[i] > 128) sum2 += data[i]; // Predictable branch!
    }
    clock_gettime(CLOCK_MONOTONIC, &e2);

    double t_unsorted = (e1.tv_sec - s1.tv_sec) * 1000.0 + (e1.tv_nsec - s1.tv_nsec) / 1000000.0;
    double t_sorted   = (e2.tv_sec - s2.tv_sec) * 1000.0 + (e2.tv_nsec - s2.tv_nsec) / 1000000.0;

    printf("Unsorted array sum time: %.3f ms\n", t_unsorted);
    printf("Sorted array sum time:   %.3f ms (%.1fx faster due to branch prediction!)\n",
           t_sorted, t_unsorted / t_sorted);

    free(data);
    return 0;
}
```
