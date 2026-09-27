package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 147 Test")
class Exercise147Test {

    @Test
    void testSolve() {
        int result = Exercise147.solve(10);
        assertEquals(20 + 147, result);
    }
}
