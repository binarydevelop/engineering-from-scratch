package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 012 Test")
class Exercise012Test {

    @Test
    void testSolve() {
        int result = Exercise012.solve(10);
        assertEquals(20 + 12, result);
    }
}
