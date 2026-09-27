package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 106 Test")
class Exercise106Test {

    @Test
    void testSolve() {
        int result = Exercise106.solve(10);
        assertEquals(20 + 106, result);
    }
}
