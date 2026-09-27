# Solution for Lab 05: Unbounded Static Map Memory Leak

## Buggy Code Explanation
Static collection retains object references, preventing GC reclamation

## Fixed Code Walkthrough
The fix in `FixedLab05` restores the required class invariant or synchronization contract.
