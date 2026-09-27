# Solution for Lab 35: StackOverflowError from Unbounded Recursion

## Buggy Code Explanation
Method recursive call without base case exhausts 1MB thread stack

## Fixed Code Walkthrough
The fix in `FixedLab35` restores the required class invariant or synchronization contract.
