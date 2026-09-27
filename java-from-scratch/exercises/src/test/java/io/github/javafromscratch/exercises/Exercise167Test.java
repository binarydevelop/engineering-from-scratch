package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 167 Test")
class Exercise167Test {

    @Test
    void testSolve() {
        int result = Exercise167.solve(10);
        assertEquals(20 + 167, result);
    }
}
