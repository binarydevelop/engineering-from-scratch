package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 039 Test")
class Exercise039Test {

    @Test
    void testSolve() {
        int result = Exercise039.solve(10);
        assertEquals(20 + 39, result);
    }
}
