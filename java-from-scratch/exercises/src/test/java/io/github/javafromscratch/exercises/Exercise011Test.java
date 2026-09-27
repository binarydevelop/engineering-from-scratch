package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 011 Test")
class Exercise011Test {

    @Test
    void testSolve() {
        int result = Exercise011.solve(10);
        assertEquals(20 + 11, result);
    }
}
