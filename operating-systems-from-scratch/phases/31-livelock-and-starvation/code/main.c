// Phase 31: Livelock and Starvation
// Motto: In deadlock nobody moves; in livelock everybody moves but makes no progress; in starvation one is left behind.

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(void) {
    printf("[Phase 31: Livelock and Starvation] Executing on Host (PID: %d)...\n", getpid());
    printf("Motto: In deadlock nobody moves; in livelock everybody moves but makes no progress; in starvation one is left behind.\n");
    return 0;
}
