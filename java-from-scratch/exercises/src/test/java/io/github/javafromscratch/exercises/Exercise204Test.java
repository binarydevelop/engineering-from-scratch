package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 204 Test")
class Exercise204Test {

    @Test
    void testSolve() {
        int result = Exercise204.solve(10);
        assertEquals(20 + 204, result);
    }
}
