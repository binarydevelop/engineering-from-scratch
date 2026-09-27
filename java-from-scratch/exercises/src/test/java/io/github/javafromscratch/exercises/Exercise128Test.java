package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 128 Test")
class Exercise128Test {

    @Test
    void testSolve() {
        int result = Exercise128.solve(10);
        assertEquals(20 + 128, result);
    }
}
