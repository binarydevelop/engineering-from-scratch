package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 202 Test")
class Exercise202Test {

    @Test
    void testSolve() {
        int result = Exercise202.solve(10);
        assertEquals(20 + 202, result);
    }
}
