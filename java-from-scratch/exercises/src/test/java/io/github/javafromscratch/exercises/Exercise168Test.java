package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 168 Test")
class Exercise168Test {

    @Test
    void testSolve() {
        int result = Exercise168.solve(10);
        assertEquals(20 + 168, result);
    }
}
