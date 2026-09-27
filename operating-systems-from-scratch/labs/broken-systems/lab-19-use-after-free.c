// Symptom: Mysterious memory corruption or crash in malloc allocator metadata.
// Task: Compile with AddressSanitizer (-fsanitize=address), observe the heap-use-after-free report, and set freed pointers to NULL.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Session {
    int user_id;
    char token[32];
};

int main(void) {
    printf("[Lab 19] Demonstrating Use-After-Free...\n");

    struct Session *s = malloc(sizeof(struct Session));
    s->user_id = 42;
    strcpy(s->token, "secret_auth_token");

    // Free the session
    free(s);

    // BUG: Writing to memory after free() has relinquished ownership to the allocator!
    s->user_id = 999;
    printf("[Lab 19] Wrote through dangling pointer! User ID: %d\n", s->user_id);
    return 0;
}
