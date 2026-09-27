package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 030 Test")
class Exercise030Test {

    @Test
    void testSolve() {
        int result = Exercise030.solve(10);
        assertEquals(20 + 30, result);
    }
}
