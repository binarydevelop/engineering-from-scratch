package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 072 Test")
class Exercise072Test {

    @Test
    void testSolve() {
        int result = Exercise072.solve(10);
        assertEquals(20 + 72, result);
    }
}
