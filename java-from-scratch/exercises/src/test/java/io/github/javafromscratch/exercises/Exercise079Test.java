package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 079 Test")
class Exercise079Test {

    @Test
    void testSolve() {
        int result = Exercise079.solve(10);
        assertEquals(20 + 79, result);
    }
}
