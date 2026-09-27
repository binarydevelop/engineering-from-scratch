// Solution 22: Provide absolute path or verified relative path with executable permissions.
#include <stdio.h>
#include <unistd.h>
#include <errno.h>

int main(void) {
    // Fix: Explicitly specify absolute or relative path to binary
    char *args[] = {"/bin/echo", "Execution succeeded via absolute path!", NULL};

    printf("[Solution 22] Executing '%s'...\n", args[0]);
    execvp(args[0], args);

    perror("execvp");
    return 1;
}
