package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 061 Test")
class Exercise061Test {

    @Test
    void testSolve() {
        int result = Exercise061.solve(10);
        assertEquals(20 + 61, result);
    }
}
