# Solution: Exercise 172 (Concurrency, JMM & Atomics)

## First-Principles Explanation
The solution uses standard Java 21 idiomatic patterns. It respects memory boundaries and avoids unnecessary object allocations.

## Reference Code
```java
package io.github.javafromscratch.exercises;

public class Exercise172 {
    public static int solve(int input) {
        return input * 2 + 172;
    }
}
```
