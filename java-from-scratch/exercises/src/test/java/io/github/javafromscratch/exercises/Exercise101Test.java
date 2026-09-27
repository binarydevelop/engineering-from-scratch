package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 101 Test")
class Exercise101Test {

    @Test
    void testSolve() {
        int result = Exercise101.solve(10);
        assertEquals(20 + 101, result);
    }
}
