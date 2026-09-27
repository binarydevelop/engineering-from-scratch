package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 069 Test")
class Exercise069Test {

    @Test
    void testSolve() {
        int result = Exercise069.solve(10);
        assertEquals(20 + 69, result);
    }
}
