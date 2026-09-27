package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 149 Test")
class Exercise149Test {

    @Test
    void testSolve() {
        int result = Exercise149.solve(10);
        assertEquals(20 + 149, result);
    }
}
