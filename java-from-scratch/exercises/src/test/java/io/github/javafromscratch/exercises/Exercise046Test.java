package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 046 Test")
class Exercise046Test {

    @Test
    void testSolve() {
        int result = Exercise046.solve(10);
        assertEquals(20 + 46, result);
    }
}
