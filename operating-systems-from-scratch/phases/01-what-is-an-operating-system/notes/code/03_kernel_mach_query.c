#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/sysctl.h>
#include <mach/mach.h>

/**
 * Topic 03: Interrogating the Running Kernel
 * 
 * Demonstrates:
 * 1. Using sysctl() to query kernel properties directly from kernel memory.
 * 2. Using Mach kernel primitives (mach_task_self) to inspect internal kernel
 *    accounting for this process (page faults, virtual size, resident RAM).
 */

int main(void) {
    printf("================================================================\n");
    printf("TOPIC 03: INTERROGATING THE LIVING KERNEL\n");
    printf("================================================================\n");

    // 1. Query Kernel Version via sysctl
    char kernel_version[256];
    size_t size = sizeof(kernel_version);
    if (sysctlbyname("kern.version", kernel_version, &size, NULL, 0) == 0) {
        printf("[Kernel Identity]\n");
        printf("  Kernel Version String : %s\n", kernel_version);
    }

    // 2. Query Physical Memory size known to the Kernel
    int64_t memsize = 0;
    size = sizeof(memsize);
    if (sysctlbyname("hw.memsize", &memsize, &size, NULL, 0) == 0) {
        printf("  Physical RAM Managed  : %.2f GB\n", (double)memsize / (1024 * 1024 * 1024));
    }

    // 3. Query CPU Cores managed by the Kernel Scheduler
    int ncpu = 0;
    size = sizeof(ncpu);
    if (sysctlbyname("hw.ncpu", &ncpu, &size, NULL, 0) == 0) {
        printf("  Active CPU Cores      : %d cores\n", ncpu);
    }

    // 4. Inspect Kernel Process Tracking (Mach Task Info)
    struct mach_task_basic_info info;
    mach_msg_type_number_t count = MACH_TASK_BASIC_INFO_COUNT;
    kern_return_t kr = task_info(mach_task_self(), MACH_TASK_BASIC_INFO, (task_info_t)&info, &count);

    if (kr == KERN_SUCCESS) {
        printf("\n[Kernel PCB / Task Accounting for PID %d]\n", getpid());
        printf("  Virtual Address Space : %lu KB\n", (unsigned long)(info.virtual_size / 1024));
        printf("  Resident Memory (RAM) : %lu KB\n", (unsigned long)(info.resident_size / 1024));
        printf("  User CPU Time Used    : %d.%06d sec\n", (int)info.user_time.seconds, (int)info.user_time.microseconds);
        printf("  Kernel CPU Time Used  : %d.%06d sec (CPU time spent inside Ring 0!)\n", 
               (int)info.system_time.seconds, (int)info.system_time.microseconds);
    }

    printf("================================================================\n");
    return 0;
}
