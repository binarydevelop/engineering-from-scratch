// Solution 19: Clear pointers immediately upon free to prevent dangling access.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Session {
    int user_id;
    char token[32];
};

int main(void) {
    printf("[Solution 19] Running safe session lifecycle...\n");

    struct Session *s = malloc(sizeof(struct Session));
    if (!s) return 1;
    s->user_id = 42;
    strcpy(s->token, "secret_auth_token");

    // Proper teardown
    free(s);
    s = NULL; // Fix: Neutralize dangling pointer

    if (s != NULL) {
        s->user_id = 999;
    } else {
        printf("[Solution 19] Pointer is NULL; prevented illegal memory write.\n");
    }
    return 0;
}
