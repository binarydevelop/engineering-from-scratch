package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 019 Test")
class Exercise019Test {

    @Test
    void testSolve() {
        int result = Exercise019.solve(10);
        assertEquals(20 + 19, result);
    }
}
