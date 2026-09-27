package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 163 Test")
class Exercise163Test {

    @Test
    void testSolve() {
        int result = Exercise163.solve(10);
        assertEquals(20 + 163, result);
    }
}
