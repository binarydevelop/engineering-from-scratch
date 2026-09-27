# Solution for Lab 17: Escaping this Reference from Constructor

## Buggy Code Explanation
Publishing this to another thread before constructor finishes establishing invariants

## Fixed Code Walkthrough
The fix in `FixedLab17` restores the required class invariant or synchronization contract.
