# Solution for Lab 10: Mutable Key Mutates After Put in HashMap

## Buggy Code Explanation
Mutating key field changes hashCode, making entry unfindable

## Fixed Code Walkthrough
The fix in `FixedLab10` restores the required class invariant or synchronization contract.
