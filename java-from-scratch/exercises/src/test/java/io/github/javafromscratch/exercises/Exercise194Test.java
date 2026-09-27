package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 194 Test")
class Exercise194Test {

    @Test
    void testSolve() {
        int result = Exercise194.solve(10);
        assertEquals(20 + 194, result);
    }
}
