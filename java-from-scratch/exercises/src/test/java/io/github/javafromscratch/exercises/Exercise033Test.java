package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 033 Test")
class Exercise033Test {

    @Test
    void testSolve() {
        int result = Exercise033.solve(10);
        assertEquals(20 + 33, result);
    }
}
