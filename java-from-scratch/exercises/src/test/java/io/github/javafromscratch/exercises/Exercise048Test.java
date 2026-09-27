package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 048 Test")
class Exercise048Test {

    @Test
    void testSolve() {
        int result = Exercise048.solve(10);
        assertEquals(20 + 48, result);
    }
}
