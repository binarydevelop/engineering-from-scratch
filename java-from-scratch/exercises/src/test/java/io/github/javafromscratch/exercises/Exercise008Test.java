package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 008 Test")
class Exercise008Test {

    @Test
    void testSolve() {
        int result = Exercise008.solve(10);
        assertEquals(20 + 8, result);
    }
}
