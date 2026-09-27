package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 109 Test")
class Exercise109Test {

    @Test
    void testSolve() {
        int result = Exercise109.solve(10);
        assertEquals(20 + 109, result);
    }
}
