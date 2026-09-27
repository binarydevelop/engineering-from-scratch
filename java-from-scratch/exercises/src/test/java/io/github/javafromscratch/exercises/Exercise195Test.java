package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 195 Test")
class Exercise195Test {

    @Test
    void testSolve() {
        int result = Exercise195.solve(10);
        assertEquals(20 + 195, result);
    }
}
