package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 193 Test")
class Exercise193Test {

    @Test
    void testSolve() {
        int result = Exercise193.solve(10);
        assertEquals(20 + 193, result);
    }
}
