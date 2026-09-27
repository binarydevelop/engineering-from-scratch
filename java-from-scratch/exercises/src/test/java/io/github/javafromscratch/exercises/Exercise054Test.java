package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 054 Test")
class Exercise054Test {

    @Test
    void testSolve() {
        int result = Exercise054.solve(10);
        assertEquals(20 + 54, result);
    }
}
