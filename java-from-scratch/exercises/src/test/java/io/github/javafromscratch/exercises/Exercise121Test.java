package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 121 Test")
class Exercise121Test {

    @Test
    void testSolve() {
        int result = Exercise121.solve(10);
        assertEquals(20 + 121, result);
    }
}
