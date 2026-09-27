# Solution for Lab 31: N+1 Database Query Avalanche

## Buggy Code Explanation
Iterating entities fires separate select query per child record

## Fixed Code Walkthrough
The fix in `FixedLab31` restores the required class invariant or synchronization contract.
