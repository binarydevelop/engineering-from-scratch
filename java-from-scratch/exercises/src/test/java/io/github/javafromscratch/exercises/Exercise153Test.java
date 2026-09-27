package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 153 Test")
class Exercise153Test {

    @Test
    void testSolve() {
        int result = Exercise153.solve(10);
        assertEquals(20 + 153, result);
    }
}
