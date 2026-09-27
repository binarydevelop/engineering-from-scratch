package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 031 Test")
class Exercise031Test {

    @Test
    void testSolve() {
        int result = Exercise031.solve(10);
        assertEquals(20 + 31, result);
    }
}
