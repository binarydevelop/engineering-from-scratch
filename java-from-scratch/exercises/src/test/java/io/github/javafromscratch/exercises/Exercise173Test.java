package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 173 Test")
class Exercise173Test {

    @Test
    void testSolve() {
        int result = Exercise173.solve(10);
        assertEquals(20 + 173, result);
    }
}
