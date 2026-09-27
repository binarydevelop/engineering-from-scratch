package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 183 Test")
class Exercise183Test {

    @Test
    void testSolve() {
        int result = Exercise183.solve(10);
        assertEquals(20 + 183, result);
    }
}
