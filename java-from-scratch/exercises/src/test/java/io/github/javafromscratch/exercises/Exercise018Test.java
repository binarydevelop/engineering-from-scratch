package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 018 Test")
class Exercise018Test {

    @Test
    void testSolve() {
        int result = Exercise018.solve(10);
        assertEquals(20 + 18, result);
    }
}
