#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/mount.h>
#include <sys/stat.h>

#ifdef __linux__
#include <sched.h>
#include <sys/prctl.h>
#endif

#define STACK_SIZE (1024 * 1024) // 1 MB stack for cloned child

struct ContainerConfig {
    const char *hostname;
    const char *rootfs;
    char **argv;
};

int container_child(void *arg) {
    struct ContainerConfig *config = (struct ContainerConfig *)arg;

#ifdef __linux__
    // 1. UTS Namespace: Set private container hostname
    if (sethostname(config->hostname, strlen(config->hostname)) != 0) {
        perror("sethostname");
    }

    // 2. Prevent gaining new privileges via setuid binaries
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0) {
        perror("prctl(PR_SET_NO_NEW_PRIVS)");
    }

    // 3. Mount Namespace & Rootfs isolation
    if (config->rootfs) {
        if (chroot(config->rootfs) != 0) {
            perror("chroot failed (requires root / CAP_SYS_ADMIN)");
        } else {
            chdir("/");
        }
    }
#else
    printf("[Darwin/macOS Warning] Linux namespaces are Linux-specific.\n");
    printf("Simulating container execution without raw Linux kernel clone flags.\n");
#endif

    // Execute container payload command
    printf("[Container] Executing command: %s\n", config->argv[0]);
    execvp(config->argv[0], config->argv);
    perror("execvp failed");
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <command> [args...]\n", argv[0]);
        return 1;
    }

    struct ContainerConfig config;
    config.hostname = "sandbox-container";
    config.rootfs = NULL;
    config.argv = &argv[1];

    printf("================================================================\n");
    printf("Capstone 6: Tiny Container Sandbox Launcher\n");
    printf("================================================================\n");

#ifdef __linux__
    char *stack = malloc(STACK_SIZE);
    if (!stack) { perror("malloc stack"); return 1; }
    char *stack_top = stack + STACK_SIZE;

    // Clone child into new PID, UTS, Mount, and Network namespaces
    int clone_flags = CLONE_NEWPID | CLONE_NEWUTS | CLONE_NEWNS | CLONE_NEWNET | SIGCHLD;
    pid_t child_pid = clone(container_child, stack_top, clone_flags, &config);

    if (child_pid < 0) {
        perror("clone failed (Ensure you are running under sudo / CAP_SYS_ADMIN)");
        free(stack);
        return 1;
    }

    printf("[Host] Spawned isolated container PID %d\n", child_pid);
    waitpid(child_pid, NULL, 0);
    printf("[Host] Container terminated. Reaped cleanly.\n");
    free(stack);
#else
    printf("[Host Platform: Darwin/macOS]\n");
    printf("Linux namespaces (CLONE_NEWPID, CLONE_NEWNET) require a Linux kernel.\n");
    printf("Running child in standard process isolation mode.\n");
    pid_t pid = fork();
    if (pid == 0) {
        container_child(&config);
        exit(0);
    } else {
        waitpid(pid, NULL, 0);
    }
#endif

    return 0;
}
