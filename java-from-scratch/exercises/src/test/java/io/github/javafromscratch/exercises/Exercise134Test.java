package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 134 Test")
class Exercise134Test {

    @Test
    void testSolve() {
        int result = Exercise134.solve(10);
        assertEquals(20 + 134, result);
    }
}
