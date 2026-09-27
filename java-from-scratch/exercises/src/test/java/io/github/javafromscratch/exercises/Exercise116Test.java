package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 116 Test")
class Exercise116Test {

    @Test
    void testSolve() {
        int result = Exercise116.solve(10);
        assertEquals(20 + 116, result);
    }
}
