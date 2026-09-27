package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 165 Test")
class Exercise165Test {

    @Test
    void testSolve() {
        int result = Exercise165.solve(10);
        assertEquals(20 + 165, result);
    }
}
