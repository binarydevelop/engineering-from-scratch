package io.github.javafromscratch.exercises;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("Exercise 184 Test")
class Exercise184Test {

    @Test
    void testSolve() {
        int result = Exercise184.solve(10);
        assertEquals(20 + 184, result);
    }
}
