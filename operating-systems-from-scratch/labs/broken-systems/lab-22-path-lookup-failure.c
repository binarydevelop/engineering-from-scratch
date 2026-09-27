// Symptom: execvp() fails with ENOENT (No such file or directory) even though the binary exists on disk.
// Task: Explain how the kernel searches directories in $PATH, trace the failure, and provide absolute or relative paths.
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main(void) {
    char *args[] = {"custom_script", NULL};

    printf("[Lab 22] Executing '%s' via execvp...\n", args[0]);

    // BUG: "custom_script" is not in $PATH, so execvp searches /usr/bin, /bin, etc. and fails!
    execvp(args[0], args);

    printf("execvp failed: %s (errno: %d)\n", strerror(errno), errno);
    return 1;
}
