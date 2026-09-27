package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 127 Test")
class Exercise127Test {

    @Test
    void testSolve() {
        int result = Exercise127.solve(10);
        assertEquals(20 + 127, result);
    }
}
