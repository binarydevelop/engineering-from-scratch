// Solution 10: Perform defensive NULL pointer verification before dereferencing.
#include <stdio.h>

struct UserRecord {
    int id;
    char name[32];
};

void print_user_safe(struct UserRecord *u) {
    // Fix: Validate pointer before dereferencing
    if (u == NULL) {
        fprintf(stderr, "Warning: Attempted to print NULL user record.\n");
        return;
    }
    printf("User ID: %d, Name: %s\n", u->id, u->name);
}

int main(void) {
    printf("[Solution 10] Running safe pointer access...\n");
    struct UserRecord *ptr = NULL;
    print_user_safe(ptr);

    struct UserRecord valid_user = {101, "Alice"};
    print_user_safe(&valid_user);
    return 0;
}
