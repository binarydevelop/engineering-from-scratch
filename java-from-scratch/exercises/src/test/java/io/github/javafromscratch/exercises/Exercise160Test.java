package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 160 Test")
class Exercise160Test {

    @Test
    void testSolve() {
        int result = Exercise160.solve(10);
        assertEquals(20 + 160, result);
    }
}
