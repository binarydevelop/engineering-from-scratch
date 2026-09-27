package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 205 Test")
class Exercise205Test {

    @Test
    void testSolve() {
        int result = Exercise205.solve(10);
        assertEquals(20 + 205, result);
    }
}
