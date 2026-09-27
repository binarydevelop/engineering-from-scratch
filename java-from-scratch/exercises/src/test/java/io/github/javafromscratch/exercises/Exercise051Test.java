package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 051 Test")
class Exercise051Test {

    @Test
    void testSolve() {
        int result = Exercise051.solve(10);
        assertEquals(20 + 51, result);
    }
}
