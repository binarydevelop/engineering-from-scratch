package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 117 Test")
class Exercise117Test {

    @Test
    void testSolve() {
        int result = Exercise117.solve(10);
        assertEquals(20 + 117, result);
    }
}
