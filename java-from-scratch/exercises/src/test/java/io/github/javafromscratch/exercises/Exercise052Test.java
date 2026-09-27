package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 052 Test")
class Exercise052Test {

    @Test
    void testSolve() {
        int result = Exercise052.solve(10);
        assertEquals(20 + 52, result);
    }
}
