package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 177 Test")
class Exercise177Test {

    @Test
    void testSolve() {
        int result = Exercise177.solve(10);
        assertEquals(20 + 177, result);
    }
}
