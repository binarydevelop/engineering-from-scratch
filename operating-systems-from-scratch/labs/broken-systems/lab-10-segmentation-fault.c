// Symptom: Process aborts with "Segmentation fault (core dumped)" (SIGSEGV).
// Task: Run under gdb, inspect backtrace and register $rip, and implement NULL checks before dereferencing pointers.
#include <stdio.h>

struct UserRecord {
    int id;
    char name[32];
};

void print_user(struct UserRecord *u) {
    // BUG: Dereferencing unverified pointer (NULL dereference!)
    printf("User ID: %d, Name: %s\n", u->id, u->name);
}

int main(void) {
    printf("[Lab 10] Demonstrating Segmentation Fault...\n");
    struct UserRecord *ptr = NULL;
    print_user(ptr);
    return 0;
}
