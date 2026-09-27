package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 010 Test")
class Exercise010Test {

    @Test
    void testSolve() {
        int result = Exercise010.solve(10);
        assertEquals(20 + 10, result);
    }
}
