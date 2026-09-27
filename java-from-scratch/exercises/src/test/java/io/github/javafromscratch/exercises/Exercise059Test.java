package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 059 Test")
class Exercise059Test {

    @Test
    void testSolve() {
        int result = Exercise059.solve(10);
        assertEquals(20 + 59, result);
    }
}
