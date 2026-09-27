package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 043 Test")
class Exercise043Test {

    @Test
    void testSolve() {
        int result = Exercise043.solve(10);
        assertEquals(20 + 43, result);
    }
}
