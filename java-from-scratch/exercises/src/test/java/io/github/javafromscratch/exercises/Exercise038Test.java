package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 038 Test")
class Exercise038Test {

    @Test
    void testSolve() {
        int result = Exercise038.solve(10);
        assertEquals(20 + 38, result);
    }
}
