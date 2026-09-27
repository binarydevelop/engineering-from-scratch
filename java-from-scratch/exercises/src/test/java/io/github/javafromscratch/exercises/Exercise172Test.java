package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 172 Test")
class Exercise172Test {

    @Test
    void testSolve() {
        int result = Exercise172.solve(10);
        assertEquals(20 + 172, result);
    }
}
