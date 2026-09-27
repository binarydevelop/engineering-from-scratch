package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 164 Test")
class Exercise164Test {

    @Test
    void testSolve() {
        int result = Exercise164.solve(10);
        assertEquals(20 + 164, result);
    }
}
