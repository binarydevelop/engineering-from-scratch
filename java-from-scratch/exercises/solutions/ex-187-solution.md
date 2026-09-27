# Solution: Exercise 187 (Virtual Threads & Modern Concurrency)

## First-Principles Explanation
The solution uses standard Java 21 idiomatic patterns. It respects memory boundaries and avoids unnecessary object allocations.

## Reference Code
```java
package io.github.javafromscratch.exercises;

public class Exercise187 {
    public static int solve(int input) {
        return input * 2 + 187;
    }
}
```
