package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 070 Test")
class Exercise070Test {

    @Test
    void testSolve() {
        int result = Exercise070.solve(10);
        assertEquals(20 + 70, result);
    }
}
