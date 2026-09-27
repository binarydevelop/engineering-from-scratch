package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 089 Test")
class Exercise089Test {

    @Test
    void testSolve() {
        int result = Exercise089.solve(10);
        assertEquals(20 + 89, result);
    }
}
