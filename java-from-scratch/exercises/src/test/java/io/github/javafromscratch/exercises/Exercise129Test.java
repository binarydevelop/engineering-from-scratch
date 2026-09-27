package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 129 Test")
class Exercise129Test {

    @Test
    void testSolve() {
        int result = Exercise129.solve(10);
        assertEquals(20 + 129, result);
    }
}
