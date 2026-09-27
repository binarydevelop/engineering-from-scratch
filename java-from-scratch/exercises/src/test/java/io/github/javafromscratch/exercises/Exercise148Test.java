package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 148 Test")
class Exercise148Test {

    @Test
    void testSolve() {
        int result = Exercise148.solve(10);
        assertEquals(20 + 148, result);
    }
}
