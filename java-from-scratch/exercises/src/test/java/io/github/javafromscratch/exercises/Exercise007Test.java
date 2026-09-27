package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 007 Test")
class Exercise007Test {

    @Test
    void testSolve() {
        int result = Exercise007.solve(10);
        assertEquals(20 + 7, result);
    }
}
