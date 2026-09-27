package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 015 Test")
class Exercise015Test {

    @Test
    void testSolve() {
        int result = Exercise015.solve(10);
        assertEquals(20 + 15, result);
    }
}
