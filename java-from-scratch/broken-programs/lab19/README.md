# Broken Lab 19: Character Encoding Corruption on Byte Conversions

> **Failure Type:** `EncodingMismatch`  
> **Symptom:** String.getBytes() using default system encoding instead of UTF-8

---

## 1. Problem Description
In high-scale Java systems, this failure manifests as string.getbytes() using default system encoding instead of utf-8.
The buggy code appears plausible at first glance but violates critical Java Language Specification (JLS) or JVM runtime invariants.

## 2. Buggy Implementation Snippet
```java
// See BuggyLab19.java
```

## 3. How to Reproduce
Run the reproduction test to observe the exact failure:
```bash
mvn test -pl broken-programs -Dtest=ReproductionLab19Test
```

## 4. Root Cause Analysis
- **Language / JVM Specification Rule**: What rule was violated?
- **Diagnostic Tool**: Using `jcmd`, `jstack`, `javap`, or stack trace forensics.

## 5. The Fix
Refactor the code into `FixedLab19.java`.

Verify the fix passes all assertions:
```bash
mvn test -pl broken-programs -Dtest=FixedLab19Test
```
