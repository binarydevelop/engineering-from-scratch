package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 125 Test")
class Exercise125Test {

    @Test
    void testSolve() {
        int result = Exercise125.solve(10);
        assertEquals(20 + 125, result);
    }
}
