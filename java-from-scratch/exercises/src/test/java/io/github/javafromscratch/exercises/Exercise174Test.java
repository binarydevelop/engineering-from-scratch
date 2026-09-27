package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 174 Test")
class Exercise174Test {

    @Test
    void testSolve() {
        int result = Exercise174.solve(10);
        assertEquals(20 + 174, result);
    }
}
