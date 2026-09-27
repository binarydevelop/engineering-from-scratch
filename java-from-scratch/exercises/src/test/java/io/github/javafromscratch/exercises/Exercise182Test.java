package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 182 Test")
class Exercise182Test {

    @Test
    void testSolve() {
        int result = Exercise182.solve(10);
        assertEquals(20 + 182, result);
    }
}
