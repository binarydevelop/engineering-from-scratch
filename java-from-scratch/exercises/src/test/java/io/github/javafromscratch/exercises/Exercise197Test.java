package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 197 Test")
class Exercise197Test {

    @Test
    void testSolve() {
        int result = Exercise197.solve(10);
        assertEquals(20 + 197, result);
    }
}
