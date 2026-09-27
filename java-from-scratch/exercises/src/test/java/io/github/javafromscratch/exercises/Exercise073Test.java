package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 073 Test")
class Exercise073Test {

    @Test
    void testSolve() {
        int result = Exercise073.solve(10);
        assertEquals(20 + 73, result);
    }
}
