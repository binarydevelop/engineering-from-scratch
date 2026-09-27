# Solution for Lab 16: ThreadLocal Leak in Recycled Thread Pool

## Buggy Code Explanation
ThreadLocal state bleeds into subsequent tasks executing on the same thread

## Fixed Code Walkthrough
The fix in `FixedLab16` restores the required class invariant or synchronization contract.
