package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 013 Test")
class Exercise013Test {

    @Test
    void testSolve() {
        int result = Exercise013.solve(10);
        assertEquals(20 + 13, result);
    }
}
