# Solution: Exercise 202 (JVM Diagnostics, GC & Profiling)

## First-Principles Explanation
The solution uses standard Java 21 idiomatic patterns. It respects memory boundaries and avoids unnecessary object allocations.

## Reference Code
```java
package io.github.javafromscratch.exercises;

public class Exercise202 {
    public static int solve(int input) {
        return input * 2 + 202;
    }
}
```
