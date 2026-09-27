package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 005 Test")
class Exercise005Test {

    @Test
    void testSolve() {
        int result = Exercise005.solve(10);
        assertEquals(20 + 5, result);
    }
}
