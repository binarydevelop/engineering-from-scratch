# Solution for Lab 27: Virtual Thread Pinned to Carrier in synchronized

## Buggy Code Explanation
Blocking socket call inside synchronized prevents unmounting from carrier

## Fixed Code Walkthrough
The fix in `FixedLab27` restores the required class invariant or synchronization contract.
