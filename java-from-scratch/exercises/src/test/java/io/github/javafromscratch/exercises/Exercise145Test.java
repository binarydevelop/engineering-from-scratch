package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 145 Test")
class Exercise145Test {

    @Test
    void testSolve() {
        int result = Exercise145.solve(10);
        assertEquals(20 + 145, result);
    }
}
