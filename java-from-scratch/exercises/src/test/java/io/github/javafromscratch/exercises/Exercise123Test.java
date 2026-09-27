package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 123 Test")
class Exercise123Test {

    @Test
    void testSolve() {
        int result = Exercise123.solve(10);
        assertEquals(20 + 123, result);
    }
}
