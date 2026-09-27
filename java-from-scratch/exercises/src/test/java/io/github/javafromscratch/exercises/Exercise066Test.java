package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 066 Test")
class Exercise066Test {

    @Test
    void testSolve() {
        int result = Exercise066.solve(10);
        assertEquals(20 + 66, result);
    }
}
