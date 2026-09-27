# Solution for Lab 14: Non-Atomic Compound Operation on volatile

## Buggy Code Explanation
volatile int count; count++ still suffers from race conditions

## Fixed Code Walkthrough
The fix in `FixedLab14` restores the required class invariant or synchronization contract.
