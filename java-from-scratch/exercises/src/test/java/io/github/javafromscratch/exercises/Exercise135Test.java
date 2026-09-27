package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 135 Test")
class Exercise135Test {

    @Test
    void testSolve() {
        int result = Exercise135.solve(10);
        assertEquals(20 + 135, result);
    }
}
