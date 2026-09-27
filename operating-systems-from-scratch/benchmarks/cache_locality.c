#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ROWS 4096
#define COLS 4096

static int matrix[ROWS][COLS];

int main(void) {
    // Warm up and initialize
    for (int r = 0; r < ROWS; r++) {
        for (int c = 0; c < COLS; c++) {
            matrix[r][c] = 1;
        }
    }

    struct timespec start, end;

    // 1. Row-Major Traversal (Stride-1, sequential, spatial locality)
    clock_gettime(CLOCK_MONOTONIC, &start);
    long long sum_row = 0;
    for (int r = 0; r < ROWS; r++) {
        for (int c = 0; c < COLS; c++) {
            sum_row += matrix[r][c];
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    long long row_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);

    // 2. Column-Major Traversal (Stride-4096, non-sequential, cache line thrashing)
    clock_gettime(CLOCK_MONOTONIC, &start);
    long long sum_col = 0;
    for (int c = 0; c < COLS; c++) {
        for (int r = 0; r < ROWS; r++) {
            sum_col += matrix[r][c];
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    long long col_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);

    printf("================================================================\n");
    printf("CPU Cache Locality Benchmark (Matrix Traversal: %dx%d)\n", ROWS, COLS);
    printf("Total Elements: %d integers (%.1f MB)\n", ROWS * COLS, (ROWS * COLS * sizeof(int)) / (1024.0 * 1024.0));
    printf("================================================================\n");
    printf("Row-Major Traversal (Spatial Locality):    %.3f ms (Sum: %lld)\n", row_ns / 1000000.0, sum_row);
    printf("Column-Major Traversal (Cache Thrashing): %.3f ms (Sum: %lld)\n", col_ns / 1000000.0, sum_col);
    printf("Performance Penalty:                      %.2fx slower due to cache misses!\n", (double)col_ns / row_ns);
    printf("================================================================\n");
    return 0;
}
