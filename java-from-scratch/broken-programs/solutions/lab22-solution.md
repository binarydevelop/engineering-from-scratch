# Solution for Lab 22: Blocking I/O Inside Common ForkJoinPool

## Buggy Code Explanation
Parallel stream blocking all worker threads in the JVM common pool

## Fixed Code Walkthrough
The fix in `FixedLab22` restores the required class invariant or synchronization contract.
