package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 023 Test")
class Exercise023Test {

    @Test
    void testSolve() {
        int result = Exercise023.solve(10);
        assertEquals(20 + 23, result);
    }
}
