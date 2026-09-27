package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 024 Test")
class Exercise024Test {

    @Test
    void testSolve() {
        int result = Exercise024.solve(10);
        assertEquals(20 + 24, result);
    }
}
