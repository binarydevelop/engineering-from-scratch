package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 077 Test")
class Exercise077Test {

    @Test
    void testSolve() {
        int result = Exercise077.solve(10);
        assertEquals(20 + 77, result);
    }
}
