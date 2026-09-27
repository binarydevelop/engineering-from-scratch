package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 185 Test")
class Exercise185Test {

    @Test
    void testSolve() {
        int result = Exercise185.solve(10);
        assertEquals(20 + 185, result);
    }
}
