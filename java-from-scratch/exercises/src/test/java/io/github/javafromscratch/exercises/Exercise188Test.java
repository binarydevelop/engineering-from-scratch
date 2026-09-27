package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 188 Test")
class Exercise188Test {

    @Test
    void testSolve() {
        int result = Exercise188.solve(10);
        assertEquals(20 + 188, result);
    }
}
