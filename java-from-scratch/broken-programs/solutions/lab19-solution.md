# Solution for Lab 19: Character Encoding Corruption on Byte Conversions

## Buggy Code Explanation
String.getBytes() using default system encoding instead of UTF-8

## Fixed Code Walkthrough
The fix in `FixedLab19` restores the required class invariant or synchronization contract.
