package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 074 Test")
class Exercise074Test {

    @Test
    void testSolve() {
        int result = Exercise074.solve(10);
        assertEquals(20 + 74, result);
    }
}
