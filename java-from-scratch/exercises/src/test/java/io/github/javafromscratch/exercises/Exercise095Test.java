package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 095 Test")
class Exercise095Test {

    @Test
    void testSolve() {
        int result = Exercise095.solve(10);
        assertEquals(20 + 95, result);
    }
}
