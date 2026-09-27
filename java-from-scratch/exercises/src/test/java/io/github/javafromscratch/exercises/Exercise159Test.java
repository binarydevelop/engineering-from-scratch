package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 159 Test")
class Exercise159Test {

    @Test
    void testSolve() {
        int result = Exercise159.solve(10);
        assertEquals(20 + 159, result);
    }
}
