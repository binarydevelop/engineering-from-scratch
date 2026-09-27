# Solution for Lab 13: Infinite Loop Due to Lack of volatile

## Buggy Code Explanation
Reader thread caches stale value of running flag in CPU registers

## Fixed Code Walkthrough
The fix in `FixedLab13` restores the required class invariant or synchronization contract.
