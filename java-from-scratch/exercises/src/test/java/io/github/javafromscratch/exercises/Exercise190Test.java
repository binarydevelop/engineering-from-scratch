package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 190 Test")
class Exercise190Test {

    @Test
    void testSolve() {
        int result = Exercise190.solve(10);
        assertEquals(20 + 190, result);
    }
}
