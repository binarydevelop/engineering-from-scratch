package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 143 Test")
class Exercise143Test {

    @Test
    void testSolve() {
        int result = Exercise143.solve(10);
        assertEquals(20 + 143, result);
    }
}
