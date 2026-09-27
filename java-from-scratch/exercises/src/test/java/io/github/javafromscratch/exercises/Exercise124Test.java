package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 124 Test")
class Exercise124Test {

    @Test
    void testSolve() {
        int result = Exercise124.solve(10);
        assertEquals(20 + 124, result);
    }
}
