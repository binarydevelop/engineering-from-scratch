package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 004 Test")
class Exercise004Test {

    @Test
    void testSolve() {
        int result = Exercise004.solve(10);
        assertEquals(20 + 4, result);
    }
}
