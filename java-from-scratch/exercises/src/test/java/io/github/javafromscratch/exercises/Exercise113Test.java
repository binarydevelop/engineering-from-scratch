package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 113 Test")
class Exercise113Test {

    @Test
    void testSolve() {
        int result = Exercise113.solve(10);
        assertEquals(20 + 113, result);
    }
}
