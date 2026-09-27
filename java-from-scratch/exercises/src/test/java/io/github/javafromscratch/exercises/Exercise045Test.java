package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 045 Test")
class Exercise045Test {

    @Test
    void testSolve() {
        int result = Exercise045.solve(10);
        assertEquals(20 + 45, result);
    }
}
