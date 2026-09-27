package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 002 Test")
class Exercise002Test {

    @Test
    void testSolve() {
        int result = Exercise002.solve(10);
        assertEquals(20 + 2, result);
    }
}
