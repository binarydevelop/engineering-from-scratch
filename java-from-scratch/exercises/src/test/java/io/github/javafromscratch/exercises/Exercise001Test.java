package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 001 Test")
class Exercise001Test {

    @Test
    void testSolve() {
        int result = Exercise001.solve(10);
        assertEquals(20 + 1, result);
    }
}
