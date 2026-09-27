# Solutions: Track 4 Virtual Memory Exercises

### Solution 4.1: Inspecting Memory Segments
```c
#include <stdio.h>
#include <stdlib.h>

int uninit_global;               // BSS segment
int init_global = 42;            // Data segment
const char *str = "Hello OS";    // Text (ROData)

int main(void) {
    int stack_var = 10;          // Stack
    char *heap_var = malloc(64); // Heap

    printf("Text (main):        %p\n", (void *)&main);
    printf("ROData (string):    %p\n", (void *)str);
    printf("Data (init_global): %p\n", (void *)&init_global);
    printf("BSS (uninit_glob):  %p\n", (void *)&uninit_global);
    printf("Heap (malloc):      %p\n", (void *)heap_var);
    printf("Stack (stack_var):  %p\n", (void *)&stack_var);

    free(heap_var);
    return 0;
}
```

### Solution 4.3: Manual Offset Calculation
* 32-bit address space, 4KB ($2^{12}$ bytes) page size:
  * 12 bits for offset ($0 \dots 4095$).
  * $32 - 12 = 20$ bits for Virtual Page Number (VPN).
* Address `0x0001A4B0`:
  * Lower 12 bits (3 hex digits: `4B0`) = Offset `0x4B0` (1,200 bytes into the page).
  * Upper 20 bits (`0x0001A`) = VPN `0x1A` (Page 26).

### Solution 4.5: Anonymous Memory Mapping with `mmap`
```c
#include <stdio.h>
#include <sys/mman.h>
#include <string.h>

int main(void) {
    size_t size = 1024 * 1024; // 1 MB
    char *ptr = mmap(NULL, size, PROT_READ | PROT_WRITE,
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap failed");
        return 1;
    }

    strcpy(ptr, "Anonymous memory allocated directly from kernel MMU!");
    printf("mmap pointer: %p\nPayload: %s\n", (void *)ptr, ptr);

    munmap(ptr, size);
    return 0;
}
```

### Solution 4.8: Demand Paging & RSS Measurement
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    size_t bytes = 50 * 1024 * 1024; // 50 MB
    printf("[Step 1] Allocating 50MB virtual memory (PID: %d)...\n", getpid());
    char *buf = malloc(bytes);
    printf("Check top/ps: VIRT increased by 50MB, but RES is ~0MB (Demand Paging!)\n");
    sleep(2);

    printf("[Step 2] Writing to every 4KB page...\n");
    for (size_t i = 0; i < bytes; i += 4096) {
        buf[i] = 1; // Forces physical frame allocation via minor page fault
    }
    printf("Check top/ps: RES has now climbed to 50MB!\n");
    sleep(2);

    free(buf);
    return 0;
}
```

### Solution 4.15: ASLR Demonstration
```c
#include <stdio.h>

int main(void) {
    int local = 10;
    printf("Main address:  %p | Stack address: %p\n", (void *)&main, (void *)&local);
    return 0;
}
```
**Explanation:** If ASLR is enabled in the Linux kernel (`/proc/sys/kernel/randomize_va_space > 0`), the addresses will change on every invocation to protect against Return-Oriented Programming (ROP) exploits.
