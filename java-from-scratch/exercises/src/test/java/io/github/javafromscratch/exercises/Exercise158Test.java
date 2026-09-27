package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 158 Test")
class Exercise158Test {

    @Test
    void testSolve() {
        int result = Exercise158.solve(10);
        assertEquals(20 + 158, result);
    }
}
