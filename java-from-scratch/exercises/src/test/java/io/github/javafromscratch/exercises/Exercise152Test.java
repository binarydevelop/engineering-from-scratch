package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 152 Test")
class Exercise152Test {

    @Test
    void testSolve() {
        int result = Exercise152.solve(10);
        assertEquals(20 + 152, result);
    }
}
