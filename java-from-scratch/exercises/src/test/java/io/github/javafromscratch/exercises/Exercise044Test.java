package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 044 Test")
class Exercise044Test {

    @Test
    void testSolve() {
        int result = Exercise044.solve(10);
        assertEquals(20 + 44, result);
    }
}
