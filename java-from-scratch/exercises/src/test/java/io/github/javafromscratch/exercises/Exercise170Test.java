package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 170 Test")
class Exercise170Test {

    @Test
    void testSolve() {
        int result = Exercise170.solve(10);
        assertEquals(20 + 170, result);
    }
}
