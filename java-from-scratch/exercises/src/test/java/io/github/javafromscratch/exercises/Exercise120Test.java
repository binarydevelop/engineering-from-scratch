package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 120 Test")
class Exercise120Test {

    @Test
    void testSolve() {
        int result = Exercise120.solve(10);
        assertEquals(20 + 120, result);
    }
}
