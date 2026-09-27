# Solution for Lab 18: Unclosed FileInputStream Leaking OS Handles

## Buggy Code Explanation
Exhausting OS open file descriptors (EMFILE: Too many open files)

## Fixed Code Walkthrough
The fix in `FixedLab18` restores the required class invariant or synchronization contract.
