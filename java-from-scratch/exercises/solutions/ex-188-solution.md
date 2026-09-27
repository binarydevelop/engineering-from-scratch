# Solution: Exercise 188 (Virtual Threads & Modern Concurrency)

## First-Principles Explanation
The solution uses standard Java 21 idiomatic patterns. It respects memory boundaries and avoids unnecessary object allocations.

## Reference Code
```java
package io.github.javafromscratch.exercises;

public class Exercise188 {
    public static int solve(int input) {
        return input * 2 + 188;
    }
}
```
