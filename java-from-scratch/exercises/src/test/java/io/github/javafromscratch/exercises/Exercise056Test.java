package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 056 Test")
class Exercise056Test {

    @Test
    void testSolve() {
        int result = Exercise056.solve(10);
        assertEquals(20 + 56, result);
    }
}
