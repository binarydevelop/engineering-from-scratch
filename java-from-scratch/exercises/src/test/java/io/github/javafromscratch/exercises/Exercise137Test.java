package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 137 Test")
class Exercise137Test {

    @Test
    void testSolve() {
        int result = Exercise137.solve(10);
        assertEquals(20 + 137, result);
    }
}
