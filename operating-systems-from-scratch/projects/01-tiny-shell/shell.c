#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <errno.h>

#define MAX_LINE 1024
#define MAX_ARGS 64

static volatile pid_t foreground_pid = 0;

void sigint_handler(int sig) {
    (void)sig;
    if (foreground_pid > 0) {
        // Forward SIGINT to the active foreground child
        kill(foreground_pid, SIGINT);
    } else {
        write(STDOUT_FILENO, "\nmini-shell> ", 13);
    }
}

void parse_tokens(char *line, char **args, int *arg_count) {
    *arg_count = 0;
    char *token = strtok(line, " \t\r\n");
    while (token != NULL && *arg_count < MAX_ARGS - 1) {
        args[(*arg_count)++] = token;
        token = strtok(NULL, " \t\r\n");
    }
    args[*arg_count] = NULL;
}

int handle_builtins(char **args, int arg_count) {
    if (arg_count == 0) return 1;

    if (strcmp(args[0], "exit") == 0) {
        printf("Exiting mini-shell. Goodbye!\n");
        exit(0);
    } else if (strcmp(args[0], "cd") == 0) {
        char *target = args[1] ? args[1] : getenv("HOME");
        if (target == NULL) target = "/";
        if (chdir(target) != 0) {
            perror("cd failed");
        }
        return 1;
    } else if (strcmp(args[0], "pwd") == 0) {
        char cwd[1024];
        if (getcwd(cwd, sizeof(cwd)) != NULL) {
            printf("%s\n", cwd);
        } else {
            perror("pwd failed");
        }
        return 1;
    } else if (strcmp(args[0], "help") == 0) {
        printf("Mini-Shell Built-in Commands:\n");
        printf("  cd <dir>     : Change current working directory\n");
        printf("  pwd          : Print current working directory\n");
        printf("  help         : Print this help message\n");
        printf("  exit         : Terminate the shell\n");
        printf("Features:\n");
        printf("  Pipes:       cmd1 | cmd2\n");
        printf("  Redirection: cmd > file, cmd >> file, cmd < file\n");
        printf("  Background:  cmd &\n");
        return 1;
    }
    return 0; // Not a builtin
}

void execute_simple_command(char **args, int arg_count, int is_background) {
    char *input_file = NULL;
    char *output_file = NULL;
    int append_mode = 0;

    // Filter out redirection tokens
    int clean_count = 0;
    char *clean_args[MAX_ARGS];

    for (int i = 0; i < arg_count; i++) {
        if (strcmp(args[i], "<") == 0 && i + 1 < arg_count) {
            input_file = args[++i];
        } else if (strcmp(args[i], ">") == 0 && i + 1 < arg_count) {
            output_file = args[++i];
            append_mode = 0;
        } else if (strcmp(args[i], ">>") == 0 && i + 1 < arg_count) {
            output_file = args[++i];
            append_mode = 1;
        } else {
            clean_args[clean_count++] = args[i];
        }
    }
    clean_args[clean_count] = NULL;
    if (clean_count == 0) return;

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        return;
    }

    if (pid == 0) {
        // --- CHILD PROCESS ---
        if (input_file) {
            int in_fd = open(input_file, O_RDONLY);
            if (in_fd < 0) { perror("open input"); exit(1); }
            dup2(in_fd, STDIN_FILENO);
            close(in_fd);
        }
        if (output_file) {
            int flags = O_WRONLY | O_CREAT | (append_mode ? O_APPEND : O_TRUNC);
            int out_fd = open(output_file, flags, 0644);
            if (out_fd < 0) { perror("open output"); exit(1); }
            dup2(out_fd, STDOUT_FILENO);
            close(out_fd);
        }

        execvp(clean_args[0], clean_args);
        fprintf(stderr, "mini-shell: command not found: %s\n", clean_args[0]);
        exit(127);
    } else {
        // --- PARENT PROCESS ---
        if (!is_background) {
            foreground_pid = pid;
            int status;
            waitpid(pid, &status, 0);
            foreground_pid = 0;
        } else {
            printf("[Process %d running in background]\n", pid);
        }
    }
}

void execute_pipeline(char *line) {
    char *pipe_segments[MAX_ARGS];
    int segment_count = 0;

    char *seg = strtok(line, "|");
    while (seg != NULL && segment_count < MAX_ARGS - 1) {
        pipe_segments[segment_count++] = seg;
        seg = strtok(NULL, "|");
    }
    pipe_segments[segment_count] = NULL;

    if (segment_count == 1) {
        // Single command (no pipes)
        char *args[MAX_ARGS];
        int arg_count = 0;
        int is_background = 0;

        parse_tokens(pipe_segments[0], args, &arg_count);
        if (arg_count > 0 && strcmp(args[arg_count - 1], "&") == 0) {
            is_background = 1;
            args[--arg_count] = NULL;
        }

        if (!handle_builtins(args, arg_count)) {
            execute_simple_command(args, arg_count, is_background);
        }
        return;
    }

    // Pipeline with segment_count commands
    int pipe_fds[2 * (segment_count - 1)];
    for (int i = 0; i < segment_count - 1; i++) {
        if (pipe(pipe_fds + i * 2) < 0) {
            perror("pipe creation failed");
            return;
        }
    }

    for (int i = 0; i < segment_count; i++) {
        char *args[MAX_ARGS];
        int arg_count = 0;
        parse_tokens(pipe_segments[i], args, &arg_count);
        if (arg_count == 0) continue;

        pid_t pid = fork();
        if (pid < 0) {
            perror("fork in pipeline");
            return;
        }

        if (pid == 0) {
            // If not first command, redirect stdin from previous pipe read end
            if (i != 0) {
                dup2(pipe_fds[(i - 1) * 2], STDIN_FILENO);
            }
            // If not last command, redirect stdout to current pipe write end
            if (i != segment_count - 1) {
                dup2(pipe_fds[i * 2 + 1], STDOUT_FILENO);
            }
            // Close all pipe descriptors in child
            for (int j = 0; j < 2 * (segment_count - 1); j++) {
                close(pipe_fds[j]);
            }

            execvp(args[0], args);
            fprintf(stderr, "mini-shell: command not found: %s\n", args[0]);
            exit(127);
        }
    }

    // Close all pipes in parent
    for (int j = 0; j < 2 * (segment_count - 1); j++) {
        close(pipe_fds[j]);
    }

    // Wait for all pipeline children
    for (int i = 0; i < segment_count; i++) {
        wait(NULL);
    }
}

int main(void) {
    struct sigaction sa;
    sa.sa_handler = sigint_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    sigaction(SIGINT, &sa, NULL);

    char line[MAX_LINE];
    printf("================================================================\n");
    printf("Welcome to Mini-Shell (Capstone 1: Expanded Unix Shell)\n");
    printf("Type 'help' for builtins or 'exit' to quit.\n");
    printf("================================================================\n");

    while (1) {
        // Reap any background zombie processes
        while (waitpid(-1, NULL, WNOHANG) > 0);

        printf("mini-shell> ");
        fflush(stdout);

        if (fgets(line, sizeof(line), stdin) == NULL) {
            // EOF (Ctrl+D)
            printf("\nExiting mini-shell.\n");
            break;
        }

        // Trim newline
        line[strcspn(line, "\r\n")] = 0;
        if (strlen(line) == 0) continue;

        execute_pipeline(line);
    }

    return 0;
}
