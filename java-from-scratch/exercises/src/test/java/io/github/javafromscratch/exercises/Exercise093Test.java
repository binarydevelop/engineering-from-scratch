package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 093 Test")
class Exercise093Test {

    @Test
    void testSolve() {
        int result = Exercise093.solve(10);
        assertEquals(20 + 93, result);
    }
}
