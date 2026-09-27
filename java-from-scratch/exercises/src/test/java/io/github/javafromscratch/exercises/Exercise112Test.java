package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 112 Test")
class Exercise112Test {

    @Test
    void testSolve() {
        int result = Exercise112.solve(10);
        assertEquals(20 + 112, result);
    }
}
