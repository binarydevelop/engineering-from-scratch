# Solution for Lab 06: GC Allocation Storm from String Concat

## Buggy Code Explanation
Repeated string concatenation in tight loop generates gigabytes of temporary garbage

## Fixed Code Walkthrough
The fix in `FixedLab06` restores the required class invariant or synchronization contract.
