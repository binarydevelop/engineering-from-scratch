# Solution for Lab 12: Race Condition on Non-Synchronized Shared Counter

## Buggy Code Explanation
Concurrent increments lose updates due to non-atomic read-modify-write

## Fixed Code Walkthrough
The fix in `FixedLab12` restores the required class invariant or synchronization contract.
