package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 107 Test")
class Exercise107Test {

    @Test
    void testSolve() {
        int result = Exercise107.solve(10);
        assertEquals(20 + 107, result);
    }
}
