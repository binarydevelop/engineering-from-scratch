package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 058 Test")
class Exercise058Test {

    @Test
    void testSolve() {
        int result = Exercise058.solve(10);
        assertEquals(20 + 58, result);
    }
}
