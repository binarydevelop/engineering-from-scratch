package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 171 Test")
class Exercise171Test {

    @Test
    void testSolve() {
        int result = Exercise171.solve(10);
        assertEquals(20 + 171, result);
    }
}
