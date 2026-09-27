package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 191 Test")
class Exercise191Test {

    @Test
    void testSolve() {
        int result = Exercise191.solve(10);
        assertEquals(20 + 191, result);
    }
}
