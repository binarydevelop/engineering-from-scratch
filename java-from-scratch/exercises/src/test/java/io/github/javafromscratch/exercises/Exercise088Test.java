package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 088 Test")
class Exercise088Test {

    @Test
    void testSolve() {
        int result = Exercise088.solve(10);
        assertEquals(20 + 88, result);
    }
}
