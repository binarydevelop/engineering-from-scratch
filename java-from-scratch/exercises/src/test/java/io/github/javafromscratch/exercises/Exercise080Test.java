package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 080 Test")
class Exercise080Test {

    @Test
    void testSolve() {
        int result = Exercise080.solve(10);
        assertEquals(20 + 80, result);
    }
}
