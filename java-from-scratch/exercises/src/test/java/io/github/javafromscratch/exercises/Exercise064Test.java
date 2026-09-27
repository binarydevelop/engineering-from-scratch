package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 064 Test")
class Exercise064Test {

    @Test
    void testSolve() {
        int result = Exercise064.solve(10);
        assertEquals(20 + 64, result);
    }
}
