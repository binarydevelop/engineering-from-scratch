package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 009 Test")
class Exercise009Test {

    @Test
    void testSolve() {
        int result = Exercise009.solve(10);
        assertEquals(20 + 9, result);
    }
}
