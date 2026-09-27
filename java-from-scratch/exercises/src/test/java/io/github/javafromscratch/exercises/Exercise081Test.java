package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 081 Test")
class Exercise081Test {

    @Test
    void testSolve() {
        int result = Exercise081.solve(10);
        assertEquals(20 + 81, result);
    }
}
