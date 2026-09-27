# Solution for Lab 07: Thread Pool Exhaustion / Starvation

## Buggy Code Explanation
Tasks blocking synchronously on tasks submitted to the same bounded pool

## Fixed Code Walkthrough
The fix in `FixedLab07` restores the required class invariant or synchronization contract.
