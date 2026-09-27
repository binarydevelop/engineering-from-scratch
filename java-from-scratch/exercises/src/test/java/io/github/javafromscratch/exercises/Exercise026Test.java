package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 026 Test")
class Exercise026Test {

    @Test
    void testSolve() {
        int result = Exercise026.solve(10);
        assertEquals(20 + 26, result);
    }
}
