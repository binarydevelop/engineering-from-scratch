package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 025 Test")
class Exercise025Test {

    @Test
    void testSolve() {
        int result = Exercise025.solve(10);
        assertEquals(20 + 25, result);
    }
}
