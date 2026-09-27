package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 131 Test")
class Exercise131Test {

    @Test
    void testSolve() {
        int result = Exercise131.solve(10);
        assertEquals(20 + 131, result);
    }
}
