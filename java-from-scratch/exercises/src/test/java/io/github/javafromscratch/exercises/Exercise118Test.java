package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 118 Test")
class Exercise118Test {

    @Test
    void testSolve() {
        int result = Exercise118.solve(10);
        assertEquals(20 + 118, result);
    }
}
