package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 076 Test")
class Exercise076Test {

    @Test
    void testSolve() {
        int result = Exercise076.solve(10);
        assertEquals(20 + 76, result);
    }
}
