package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 140 Test")
class Exercise140Test {

    @Test
    void testSolve() {
        int result = Exercise140.solve(10);
        assertEquals(20 + 140, result);
    }
}
