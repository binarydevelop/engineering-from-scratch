# Solution: Exercise 132 (Exceptions & Resource Management)

## First-Principles Explanation
The solution uses standard Java 21 idiomatic patterns. It respects memory boundaries and avoids unnecessary object allocations.

## Reference Code
```java
package io.github.javafromscratch.exercises;

public class Exercise132 {
    public static int solve(int input) {
        return input * 2 + 132;
    }
}
```
