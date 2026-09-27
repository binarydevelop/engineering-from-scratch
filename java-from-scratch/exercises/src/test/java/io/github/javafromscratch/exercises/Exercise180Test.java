package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 180 Test")
class Exercise180Test {

    @Test
    void testSolve() {
        int result = Exercise180.solve(10);
        assertEquals(20 + 180, result);
    }
}
