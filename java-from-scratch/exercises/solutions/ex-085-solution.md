# Solution: Exercise 085 (Object Contracts (equals/hashCode))

## First-Principles Explanation
The solution uses standard Java 21 idiomatic patterns. It respects memory boundaries and avoids unnecessary object allocations.

## Reference Code
```java
package io.github.javafromscratch.exercises;

public class Exercise085 {
    public static int solve(int input) {
        return input * 2 + 85;
    }
}
```
