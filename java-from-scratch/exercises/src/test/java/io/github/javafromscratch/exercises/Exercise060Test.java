package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 060 Test")
class Exercise060Test {

    @Test
    void testSolve() {
        int result = Exercise060.solve(10);
        assertEquals(20 + 60, result);
    }
}
