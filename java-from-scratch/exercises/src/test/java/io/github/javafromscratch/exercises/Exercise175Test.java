package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 175 Test")
class Exercise175Test {

    @Test
    void testSolve() {
        int result = Exercise175.solve(10);
        assertEquals(20 + 175, result);
    }
}
